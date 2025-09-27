from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from beanie import PydanticObjectId
from typing import List
from datetime import datetime

from app.models import Env, EnvKey  # <-- from earlier schema

router = APIRouter(prefix="/envs", tags=["Environments"])


# ---------------------------
# Pydantic Schemas
# ---------------------------
class EnvCreate(BaseModel):
    envName: str
    slug: str
    description: str | None = None
    createdBy: str


class EnvKeyCreateResponse(BaseModel):
    secret: str  # plain secret shown only once
    envId: str
    createdAt: datetime


class EnvResponse(BaseModel):
    id: str
    envName: str
    slug: str
    description: str | None
    createdBy: str
    createdAt: datetime


# ---------------------------
# Endpoints
# ---------------------------

# 1. Create new environment
@router.post("/", response_model=EnvResponse)
async def create_env(payload: EnvCreate):
    env = Env(**payload.dict())
    try:
        await env.insert()
    except Exception as e:
        # Handle DuplicateKeyError from pymongo/beanie
        if hasattr(e, "code") and e.code == 11000:
            # Extract duplicate key info if available
            errmsg = getattr(e, "details", {}).get("errmsg") or str(e)
            slug_val = getattr(e, "details", {}).get("keyValue", {}).get("slug")
            msg = f"Environment with slug '{slug_val or payload.slug}' already exists."
            raise HTTPException(status_code=409, detail=msg)
        raise
    return EnvResponse(
        id=str(env.id),
        envName=env.envName,
        slug=env.slug,
        description=env.description,
        createdBy=env.createdBy,
        createdAt=env.createdAt,
    )


# 2. List environments
@router.get("/", response_model=List[EnvResponse])
async def list_envs():
    envs = await Env.find_all().to_list()
    return [
        EnvResponse(
            id=str(env.id),
            envName=env.envName,
            slug=env.slug,
            description=env.description,
            createdBy=env.createdBy,
            createdAt=env.createdAt,
        )
        for env in envs
    ]


# 3. Create a new EnvKey and return secret (only once!)
@router.post("/{env_id}/keys", response_model=EnvKeyCreateResponse)
async def create_env_key(env_id: str, createdBy: str):
    env = await Env.get(env_id)
    if not env:
        raise HTTPException(status_code=404, detail="Env not found")

    plain_secret = EnvKey.generate_secret()
    hashed = EnvKey.hash_secret(plain_secret)

    env_key = EnvKey(envId=env, hashedSecret=hashed, createdBy=createdBy)
    await env_key.insert()

    return EnvKeyCreateResponse(
        secret=plain_secret,
        envId=str(env.id),
        createdAt=env_key.createdAt,
    )

async def resolve_env_from_secret(secret: str) -> Env | None:
    env_keys = await EnvKey.find(EnvKey.status == "active").to_list()
    for key in env_keys:
        if EnvKey.verify_secret(secret, key.hashedSecret):
            await key.fetch_link("envId")
            return key.envId
    return None

# 4. Lookup Env by secret
@router.post("/lookup")
async def lookup_env(secret: str):
    env = await resolve_env_from_secret(secret)
    if not env:
        raise HTTPException(status_code=401, detail="Invalid secret")
    return {"envId": str(env.id), "slug": env.slug}



# 5. Expire (deactivate) a key
@router.post("/keys/{key_id}/expire")
async def expire_key(key_id: str):
    key = await EnvKey.get(key_id)
    if not key:
        raise HTTPException(status_code=404, detail="Key not found")

    key.status = "revoked"
    await key.save()
    return {"message": "Key revoked", "keyId": str(key.id)}


# 5b. Pause (deactivate) a key
@router.post("/keys/{key_id}/pause")
async def pause_key(key_id: str):
    key = await EnvKey.get(key_id)
    if not key:
        raise HTTPException(status_code=404, detail="Key not found")

    key.status = "inactive"
    await key.save()
    return {"message": "Key paused", "keyId": str(key.id)}

# 5c. Mark key as active (if not revoked)
@router.post("/keys/{key_id}/activate")
async def activate_key(key_id: str):
    key = await EnvKey.get(key_id)
    if not key:
        raise HTTPException(status_code=404, detail="Key not found")
    if key.status == "revoked":
        raise HTTPException(status_code=400, detail="Cannot activate a revoked key")
    key.status = "active"
    await key.save()
    return {"message": "Key activated", "keyId": str(key.id)}



# 6. List keys for an environment
@router.get("/envKeys")
async def get_keys(envId: str = Query(...)):
    # Convert string to PydanticObjectId
    env_obj_id = PydanticObjectId(envId)

    # Query EnvKey directly
    keys = await EnvKey.find(EnvKey.envId.id == env_obj_id).to_list()

    return [
        {
            "id": str(k.id),
            "status": k.status,
            "createdBy": k.createdBy,
            "createdAt": k.createdAt,
        }
        for k in keys
    ]
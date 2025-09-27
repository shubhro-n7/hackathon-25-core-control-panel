from fastapi import APIRouter, Header, HTTPException, Depends
from beanie import PydanticObjectId
from app.models import View
from routers.envs import lookup_env

router = APIRouter(prefix="/secure-views", tags=["secure-views"])


@router.get("/{view_id}", response_model=dict)
async def get_secure_view(
    view_id: str,
    x_token: str = Header(..., alias="X-Token")  # not optional
):
    """
    Fetch a view by view_id + env, secured by X-Token header.
    - X-Token is matched against active EnvKeys.
    - EnvId is resolved from the secret.
    - View is returned only if it belongs to that Env.
    """

    # 1. Validate secret
    lookup_response = await lookup_env(x_token)
    env_id = lookup_response.get("envId")
    if not env_id:
        raise HTTPException(status_code=401, detail="Invalid secret")

    # 2. Fetch the view for that env + view_id
    view_doc = await View.find_one(
        View.id == PydanticObjectId(view_id),
        View.envId == env_id
    )
    if not view_doc:
        raise HTTPException(status_code=404, detail="View not found")

    # 3. Expand to full view
    return await view_doc.expand_full()

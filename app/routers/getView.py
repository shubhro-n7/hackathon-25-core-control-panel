from fastapi import APIRouter, Header, HTTPException, Depends
from beanie import PydanticObjectId
from app.models import View
from .envs import resolve_env_from_secret
from beanie import PydanticObjectId
from beanie.operators import Or

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
    lookup_response = await resolve_env_from_secret(x_token)
    if lookup_response is None:
        raise HTTPException(status_code=401, detail="Invalid secret")
    env_id = lookup_response.get("envId")

    # 2. Fetch the view for that env + view_id
    conditions = [View.name == view_id]
    try:
        conditions.append(View.viewId == int(view_id))
    except ValueError:
        pass  # not an int, only match name

    view_doc = await View.find_one(
        Or(*conditions),
        View.env.id == PydanticObjectId(env_id),
        View.status == "active"
    )
    if not view_doc:
        raise HTTPException(status_code=404, detail="View not found")

    # 3. Expand to full view
    return await view_doc.expand_full()

import httpx
import asyncio
from typing import List, Dict, Any

from models.mapping import MenuMaster, SubMenuMaster, Mapping, MenuMapping, SubMenuMapping
from models.env import Env
from core.config import settings

# --- IMPORTANT: List of View IDs to fetch ---
# For the hackathon, we'll hardcode this list.
# In a real application, you might get this from another API endpoint.
VIEW_IDS_TO_FETCH = [1, 2, 3, 4, 6, 39, 40, 41, 42, 43, 44, 67]

async def fetch_view_json(view_id: int, client: httpx.AsyncClient) -> Dict[str, Any]:
    """Fetches a single view JSON from the source API."""
    url = settings.SOURCE_API_URL.format(view_id=view_id)
    headers = {"Authorization": f"Bearer {settings.API_BEARER_TOKEN}"}
    
    try:
        response = await client.get(url, headers=headers, timeout=10.0)
        response.raise_for_status()  # Raises an exception for 4xx or 5xx status codes
        return response.json()
    except httpx.HTTPStatusError as e:
        print(f"Error fetching view {view_id}: {e.response.status_code} - {e.response.text}")
    except httpx.RequestError as e:
        print(f"Request error for view {view_id}: {e}")
    return None

async def sync_views_from_api():
    """
    Main function to orchestrate the fetching, transforming, and saving of views.
    """
    print("--- Starting View Synchronization ---")

    # 1. Clear existing data for a fresh start
    print("Clearing old data from MongoDB...")
    await MenuMaster.delete_all()
    await SubMenuMaster.delete_all()
    await Env.delete_all()
    await Mapping.delete_all()

    # 2. Fetch all raw view data concurrently
    all_views_data = []
    async with httpx.AsyncClient() as client:
        tasks = [fetch_view_json(view_id, client) for view_id in VIEW_IDS_TO_FETCH]
        results = await asyncio.gather(*tasks)
        all_views_data = [res for res in results if res is not None]

    if not all_views_data:
        print("No data fetched from the API. Aborting.")
        return {"status": "failed", "message": "No data fetched from API."}

    # 3. Create Master Data from all fetched views
    print("Creating master menu and sub-menu documents...")
    processed_menus = set()
    processed_submenus = set()
    
    for view_data in all_views_data:
        for menu_data in view_data.get("menus", []):
            menu_id = menu_data.get("menuId")
            if menu_id and menu_id not in processed_menus:
                await MenuMaster(
                    id=menu_id,
                    menuId=menu_id,
                    name=menu_data.get("name"),
                    label=menu_data.get("label"),
                    icon=menu_data.get("icon")
                ).insert()
                processed_menus.add(menu_id)

            for entity_data in menu_data.get("entities", []):
                entity_id = entity_data.get("entityId")
                if entity_id and entity_id not in processed_submenus:
                    await SubMenuMaster(
                        id=entity_id,
                        entityId=entity_id,
                        name=entity_data.get("name"),
                        label=entity_data.get("label"),
                        link=entity_data.get("link"),
                        icon=entity_data.get("icon"),
                        visible=entity_data.get("visible", True)
                    ).insert()
                    processed_submenus.add(entity_id)

    # 4. Create a default Environment
    default_env = Env(name="production")
    await default_env.insert()

    # 5. Build and Insert the final Mapping documents
    print("Building and inserting view mappings...")
    for view_data in all_views_data:
        menu_mappings = []
        for menu_data in sorted(view_data.get("menus", []), key=lambda m: m.get("order", 0)):
            master_menu = await MenuMaster.get(menu_data["menuId"])
            if not master_menu: continue

            submenu_mappings = []
            for entity_data in sorted(menu_data.get("entities", []), key=lambda e: e.get("order", 0)):
                master_submenu = await SubMenuMaster.get(entity_data["entityId"])
                if not master_submenu: continue
                
                submenu_mappings.append(SubMenuMapping(
                    submenu=master_submenu,
                    visible=entity_data.get("visible", True)
                ))
            
            menu_mappings.append(MenuMapping(
                menu=master_menu,
                submenus=submenu_mappings
            ))

        await Mapping(
            env=default_env,
            viewName=view_data["name"],
            viewId=view_data["id"],
            menus=menu_mappings,
            status="active"
        ).insert()

    print(f"--- Synchronization Complete! {len(all_views_data)} views processed. ---")
    return {"status": "success", "views_processed": len(all_views_data)}
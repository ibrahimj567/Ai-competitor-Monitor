from fastapi import APIRouter
from fastapi import Depends
from fastapi import Form
from fastapi import Request

from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse

from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.services import dashboard_service
from app.services.website_service import WebsiteService
from app.services.snapshot_service import SnapshotService
from app.services.monitor_service import MonitorService
from app.services.scheduler_service import SchedulerService
from app.services.dashboard_service import DashboardService


router = APIRouter()

templates = Jinja2Templates(
    directory="app/templates"
)


# ======================================================
# Dashboard
# ======================================================

@router.get("/", response_class=HTMLResponse)
async def dashboard(
    request: Request,
    db: Session = Depends(get_db)
):

    website_service = WebsiteService(db)
    dashboard_service = DashboardService(db)

    websites = website_service.get_all()

    stats = dashboard_service.get_dashboard_stats()

    print(stats)

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "request": request,
            "title": "CompetitorIQ Dashboard",
            "websites": websites,
            "website_count": len(websites),
            "stats": stats,
        },
    )


# ======================================================
# Add Website
# ======================================================

@router.post("/add")
async def add_website(
    url: str = Form(...),
    db: Session = Depends(get_db)
):

    WebsiteService(db).create(url)

    return RedirectResponse(
        "/",
        status_code=303
    )


# ======================================================
# Scan Website
# ======================================================



@router.get("/scan/{website_id}")
def scan(
    website_id: int,
    db: Session = Depends(get_db)
):

    website = WebsiteService(db).get(website_id)

    if website:

        scheduler = SchedulerService(db)

        scheduler.scan_now(website)

    return RedirectResponse(
        "/",
        status_code=303
    )


# ======================================================
# Delete Website
# ======================================================

@router.get("/delete/{website_id}")
async def delete(
    website_id: int,
    db: Session = Depends(get_db)
):

    WebsiteService(db).delete(
        website_id
    )

    return RedirectResponse(
        "/",
        status_code=303
    )


# ======================================================
# Website Scan History
# ======================================================

@router.get(
    "/history/{website_id}",
    response_class=HTMLResponse
)
async def website_history(
    website_id: int,
    request: Request,
    db: Session = Depends(get_db)
):

    website_service = WebsiteService(db)
    snapshot_service = SnapshotService(db)

    website = website_service.get(
        website_id
    )

    if not website:

        return RedirectResponse(
            "/",
            status_code=303
        )

    snapshots = snapshot_service.get_by_website(
        website_id
    )

    return templates.TemplateResponse(
        request=request,
        name="website_history.html",
        context={
            "request": request,
            "title": "Website History",
            "website": website,
            "snapshots": snapshots
        }
    )


# ======================================================
# Snapshot Details
# ======================================================

@router.get(
    "/snapshot/{snapshot_id}",
    response_class=HTMLResponse
)
async def snapshot_detail(
    snapshot_id: int,
    request: Request,
    db: Session = Depends(get_db)
):

    snapshot = SnapshotService(db).get(
        snapshot_id
    )

    if not snapshot:

        return RedirectResponse(
            "/",
            status_code=303
        )

    return templates.TemplateResponse(
        request=request,
        name="snapshot_detail.html",
        context={
            "request": request,
            "title": "Snapshot Details",
            "snapshot": snapshot
        }
    )
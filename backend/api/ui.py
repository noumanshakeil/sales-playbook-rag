from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db import get_db
from backend.services import playbook as svc

router = APIRouter()
templates = Jinja2Templates(directory="backend/templates")

@router.get("/", response_class=HTMLResponse)
async def home(request: Request, persona: str = "general", db: AsyncSession = Depends(get_db)):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "title": "Sales Playbook RAG",
            "persona": persona,
            "plays": await svc.list_plays(db, persona),
            "coach": None,
            "matched": [],
        },
    )

@router.post("/ui/plays")
async def ui_add(
    objection: str = Form(...),
    talk_track: str = Form(...),
    persona: str = Form("general"),
    proof: str = Form(""),
    db: AsyncSession = Depends(get_db),
):
    await svc.add_play(db, objection, talk_track, persona, proof)
    return RedirectResponse(f"/?persona={persona}", status_code=303)

@router.post("/ui/coach", response_class=HTMLResponse)
async def ui_coach(
    request: Request,
    situation: str = Form(...),
    persona: str = Form("general"),
    db: AsyncSession = Depends(get_db),
):
    result = await svc.coach(db, situation, persona)
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "title": "Sales Playbook RAG",
            "persona": persona,
            "plays": await svc.list_plays(db, persona),
            "coach": result["coach"],
            "matched": result["plays"],
            "situation": situation,
        },
    )

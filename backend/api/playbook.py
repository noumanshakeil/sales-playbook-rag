from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db import get_db
from backend.services import playbook as svc

class PlayIn(BaseModel):
    objection: str = Field(min_length=3)
    talk_track: str = Field(min_length=10)
    persona: str = "general"
    proof: str = ""

class CoachIn(BaseModel):
    situation: str = Field(min_length=5)
    persona: str | None = None

router = APIRouter()

@router.get("/plays")
async def list_plays(persona: str | None = None, db: AsyncSession = Depends(get_db)):
    rows = await svc.list_plays(db, persona)
    return {
        "plays": [
            {"id": p.id, "persona": p.persona, "objection": p.objection}
            for p in rows
        ]
    }

@router.post("/plays")
async def create(payload: PlayIn, db: AsyncSession = Depends(get_db)):
    p = await svc.add_play(db, payload.objection, payload.talk_track, payload.persona, payload.proof)
    return {"id": p.id}

@router.post("/coach")
async def coach(payload: CoachIn, db: AsyncSession = Depends(get_db)):
    return await svc.coach(db, payload.situation, payload.persona)

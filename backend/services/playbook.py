from __future__ import annotations
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.llm import get_llm
from backend.models import Play
from backend.services.rag_core import score_chunk

async def add_play(
    session: AsyncSession,
    objection: str,
    talk_track: str,
    persona: str = "general",
    proof: str = "",
) -> Play:
    row = Play(
        id=uuid.uuid4().hex[:10],
        persona=(persona or "general").lower()[:80],
        objection=objection.strip()[:200],
        talk_track=talk_track.strip(),
        proof=proof.strip(),
    )
    session.add(row)
    await session.commit()
    await session.refresh(row)
    return row

async def list_plays(session: AsyncSession, persona: str | None = None) -> list[Play]:
    stmt = select(Play)
    if persona:
        stmt = stmt.where(Play.persona == persona.lower())
    return list((await session.execute(stmt.order_by(Play.created_at.desc()))).scalars())

async def coach(session: AsyncSession, situation: str, persona: str | None = None) -> dict:
    plays = await list_plays(session, persona)
    scored = []
    for p in plays:
        blob = f"{p.objection}\n{p.talk_track}\n{p.proof}"
        s = score_chunk(situation, blob)
        if s <= 0:
            continue
        scored.append((s, p))
    scored.sort(key=lambda x: x[0], reverse=True)
    top = scored[:4]
    context = "\n\n".join(
        f"[{i}] objection={p.objection}\ntalk={p.talk_track}\nproof={p.proof}"
        for i, (_, p) in enumerate(top, start=1)
    ) or "(no plays)"
    llm = get_llm()
    draft = await llm.complete(
        f"Sales coach. Use ONLY playbook entries.\nSITUATION: {situation}\n\nPLAYS:\n{context}",
        system="Be concise. Give a talk track + one proof point.",
    )
    return {
        "coach": draft,
        "plays": [
            {
                "index": i,
                "id": p.id,
                "objection": p.objection,
                "persona": p.persona,
                "score": round(s, 3),
                "talk_track": p.talk_track[:300],
            }
            for i, (s, p) in enumerate(top, start=1)
        ],
    }

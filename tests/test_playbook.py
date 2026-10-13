import pytest

@pytest.mark.asyncio
async def test_coach(client):
    await client.post(
        "/api/plays",
        json={
            "persona": "cfo",
            "objection": "Too expensive",
            "talk_track": "Shift to cost of delay and payback period under 2 quarters.",
            "proof": "Acme cut ops cost 18% in 90 days.",
        },
    )
    r = await client.post(
        "/api/coach",
        json={"situation": "CFO says pricing is too high vs incumbent", "persona": "cfo"},
    )
    assert r.status_code == 200
    assert r.json()["plays"]

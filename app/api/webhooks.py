from fastapi import APIRouter, Request

router = APIRouter()


@router.post("/telephony/webhook")
async def telephony_webhook(
    request: Request
):

    data = await request.json()

    return {
        "status": "received",
        "data": data
    }
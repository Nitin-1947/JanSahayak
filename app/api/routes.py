from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def root():

    return {
        "message":
            "Hindi Government AI Assistant is running."
    }
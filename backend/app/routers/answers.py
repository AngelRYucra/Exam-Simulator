from fastapi import APIRouter

router = APIRouter(
    prefix="/answers",
    tags=["Answers"]
)

@router.get("/")
def get_answers():
    return {"message": "List of answers (all)"}   
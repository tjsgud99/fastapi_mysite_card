from fastapi import APIRouter
from backend.schemas.message import MessageDTO
from backend.services.service_kakao import KakaoService
router = APIRouter(
    tags=["Kakao"],
)

@router.post("/")   #http://127.0.0.1:8000/kakao/
async def send_message(msg: MessageDTO) -> dict:
    KakaoService().send_message(msg)
    return {"status" : {"code" : 200, "message" : "success"}}
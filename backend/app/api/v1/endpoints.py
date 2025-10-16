from fastapi import APIRouter, Response
from app.utils.camera import generate, get_capture
from fastapi.responses import StreamingResponse
router = APIRouter()

@router.post("/capture")
async def capture():
    return {"message": "pong"}

@router.get('/video_feed')
def video_feed():
    return StreamingResponse(generate(), media_type='multipart/x-mixed-replace; boundary=frame')

@router.get("/proxy_capture")
def proxy_capture():
    content = get_capture()
    return Response(content=content, media_type="image/jpeg")
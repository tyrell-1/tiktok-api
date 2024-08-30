from fastapi import FastAPI
from fastapi.responses import Response
from .tiktok import TiktokClient
import requests

app = FastAPI()
tt = TiktokClient()

@app.get("/info/{video_id}")
async def tiktokvideo(video_id: str):
    video_info = tt.get_video_info_by_id(video_id)
    video_info.local_source_url = f"/video/{video_info.id_str}"
    return dict(video_info)

@app.get("/video/{video_id}")
async def video(video_id: str):
    video_info = tt.get_video_info_by_id(video_id)
    source_url = video_info.source_urls[-1]
    res = requests.get(source_url)
    reponse = Response(content=res.content, media_type="video/mp4")
    return reponse
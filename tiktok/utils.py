import json
import re
from .models import TiktokSlideshow, TikTokVideo

def clean_url(url: str) -> str:
    return url.split("?")[0].strip()

def validate_url(video_url: str) -> bool:
    tiktok_url_pattern = re.compile(r'(https?://)?(www\.)?(tiktok\.com/@[\w.-]+/(video|photo)/\d{19}|vm\.tiktok\.com/[\w./]+)', re.IGNORECASE)
    return bool(re.match(tiktok_url_pattern, clean_url(video_url)))

def get_video_id_from_url(video_url: str) -> str:
    return video_url.split("?")[0].split("/")[-1]

def extract_hashtags(video_description: str) -> dict:
    hashtags = re.findall(r'#(\w+)', video_description)
    return hashtags

def get_full_title(video_info: TikTokVideo | TiktokSlideshow) -> str:
    return video_info.description + " " + " ".join([f"[#{hashtag.name}]({hashtag.url})" for hashtag in video_info.hashtags]) 
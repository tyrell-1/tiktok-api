import requests
import json
from .models import *
from .utils import *

class TiktokClient:
    BASE_URL = "https://www.tiktok.com/player/api/v1/items"
    def __init__(self) -> None:
        pass
    
    def get_video_info_by_id(self, video_id: str | int) -> TikTokVideo | TiktokSlideshow:
        video_id = str(video_id)
        params = {
            "item_ids": video_id,
            "language": "en-GB"
            }
        response = requests.get(self.BASE_URL, params=params)
        response.raise_for_status()
        if response.status_code != 200:
            raise Exception(f"Failed to fetch video with ID {video_id}. Status code: {response.status_code}")
        
        json_data = response.json()['items'][0]

        returns = TikTokVideo(
                    id=json_data['id'],
                    id_str=json_data['id_str'],
                    description=json_data['desc'].split("#")[0].strip(),
                    hashtags=[Hashtag(name=hashtag, url=f"https://www.tiktok.com/tag/{hashtag}") for hashtag in extract_hashtags(json_data['desc'])],
                    author=Author(
                        username=json_data['author_info']['unique_id'],
                        nickname=json_data['author_info']['nickname'],
                        avatar_url=json_data['author_info']['avatar_url_list'][1]
                        ),
                    music=MusicInfo(
                        id=json_data['music_info']['id'],
                        id_str=json_data['music_info']['id_str'],
                        title=json_data['music_info']['title'],
                        artist_name=json_data['music_info']['author']
                        ),
                    source_urls=json_data['video_info']['url_list'],
                    stats=StatisticsInfo(
                        comment_count=json_data['statistics_info']['comment_count'],
                        digg_count=json_data['statistics_info']['digg_count'],
                        share_count=json_data['statistics_info']['share_count']
                    )
                    )
        
        if json_data['aweme_type'] == 150:
            returns.is_slideshow = True
            returns = TiktokSlideshow(**dict(returns), image_urls=[image['display_image']['url_list'][1] for image in json_data['image_post_info']['images']])

        return returns
    
    def get_original_video_url(self, video_url: str) -> str:
        return requests.get(video_url, allow_redirects=True).url
    
    def get_video_info_by_url(self, video_url: str) -> TikTokVideo | TiktokSlideshow:
        assert validate_url(video_url)
        if "vm.tiktok.com" in video_url:
            video_url = self.get_original_video_url(video_url)
        video_id = get_video_id_from_url(video_url)
        return self.get_video_info_by_id(video_id)
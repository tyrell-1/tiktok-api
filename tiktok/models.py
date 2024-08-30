from pydantic import BaseModel


class Author(BaseModel):
    username: str
    nickname: str
    avatar_url: str

class MusicInfo(BaseModel):
    id: int
    id_str: str
    title: str
    artist_name: str

class StatisticsInfo(BaseModel):
    digg_count: int
    comment_count: int
    share_count: int

class Hashtag(BaseModel):
    name: str
    url: str

class TikTokVideo(BaseModel):
    id: int
    id_str: str
    description: str
    author: Author
    music: MusicInfo
    stats: StatisticsInfo
    source_urls: list[str]
    local_source_url: str | None = None
    is_slideshow: bool = False
    hashtags: list[Hashtag]

class TiktokSlideshow(TikTokVideo):
    image_urls: list[str]
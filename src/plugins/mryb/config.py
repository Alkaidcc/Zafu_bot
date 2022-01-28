from typing import Optional
from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here
    abot_dir: Optional[str] = None
    user_id: Optional[str] = None
    password: Optional[str] = None
    group_id: Optional[str] = None

    class Config:
        extra = "ignore"
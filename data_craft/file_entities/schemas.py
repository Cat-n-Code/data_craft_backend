from typing import Optional

from pydantic import BaseModel, ConfigDict


class FileEntitySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    filename: str
    full_url: str

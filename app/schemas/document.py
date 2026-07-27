from uuid import UUID

from pydantic import BaseModel, ConfigDict


class DocumentCreate(BaseModel):
    filename: str
    file_path: str
    file_size: int


class DocumentResponse(BaseModel):
    id: UUID
    filename: str
    file_path: str
    file_size: int
    status: str

    model_config = ConfigDict(from_attributes=True)
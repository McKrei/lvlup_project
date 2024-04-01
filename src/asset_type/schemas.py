from pydantic import BaseModel


class AssetTypeCreate(BaseModel):
    type_name: str



class AssetTypeOut(BaseModel):
    id: int
    type_name: str

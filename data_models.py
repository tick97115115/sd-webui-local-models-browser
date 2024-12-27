from pydantic import BaseModel

class Lora(BaseModel):
    name: str
    alias: str
    path: str
    
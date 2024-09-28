from pydantic import BaseModel, Field


class InputCl(BaseModel):
    text: str

class OutputCl(BaseModel):
    tags: list[str]

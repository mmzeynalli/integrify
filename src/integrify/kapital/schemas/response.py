from pydantic import BaseModel


class CreateOrderResponseSchema(BaseModel):
    id: int
    password: str
    redirect_url: str

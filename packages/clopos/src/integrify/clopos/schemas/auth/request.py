from integrify.api import PayloadBaseModel
from integrify.clopos import env
from pydantic import Field


class AuthRequest(PayloadBaseModel):
    client_id: str = Field(default=env.CLOPOS_CLIENT_ID, min_length=1, validate_default=True)
    client_secret: str = Field(
        default=env.CLOPOS_CLIENT_SECRET,
        min_length=1,
        validate_default=True,
    )
    brand: str = Field(default=env.CLOPOS_BRAND, min_length=1, validate_default=True)
    integrator_id: str = Field(
        default=env.CLOPOS_INTEGRATOR_ID,
        min_length=1,
        validate_default=True,
    )

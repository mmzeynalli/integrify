from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_pascal


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_pascal,
        populate_by_name=True,
        from_attributes=True,
    )

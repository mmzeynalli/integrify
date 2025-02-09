from datetime import datetime
from hashlib import md5
from typing import ClassVar, Optional

from pydantic import Field, computed_field

from integrify.lsim import env
from integrify.schemas import PayloadBaseModel


class SendSMSPostRequestSchema(PayloadBaseModel):
    login: Optional[str] = env.LSIM_LOGIN

    msisdn: str  # phone number

    text: str

    sender: Optional[str] = env.LSIM_SENDER_NAME

    scheduled: Optional[str] = Field(default='NOW')

    unicode: Optional[bool] = False

    @computed_field
    def key(self) -> str:
        """LSIM ucun key generasiyasi"""
        return md5(
            (
                md5(env.LSIM_PASSWORD.encode()).hexdigest()
                + self.login
                + self.text
                + self.msisdn
                + self.sender
            ).encode()
        ).hexdigest()


class CheckBalanceRequestSchema(PayloadBaseModel):
    URL_PARAM_FIELDS: ClassVar[set[str]] = {'login', 'key'}

    login: Optional[str] = env.LSIM_LOGIN

    @computed_field
    def key(self) -> str:
        """LSIM ucun key generasiyasi"""
        return md5((md5(env.LSIM_PASSWORD.encode()).hexdigest() + self.login).encode()).hexdigest()


class GetReportGetRequestSchema(PayloadBaseModel):
    login: Optional[str] = env.LSIM_LOGIN
    transid: int

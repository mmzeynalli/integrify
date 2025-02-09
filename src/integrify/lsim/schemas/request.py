from hashlib import md5

from pydantic import Field, computed_field

from integrify.lsim import env
from integrify.schemas import PayloadBaseModel


class SendSMSGetRequestSchema(PayloadBaseModel):
    login: str = Field(default=env.LSIM_LOGIN)  # type: ignore[assignment]

    msisdn: str  # phone number

    text: str

    sender: str = Field(default=env.LSIM_SENDER_NAME)  # type: ignore[assignment]

    unicode: bool = Field(default=False)

    @computed_field
    def key(self) -> str:
        """LSIM ucun key generasiyasi"""
        assert env.LSIM_PASSWORD
        return md5(
            (
                md5(env.LSIM_PASSWORD.encode()).hexdigest()
                + self.login
                + self.text
                + self.msisdn
                + self.sender
            ).encode()
        ).hexdigest()


class SendSMSPostRequestSchema(SendSMSGetRequestSchema):
    scheduled: str = Field(default='NOW')


class CheckBalanceRequestSchema(PayloadBaseModel):
    login: str = Field(default=env.LSIM_LOGIN)  # type: ignore[assignment]

    @computed_field
    def key(self) -> str:
        """LSIM ucun key generasiyasi"""
        assert env.LSIM_PASSWORD

        return md5((md5(env.LSIM_PASSWORD.encode()).hexdigest() + self.login).encode()).hexdigest()


class GetReportGetRequestSchema(PayloadBaseModel):
    login: str = Field(default=env.LSIM_LOGIN)  # type: ignore[assignment]
    transid: int

from hashlib import md5

from pydantic import Field, computed_field

from integrify.lsim import env
from integrify.schemas import PayloadBaseModel


class SendSMSGetRequestSchema(PayloadBaseModel):
    msisdn: str
    """SMS göndəriləcək nömrə: ölkə kodu + operator kodu + nömrə: 99450XXXXXXX"""

    text: str
    """Mesaj məzmunu"""

    # Not required
    login: str = env.LSIM_LOGIN  # type: ignore[assignment]
    password: str = Field(default=env.LSIM_PASSWORD, exclude=True)  # type: ignore[assignment]
    sender: str = env.LSIM_SENDER_NAME  # type: ignore[assignment]
    """SMS göndərənin adı (LSIM tərəfindən təmin olunur)"""
    unicode: bool = False
    """Mesajın unicode olub/olmaması. Əgər mesajda unikod simvollar (`ə`, `ş`, `ü` və s.) istifadə
    edirsizsə, `True` seçməlisiniz."""

    @computed_field
    def key(self) -> str:
        """LSIM ucun key generasiyasi"""
        return md5(
            (
                md5(self.password.encode()).hexdigest()  # pylint: disable=no-member
                + self.login
                + self.text
                + self.msisdn
                + self.sender
            ).encode()
        ).hexdigest()


class SendSMSPostRequestSchema(SendSMSGetRequestSchema):
    scheduled: str = 'NOW'


class CheckBalanceRequestSchema(PayloadBaseModel):
    login: str = env.LSIM_LOGIN  # type: ignore[assignment]
    password: str = Field(default=env.LSIM_PASSWORD, exclude=True)  # type: ignore[assignment]

    @computed_field
    def key(self) -> str:
        """LSIM ucun key generasiyasi"""
        return md5((md5(self.password.encode()).hexdigest() + self.login).encode()).hexdigest()  # pylint: disable=no-member


class GetReportRequestSchema(PayloadBaseModel):
    transid: int

    # Not required
    login: str = env.LSIM_LOGIN  # type: ignore[assignment]
    """Uğurlu SMS göndərildikdə alınan transaction id"""

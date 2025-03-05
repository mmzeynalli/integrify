from pydantic import Field

from integrify.lsim import env
from integrify.lsim.types import DateTime
from integrify.schemas import PayloadBaseModel


class SendBulkSMSOneMessageRequestSchema(PayloadBaseModel):
    controlid: int

    msisdns: list[str]
    bulkmessage: str

    scheduled: DateTime
    login: str = Field(env.LSIM_LOGIN, validate_default=True)  # type: ignore[assignment]
    password: str = Field(default=env.LSIM_PASSWORD, validate_default=True)  # type: ignore[assignment]
    title: str = Field(default=env.LSIM_SENDER_NAME, validate_default=True)  # type: ignore[assignment]

    operation: str = 'submit'
    isbulk: bool = True


class SendBulkSMSDifferentMessagesRequestSchema(PayloadBaseModel):
    controlid: int

    msisdns: list[str]
    messages: list[str]

    scheduled: DateTime
    login: str = Field(env.LSIM_LOGIN, validate_default=True)  # type: ignore[assignment]
    password: str = Field(default=env.LSIM_PASSWORD, validate_default=True)  # type: ignore[assignment]
    title: str = Field(default=env.LSIM_SENDER_NAME, validate_default=True)  # type: ignore[assignment]

    operation: str = 'submit'
    isbulk: bool = False


class GetBulkSMSReportRequestSchema(PayloadBaseModel):
    taskid: int

    login: str = Field(env.LSIM_LOGIN, validate_default=True)  # type: ignore[assignment]
    password: str = Field(default=env.LSIM_PASSWORD, validate_default=True)  # type: ignore[assignment]
    operation: str = 'report'


class GetBulkSMSDeatiledReportRequestSchema(GetBulkSMSReportRequestSchema):
    operation: str = 'detailedreport'


class GetBulkSMSDeatiledWithDateReportRequestSchema(GetBulkSMSReportRequestSchema):
    operation: str = 'detailedreportwithdate'


class GetBalanceRequestSchema(PayloadBaseModel):
    login: str = Field(env.LSIM_LOGIN, validate_default=True)  # type: ignore[assignment]
    password: str = Field(default=env.LSIM_PASSWORD, validate_default=True)  # type: ignore[assignment]
    operation: str = 'units'

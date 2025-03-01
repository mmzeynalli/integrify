from pydantic import Field

from integrify.lsim import env
from integrify.schemas import PayloadBaseModel


class SendBulkSMSOneMessageRequestSchema(PayloadBaseModel):
    controlid: int

    msisdns: list[str]
    bulkmessage: str

    scheduled: str = 'NOW'
    login: str = Field(env.LSIM_LOGIN, validate_default=True)  # type: ignore[assignment]
    password: str = Field(default=env.LSIM_PASSWORD, validate_default=True)  # type: ignore[assignment]
    title: str = Field(default=env.LSIM_SENDER_NAME, validate_default=True)  # type: ignore[assignment]

    operation: str = 'submit'
    isbulk: bool = True

    def model_dump(
        self,
        *,
        mode='python',
        include=None,
        exclude=None,
        context=None,
        by_alias=False,
        exclude_unset=False,
        exclude_defaults=False,
        exclude_none=False,
        round_trip=False,
        warnings=True,
        serialize_as_any=False,
    ):
        data = super().model_dump(
            mode=mode,
            include=include,
            exclude=exclude,
            context=context,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            round_trip=round_trip,
            warnings=warnings,
            serialize_as_any=serialize_as_any,
        )

        msisdns = data.pop('msisdns')

        return {'request': {'head': data, 'body': [{'msisdn': msisdn} for msisdn in msisdns]}}


class SendBulkSMSDifferentMessagesRequestSchema(PayloadBaseModel):
    controlid: int

    msisdns: list[str]
    messages: list[str]

    scheduled: str = 'NOW'
    login: str = Field(env.LSIM_LOGIN, validate_default=True)  # type: ignore[assignment]
    password: str = Field(default=env.LSIM_PASSWORD, validate_default=True)  # type: ignore[assignment]
    title: str = Field(default=env.LSIM_SENDER_NAME, validate_default=True)  # type: ignore[assignment]

    operation: str = 'submit'
    isbulk: bool = False

    def model_dump(
        self,
        *,
        mode='python',
        include=None,
        exclude=None,
        context=None,
        by_alias=False,
        exclude_unset=False,
        exclude_defaults=False,
        exclude_none=False,
        round_trip=False,
        warnings=True,
        serialize_as_any=False,
    ):
        data = super().model_dump(
            mode=mode,
            include=include,
            exclude=exclude,
            context=context,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            round_trip=round_trip,
            warnings=warnings,
            serialize_as_any=serialize_as_any,
        )

        msisdns = data.pop('msisdns')
        messages = data.pop('messages')

        return {
            'request': {
                'head': data,
                'body': [
                    {'msisdn': msisdn, 'message': message}
                    for msisdn, message in zip(msisdns, messages)
                ],
            }
        }


class GetBulkSMSReportRequestSchema(PayloadBaseModel):
    taskid: int

    login: str = Field(env.LSIM_LOGIN, validate_default=True)  # type: ignore[assignment]
    password: str = Field(default=env.LSIM_PASSWORD, validate_default=True)  # type: ignore[assignment]
    operation: str = 'report'

    def model_dump(
        self,
        *,
        mode='python',
        include=None,
        exclude=None,
        context=None,
        by_alias=False,
        exclude_unset=False,
        exclude_defaults=False,
        exclude_none=False,
        round_trip=False,
        warnings=True,
        serialize_as_any=False,
    ):
        data = super().model_dump(
            mode=mode,
            include=include,
            exclude=exclude,
            context=context,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            round_trip=round_trip,
            warnings=warnings,
            serialize_as_any=serialize_as_any,
        )

        return {'request': {'head': data}}


class GetBulkSMSDeatiledReportRequestSchema(GetBulkSMSReportRequestSchema):
    operation: str = 'detailedreport'


class GetBulkSMSDeatiledWithDateReportRequestSchema(GetBulkSMSReportRequestSchema):
    operation: str = 'detailedreportwithdate'


class GetBalanceRequestSchema(PayloadBaseModel):
    login: str = Field(env.LSIM_LOGIN, validate_default=True)  # type: ignore[assignment]
    password: str = Field(default=env.LSIM_PASSWORD, validate_default=True)  # type: ignore[assignment]
    operation: str = 'units'

    def model_dump(
        self,
        *,
        mode='python',
        include=None,
        exclude=None,
        context=None,
        by_alias=False,
        exclude_unset=False,
        exclude_defaults=False,
        exclude_none=False,
        round_trip=False,
        warnings=True,
        serialize_as_any=False,
    ):
        data = super().model_dump(
            mode=mode,
            include=include,
            exclude=exclude,
            context=context,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            round_trip=round_trip,
            warnings=warnings,
            serialize_as_any=serialize_as_any,
        )

        return {'request': {'head': data}}

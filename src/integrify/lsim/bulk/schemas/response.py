from typing import Optional, Union

from pydantic import BaseModel, Field, model_validator

from integrify.lsim.bulk.schemas.enums import Code, SMSStatus


class SendBulkSMSResponseSchema(BaseModel):
    response_code: Union[Code, int]
    """Sorğunun uğur(suz)luq kodu"""

    task_id: Optional[int] = None
    """Sorğunun id-si. Bu id-ni report almaqda istifadə edə bilərsiniz"""

    @model_validator(mode='before')
    @classmethod
    def dissect_data(cls, data: dict):
        """Sorğunun cavabının strukturunu parçalayan funksiya"""
        return {
            'response_code': data['response']['head']['responsecode'],
            'task_id': data['response'].get('body', {}).get('taskid'),
        }


class GetBulkSMSReportResponseSchema(BaseModel):
    response_code: Union[Code, int]
    """Sorğunun uğur(suz)luq kodu"""

    expired: int = -1
    """Vaxtı keçmiş SMS sayı"""

    removed: int = -1
    """Silinmiş SMS sayı"""

    black_list: int = Field(-1, validation_alias='blackList')
    """Qara list-ə düşmüş SMS sayı"""

    undelivered: int = -1
    """Göndərilməyən SMS sayı"""

    delivered: int = -1
    """Göndərilmiş və çatmış SMS sayı"""

    duplicate: int = -1
    """Təkrarlanan (duplikat) SMS sayı"""

    error: int = -1
    """Xətalı SMS sayı"""

    send: int = -1
    """Göndərilmiş SMS sayı"""

    queue: int = -1
    """Göndərilmə sırasında olan SMS sayı"""

    @model_validator(mode='before')
    @classmethod
    def dissect_data(cls, data: dict):
        """Sorğunun cavabının strukturunu parçalayan funksiya"""
        return {
            'response_code': data['response']['head']['responsecode'],
            **data['response'].get('body', {}),
        }


class SMSReportSchema(BaseModel):
    msisdn: int
    message: str
    status: SMSStatus
    date: Optional[str] = None


class GetBulkSMSDetailedReportResponseSchema(BaseModel):
    response_code: Union[Code, str]
    """Sorğunun uğur(suz)luq kodu"""

    body: list[SMSReportSchema]

    @model_validator(mode='before')
    @classmethod
    def dissect_data(cls, data: dict):
        """Sorğunun cavabının strukturunu parçalayan funksiya"""
        return {
            'response_code': int(data['response']['head']['responsecode']),
            'body': data['response'].get('body', []),
        }


class GetBalanceResponseSchema(BaseModel):
    response_code: Union[Code, str]
    """Sorğunun uğur(suz)luq kodu"""

    units: int
    """Balans"""

    @model_validator(mode='before')
    @classmethod
    def dissect_data(cls, data: dict):
        """Sorğunun cavabının strukturunu parçalayan funksiya"""
        return {
            'response_code': data['response']['head']['responsecode'],
            'units': data['response']['body']['units'],
        }

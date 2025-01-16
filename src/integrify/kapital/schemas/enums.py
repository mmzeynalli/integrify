from enum import Enum


class TransactionStatus(str, Enum):
    BEING_PREPARED = 'Preparing'
    """Order is being prepared, no transactions have been executed on it yet."""

    CANCELLED = 'Cancelled'
    """Order has been cancelled by the consumer (before payment). (Order is cancelled by the merchant.)"""  # noqa: E501

    REJECTED = 'Rejected'
    """Order has been rejected by the PSP (before payment). (Order is rejected by the PSP.)"""

    REFUSED = 'Refused'
    """Consumer has refused to pay for the order (before payment or after unsuccessful payment attempt). (Order is refused by the consumer.)"""  # noqa: E501

    EXPIRED = 'Expired'
    """Order has expired (before payment). (Timeout occurs when executing the order scenario.)"""

    AUTHORIZED = 'Authorized'
    """Order has been authorized.(Authorization transaction is executed.)"""

    PARTIALLY_PAID = 'PartiallyPaid'
    """Order has been partially paid. (Clearing transaction is executed for the part of the order amount.)"""  # noqa: E501

    FULLY_PAID = 'FullyPaid'
    """Order has been fully paid. (Clearing transaction is executed for the full order amount (or several clearing transactions).)"""  # noqa: E501

    FUNDED = 'Funded'
    """Order has been funded (debit transaction has been executed). The status can be assigned only to the order of the DualStep Transfer Order class."""  # noqa: E501

    DECLINED = 'Declined'
    """* AReq and RReq (3DS 2) could not be executed due to rejection by the issuer / error during authentication.
        * Operation was declined by PMO"""  # noqa: E501

    VOIDED = 'Voided'
    """Authorized payment amount under the order is zero."""

    REFUNDED = 'Refunded'
    """Accounted payment amount and the accounted refund amount under the order are equal."""

    CLOSED = 'Closed'
    """Order has been closed (after payment)"""


class ErrorCode(str, Enum):
    INVALID_AMOUNT = 'InvalidAmt'
    """Invalid amount"""

    INVALID_REQUEST = 'InvalidRequest'
    """Invalid request"""

    INVALID_TRANSACTION = 'InvalidTran'
    """Invalid transaction"""

    INVALID_TRANSACTION_LINKAGE = 'InvalidTranLink'
    """Invalid transaction linkage"""

    TRANSACTION_PROHIBITED = 'TranProhibited'
    """Transaction prohibited"""

    ACTION_APP_EXCEPTION = 'ActionAppException'

    CANT_CHOOSE_SETTLEMENT_ACCOUNT = 'CantChooseSettleAcct'
    """Can't choose settlement account"""

    PMO_INTERFACE_NOT_FOUND = 'PmoIfaceNotFound'
    """Pmo interface not found"""

    PMO_DECLINE = 'PmoDecline'
    """Transaction declined by PMO: {reason}"""

    PMO_UNREACHABLE = 'PmoUnreachable'
    """Can't reach PMO"""

    INVALID_CERTIFICATE = 'InvalidCert'
    """Invalid certificate"""

    INVALID_LOGIN = 'InvalidLogin'
    """Invalid login or password"""

    INVALID_ORDER_STATE = 'InvalidOrderState'
    """Invalid order state"""

    INVALID_USER_SESSION = 'InvalidUserSession'
    """Invalid user session"""

    NEED_CHANGE_PASSWORD = 'NeedChangePwd'
    """Need change password"""

    OPERATION_PROHIBITED = 'OperationProhibited'
    """Operation prohibited"""

    PASSWORD_TRY_LIMIT_EXCEEDED = 'PwdTryLimitExceeded'
    """Password try limit exceeded"""

    USER_SESSION_EXPIRED = 'UserSessionExpired'
    """User session expired"""

    COF_PROVIDER_DECLINE = 'CofpDecline'
    """Declined by CoF Provider: {Reason}"""

    COF_PROVIDER_UNREACHABLE = 'CofpUnreachable'
    """Can't reach CoF Provider"""

    INVALID_TOKEN = 'InvalidToken'
    """Invalid token"""

    INVALID_AUTH_STATUS = 'InvalidAutStatus'
    """Invalid authentication status"""

    CONSUMER_NOT_FOUND = 'ConsumerNotFound'
    """Consumer not found"""

    INVALID_CONSUMER = 'InvalidConsumer'
    """Invalid consumer"""

    INVALID_SECRET = 'InvalidSecret'
    """Invalid secret code"""

    SECRET_TRY_LIMIT_EXCEEDED = 'SecretTryLimit'
    """Secret try limit has been exceeded"""

    SERVICE_ERROR = 'ServiceError'
    """Service error"""


PMO_RESULT_CODES = {
    '0': '-',
    '1': 'Approved',
    '2': 'Approved Partial',
    '3': 'Approved Purchase Only',
    '4': 'Postponed',
    '5': 'Strong customer authentication required',
    '6': "Need Checker's confirmation",
    '7': 'Telebank customer already exists',
    '8': 'Should select virtual card product',
    '9': 'Should select account number',
    '10': 'Should change PVV',
    '11': 'Confirm payment precheck',
    '12': 'Select bill',
    '13': 'Customer confirmation requested',
    '14': 'Original transaction not found',
    '15': 'Slip already received',
    '16': 'Personal information input error',
    '17': 'SMS/EMail dynamic password requested',
    '18': 'DPA/CAP dynamic password requested',
    '19': 'Prepaid code not found',
    '20': 'Prepaid code not found',
    '21': 'Corresponding account exhausted',
    '22': 'Acquirer limit exceeded',
    '23': 'Cutover in process',
    '24': 'Dynamic PVV Expired',
    '25': 'Weak PIN',
    '26': 'External authentication required',
    '27': 'Additional data required',
    '29': 'Closed account',
    '30': 'Blocked',
    '40': 'Lost card',
    '41': 'Stolen card',
    '49': 'Ineligible vendor account',
    '50': 'Unauthorized usage',
    '51': 'Expired card',
    '52': 'Invalid card',
    '53': 'Invalid PIN',
    '54': 'System error',
    '55': 'Ineligible transaction',
    '56': 'Ineligible account',
    '57': 'Transaction not supported',
    '58': 'Restricted card',
    '59': 'Insufficient funds',
    '60': 'Uses limit exceeded',
    '61': 'Withdrawal limit would be exceeded',
    '62': 'PIN tries limit was reached',
    '63': 'Withdrawal limit already reached',
    '64': 'Credit amount limit',
    '65': 'No statement information',
    '66': 'Statement not available',
    '67': 'Invalid amount',
    '68': 'External decline',
    '69': 'No sharing',
    '71': 'Contact card issuer',
    '72': 'Destination not available',
    '73': 'Routing error',
    '74': 'Format error',
    '75': 'External decline special condition',
    '80': 'Bad CW',
    '81': 'Bad CVV2',
    '82': 'Invalid transaction',
    '83': 'PIN tries limit was exceeded',
    '84': 'Bad CAVV',
    '85': 'Bad ARQC',
    '90': 'Approve administrative card operation inside window',
    '91': 'Approve administrative card operation outside of window',
    '92': 'Approve administrative card operation',
    '93': 'Should select card',
    '94': 'Confirm Issuer Fee',
    '95': 'Insufficient cash',
    '96': 'Approved frictionless',
    '98': 'Invalid merchant',
}

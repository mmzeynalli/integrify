from integrify.epoint.helpers import decode_callback_data
from integrify.epoint.schemas.callback import CallbackDataSchema
from tests.epoint.conftest import requires_env


def test_str_to_dict():
    schema = CallbackDataSchema.model_validate(b'data=data&signature=signature')

    assert schema.data == 'data'
    assert schema.signature == 'signature'


def test_wrong_signature_response():
    schema = CallbackDataSchema.model_validate(b'data=data&signature=signature')

    assert decode_callback_data(schema) is None


@requires_env()
def test_ok_signature_response():
    # data is: {"status": "sucess"}
    schema = CallbackDataSchema.model_validate(
        b'data=eyJzdGF0dXMiOiAic3VjY2VzcyJ9&signature=EG7cnaJteYS6cVuR2aqDvpecQtk='
    )

    data = decode_callback_data(schema)

    assert data.status == 'success'

from integrify.api import APIPayloadHandler
from integrify.azericard.schemas.request import AuthRequestSchema
from integrify.azericard.schemas.response import AuthResponseSchema


class AuthPayloadHandler(APIPayloadHandler):
    def __init__(self):
        super().__init__(AuthRequestSchema, AuthResponseSchema)

from typing import Optional

from integrify.clopos import env
from integrify.clopos.client import CloposClientClass
from integrify.utils import UNSET


class CloposTestClientClass(CloposClientClass):
    _token: Optional[str] = None

    def _build_request_lambda(self, func, url, verb, handler):
        # No headers needed in auth
        if url.endswith(env.API.AUTH):
            return super()._build_request_lambda(func, url, verb, handler)

        return lambda *args, **kwds: func(
            url,
            verb,
            handler,
            *(arg for arg in args if arg is not UNSET),
            headers={'x-token': self._token},
            **{k: v for k, v in kwds.items() if v is not UNSET},
        )

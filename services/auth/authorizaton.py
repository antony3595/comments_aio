import base64
import hashlib
import hmac
import json
from datetime import datetime, timedelta
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

import config
from repository.enums.scope import Scope
from repository.user import UserRepository
from schema.api.auth import TokenPayload, BaseTokenPayload
from schema.db.user import UserSchema
from schema.query.user import UserReadQuery
from services.auth.exceptions import AuthorizationException, AuthenticationException


class AuthService:
    def generate_token(self, payload: BaseTokenPayload, ttl: int) -> str:
        expire_dt = datetime.now() + timedelta(seconds=ttl)
        header = {"alg": "HS256", "typ": "JWT"}

        payload = TokenPayload(exp=expire_dt.timestamp(), **payload.model_dump())

        unsigned_token = self._base64url_encode(json.dumps(header)) + "." + self._base64url_encode(payload.model_dump_json())
        signature = self._generate_signature(unsigned_token)
        token = unsigned_token + "." + signature
        return token

    async def validate_token(self, db: AsyncSession, token: str, required_scope: List[Scope] = None) -> UserSchema:

        if not token:
            raise AuthorizationException(message="Unauthorized")

        if len(token.split(".")) != 3 or not self.is_signature_valid(token):
            raise AuthorizationException(message="Invalid token")

        token_payload = self.parse_token(token)
        now = datetime.now().timestamp()

        if token_payload.exp < now:
            raise AuthorizationException(message="Token expired")

        has_scope = any([scope_item in token_payload.scope for scope_item in required_scope]) if required_scope else True
        if not has_scope:
            raise AuthenticationException(message="Forbidden")

        if user := await UserRepository().read(db, query=UserReadQuery(email=token_payload.email)):
            return user
        raise AuthorizationException(message="No user with given token")

    def parse_token(self, token: str) -> TokenPayload:
        payload_segment = token.split(".")[1]
        payload_json = json.loads(self._base64url_decode(payload_segment))
        return TokenPayload(**payload_json)

    def _generate_signature(self, unsigned_token: str) -> str:
        signature = hmac.new(config.settings.SECRET_KEY.get_secret_value().encode(), unsigned_token.encode(), hashlib.sha256).hexdigest()
        return self._base64url_encode(signature)

    def is_signature_valid(self, token: str) -> bool:
        segments = token.split(".")

        unsigned_token = segments[0] + "." + segments[1]
        token_signature = segments[2]
        generated_signature = self._generate_signature(unsigned_token)

        return token_signature == generated_signature

    def _base64url_decode(self, input):
        return base64.urlsafe_b64decode(input)

    def _base64url_encode(self, input):
        bytes_str = input.encode('ascii')
        base64str = base64.urlsafe_b64encode(bytes_str).decode('utf-8')
        return base64str


def get_auth_service() -> AuthService:
    return AuthService()

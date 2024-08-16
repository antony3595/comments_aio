import base64
import hashlib
import hmac
import json
from datetime import datetime, timedelta
from typing import List

from fastapi import HTTPException

import conf
from repository.enums.scope import Scope
from repository.user import UserRepository
from schema.api.auth import TokenPayload, BaseTokenPayload
from schema.query.user import UserEmailQuery


class TokenService:
    def generate_token(self, payload: BaseTokenPayload, ttl: int) -> str:
        expire_dt = datetime.now() + timedelta(minutes=ttl)
        header = {"alg": "HS256", "typ": "JWT"}

        payload = TokenPayload(exp=expire_dt.timestamp(), **payload.model_dump())

        unsigned_token = self._base64url_encode(json.dumps(header)) + "." + self._base64url_encode(payload.model_dump_json())
        signature = self._generate_signature(unsigned_token)
        token = unsigned_token + "." + signature
        return token

    def validate_token(self, token: str, required_scope: List[Scope]):

        if not token:
            raise HTTPException(detail="Unauthorized", status_code=401)

        if not self.is_signature_valid(token):
            raise HTTPException(detail="Invalid token", status_code=401)

        payload = self.parse_token(token)
        now = datetime.now().timestamp()

        if payload.exp < now:
            raise HTTPException(detail="Token expired", status_code=401)

        has_scope = any([scope_item in payload.scope for scope_item in required_scope])
        if not has_scope:
            raise HTTPException(detail="Forbidden", status_code=403)

        if not UserRepository().read(query=UserEmailQuery(email=payload.email)):
            raise HTTPException(detail="No user with given token", status_code=403)

    def parse_token(self, token: str) -> TokenPayload:
        payload_segment = token.split(".")[1]
        payload_json = json.loads(self._base64url_decode(payload_segment))
        return TokenPayload(**payload_json)

    def _generate_signature(self, unsigned_token: str) -> str:
        signature = hmac.new(conf.SECRET_KEY.encode(), unsigned_token.encode(), hashlib.sha256).hexdigest()
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


def get_token_service() -> TokenService:
    return TokenService()

import requests
from jose import jwt, JWTError

from app.core.settings import settings
from app.domain.auth.ports import IAuthProvider
from app.domain.auth.rules import InvalidTokenError


class KeycloakProvider(IAuthProvider):
    def __init__(self):
        self.jwks_url = (
            f"{settings.keycloak_url}/realms/"
            f"{settings.keycloak_realm}/protocol/openid-connect/certs"
        )
        self.issuer = f"{settings.keycloak_url}/realms/{settings.keycloak_realm}"
        self.audience = settings.keycloak_frontend_client_id
        self.algorithms = ["RS256"]

        self.jwks = requests.get(self.jwks_url).json()

    def verify_token(self, token: str) -> dict:
        if not token or token == "undefined":
            raise InvalidTokenError("Token missing")

        try:
            payload = jwt.decode(
                token,
                self.jwks,
                algorithms=self.algorithms,
                audience=self.audience,
                issuer=self.issuer,
                options={"verify_at_hash": False},
            )
            return payload

        except JWTError as e:
            raise InvalidTokenError(f"Invalid or expired token: {str(e)}")

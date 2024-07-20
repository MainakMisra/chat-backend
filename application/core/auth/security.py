import datetime
import logging

from fastapi import Request, Response
from fastapi.security import HTTPBasic
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import (InvalidHeaderError, JWTDecodeError,
                                         MissingTokenError)
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from application.database.models.users import UserOrm
from application.routes.api.exceptions import UnauthorizedUserError


class SecurityService:
    def __init__(self, req: Request, res: Response):
        self.logger = logging.getLogger(__name__)
        self._req = req
        self._res = res
        self._headers = req.headers
        self._fastapi_jwt_auth = AuthJWT(req=req, res=res)
        self.token_renewal_required = None

    def verify_user(self, session: Session) -> None:

        self._fastapi_jwt_auth.jwt_refresh_token_required(auth_from="request")
        user_id = self._fastapi_jwt_auth.get_jwt_subject()

        try:
            session.query(UserOrm).filter_by(id=user_id).one()
        except NoResultFound:
            raise 404

    def authenticate(self, session: Session) -> str:
        """Verify the access auth token."""
        try:
            self._fastapi_jwt_auth.jwt_required(auth_from="request")
        except MissingTokenError:
            raise UnauthorizedUserError
        except InvalidHeaderError:
            raise UnauthorizedUserError
        except JWTDecodeError:
            self.renew_access_token()

        self.verify_user(session)

        access_token_subject = self._fastapi_jwt_auth.get_jwt_subject()

        return str(access_token_subject)

    def renew_access_token(self) -> None:
        """Generate new access token."""
        expiry_time = datetime.timedelta(minutes=15)

        try:
            self._fastapi_jwt_auth.jwt_refresh_token_required(auth_from="request")
        except InvalidHeaderError:
            raise UnauthorizedUserError

        encoded_userid = self._fastapi_jwt_auth.get_jwt_subject()

        new_access_token = self._fastapi_jwt_auth.create_access_token(
            subject=encoded_userid, algorithm="HS256", expires_time=expiry_time
        )
        self._fastapi_jwt_auth.set_access_cookies(new_access_token, self._res)

    def set_login_cookies(self, user_id: str) -> None:
        """Function to create the response for successful login."""
        expiry_time = datetime.timedelta(minutes=15)

        access_token = self._fastapi_jwt_auth.create_access_token(
            subject=user_id, algorithm="HS256", expires_time=expiry_time
        )
        refresh_token = self._fastapi_jwt_auth.create_refresh_token(subject=user_id, algorithm="HS256")

        # Set the JWT cookies in the response
        self._fastapi_jwt_auth.set_access_cookies(access_token, self._res)
        self._fastapi_jwt_auth.set_refresh_cookies(refresh_token, self._res)

    def remove_cookies(self) -> None:
        self._fastapi_jwt_auth.unset_jwt_cookies(self._res)


admin_security = HTTPBasic()

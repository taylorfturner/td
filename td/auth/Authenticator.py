import datetime as dt
import json
import os
from dataclasses import dataclass
from dataclasses import fields
from typing import Union

import requests
from dataclasses_json import dataclass_json

from td import project_root
from td.utils import get_logger

# from config import refresh_token_dummy, access_token_dummy

logger = get_logger()


@dataclass_json
@dataclass
class Token:
    """Token

    The Token class represents an OAuth Token

    Parameters
    ----------
    access_token : str
    expires_in : int
    refresh_token : str
    refresh_token_expires_in : int
    scope : str
    token_type : str
    created_at : int, optional
    soft_expiration_minutes : int, optional
    soft_expiration_days : int, optional

    """

    access_token: str
    expires_in: int
    refresh_token: str
    refresh_token_expires_in: int
    scope: str
    token_type: str
    created_at: Union[int, float] = dt.datetime.now().timestamp()
    soft_expiration_minutes: int = 2
    soft_expiration_days: int = 7

    @property
    def expires_at(self):
        """Returns the timestamp of the token expiration

        Returns
        --------
        timestamp
            The expiration timestamp
        """

        delta = dt.datetime.fromtimestamp(self.created_at) + dt.timedelta(
            seconds=self.expires_in
        )
        return delta.timestamp()

    @property
    def refresh_expires_at(self):
        """Returns the timestamp at which the refresh token expires

        Returns
        -------
        timestamp
            The timestamp
        """
        delta = dt.datetime.fromtimestamp(self.created_at) + dt.timedelta(
            seconds=self.refresh_token_expires_in
        )
        return delta.timestamp()

    @property
    def is_expired(self):
        """Returns True if the access token is expired

        Returns
        -------
        bool
            Whether or not the token is expired
        """
        delta = self.expires_at - dt.datetime.now().timestamp()
        return delta / 60 <= self.soft_expiration_minutes

    @property
    def is_refresh_expired(self):
        """Returns True if the access token is expired

        Returns
        -------
        bool
            Whether or not the token is expired
        """
        delta = self.refresh_expires_at - dt.datetime.now().timestamp()
        return (delta / 60 / 60) <= self.soft_expiration_days

    def refresh(self, **token):
        """Refresh self with a provided token"""
        self.access_token = token.get("access_token", self.access_token)
        self.refresh_token = token.get("refresh_token", self.refresh_token)
        self.created_at = dt.datetime.now().timestamp()

    def to_dict(self):
        """Returns a dictionary of class attributes

        A Token's representation is a dictionary.  This is useful JSON serialization

        Returns
        -------
        dict
            ``{[attribute]: value}``
        """
        return {field.name: self.__getattribute__(field.name) for field in fields(self)}

    def __str__(self):
        return f"""
        Token
        -----
            expires_in: {self.expires_in}
            refresh_token_expires_in: {self.refresh_token_expires_in}
            created_at: {self.created_at}
            expires_at: {self.expires_at}
            is_expired: {self.is_expired}
        """


class Authenticator:

    client_id: str = os.environ.get("TDA_CLIENT_ID")
    oauth_token_path: str = os.environ.get(
        "TDA_OAUTH_TOKEN_PATH", ".secrets/token.json"
    )
    token: Token = None

    def __init__(self):
        self.token = self.load_auth_tokens()

    def load_auth_tokens(self):
        """Reads a token from the provided ``oauth_token_path``

        Returns
        -------
        Token
            A Token object
        """
        with open(project_root() / self.oauth_token_path, "r") as f:
            return Token(**json.load(f))

    def write_auth_tokens(self):
        """
        Writes a new auth_tokens json file with new tokens. Encodes datetimes as strings with the
        specified formats from refresh/access_token_stamp.
        """

        with open(project_root() / self.oauth_token_path, "w") as f:
            json.dump(self.token.to_dict(), f, ensure_ascii=False, indent=4)

    def check_access_token(self):
        """
        Checks the number of minutes until the access token needs to be refreshed, and
        refreshes it if needed. Access tokens last for 30 minutes, and can be refreshed
        for a new token at any point within this 30-minute period. This function uses
        the "refresh_threshold" to set the number of minutes left before expiration to
        refresh the token.
        """

        if self.token.is_expired:
            logger.info("Access token expires, creating new token.")
            self.token.refresh(**self.get_access_token())
            self.write_auth_tokens()

    def check_refresh_token(self):
        """
        Checks the number of days until the refresh token needs to be refreshed, and
        refreshes it if needed. Refresh tokens last for 90 days, and can be refreshed
        for a new token at any point within this 90-day period. This function uses
        the "refresh_threshold" to set the number of days left before expiration to
        refresh the token.

        Once a new refresh token is generated, it is then saved to the tokens file.
        """
        if self.token.is_refresh_expired:
            logger.info("Refresh Token Expired")
            self.token.refresh(**self.get_refresh_token())
            self.write_auth_tokens()

    def get_refresh_token(self):
        """
        Makes an API post request to TD Ameritrade's server, requesting
        a new refresh token.

        Parameters
        ----------
        auth_tokens : dict
            Dictionary with "auth_info" as a key, containing a "refresh_token" argument.

        Returns
        -------
        dict
            Dictionary with the new refresh token
        """
        url = r"https://api.tdameritrade.com/v1/oauth2/token"

        auth_headers = {"Content-Type": "application/x-www-form-urlencoded"}

        params = {
            "grant_type": "refresh_token",
            "refresh_token": self.token.refresh_token,
            "access_type": "offline",
            "client_id": self.client_id,
        }

        content = requests.post(url=url, data=params)

        return content.json()

    def get_access_token(self):
        """
        Makes an API post request to TD Ameritrade's server, requesting
        a new access token.

        Parameters
        ----------
        auth_tokens : dict
            Dictionary with "auth_info" as a key, containing a "access_token" argument.

        Returns
        -------
        dict
            Dictionary with the new access token
        """
        url = r"https://api.tdameritrade.com/v1/oauth2/token"

        auth_headers = {"Content-Type": "application/x-www-form-urlencoded"}

        params = {
            "grant_type": "refresh_token",
            "refresh_token": self.token.refresh_token,
            "client_id": self.client_id,
        }

        content = requests.post(url=url, data=params)

        return content.json()

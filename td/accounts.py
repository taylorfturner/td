import requests
from td.authentication import Authenticator


class Accounts:
    def __init__(self):
        """
        __init__ [summary]

        [extended_summary]
        """
        self.endpoint = "https://api.tdameritrade.com/v1/accounts"


    def get(self, params={"fields": "positions"}):
        """
        get
        
        Get all the account(s) data from the TD Ameritrade API.

        :param params: API requests parameters, defaults to {"fields": "positions"}
        :type params: dict, optional
        :return: API response data. If successful, dictionary of all account positions.
        :rtype: json object dictionary
        """
        auth = Authenticator()

        header = {
            "Authorization": f"Bearer {auth.token.access_token}"
        }

        content = requests.get(
            url = self.endpoint,
            params = params,
            headers = header
        )

        data = content.json()

        return data


    def put(self):
        """
        put

        Write to a local store of data for historical position analysis.

        :raises NotImplementedError: [description]
        """
        raise NotImplementedError

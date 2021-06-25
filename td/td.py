import requests
from td.authentication import Authenticator


class TD:

    def __init__(self):
        """Test TD class init

        :return: [description]
        :rtype: [type]
        """
        self.endpoint = "https://api.tdameritrade.com/v1/accounts"


    def get(self, params={"fields": "positions"}):
        """
        Get all the account(s) data from the TD Ameritrade API.
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
        Write to a local store of data for historical position
        analysis.
        """
        raise NotImplementedError

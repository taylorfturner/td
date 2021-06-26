from datetime import date
import requests
import json
from td.auth import Authenticator


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

        if content.status_code != 200:
            auth.get_refresh_token()

        content = requests.get(
            url = self.endpoint,
            params = params,
            headers = header
        )

        self.data = content.json()

        return True


    def put(self):
        """
        put

        Write to a local store of data for historical position analysis.

        :raises NotImplementedError: [description]
        """
        
        today = date.today()
        current_date_string = today.__str__().replace("-", "_")


        write_data = json.dumps(self.data)

        with open(f"data/{current_date_string}.json", "w") as outfile:
            outfile.write(write_data)

        return True


    def run(self):
        """
        Execute both the get and put method sequentially 
        so that users can have one interaction point to run all
        necessary methods.
        """
        self.get()
        self.put()
        return True

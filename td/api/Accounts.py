from datetime import date
import requests
import pandas as pd
import json
from td.auth.Authenticator import Authenticator


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

    def process_data(self):
        
        account_meta_df = pd.DataFrame()
        position_df = pd.DataFrame()
        
        for iter_data in self.data:
            iter_data = iter_data["securitiesAccount"]

            # account meta data
            type = iter_data["type"]
            account_id = iter_data["accountId"]
            roundTrips = iter_data["roundTrips"]
            is_day_trader = iter_data["isDayTrader"]
            is_closing_only_restricted = iter_data["isClosingOnlyRestricted"]
            initial_balances = iter_data["initialBalances"]
            current_balances = iter_data["currentBalances"]
            projected_balance = iter_data["projectedBalances"]

            # account's position data
            positions = iter_data["positions"]
            for single_position in positions:
                instrument = single_position["instrument"]
                single_position.pop("instrument", None)
                single_position["symbol"] = instrument["symbol"]
                single_position["asset_type"] = instrument["assetType"]
                single_position["account_id"] = account_id

                single_position_list = list(single_position)

                if len(position_df) < 1:
                    position_df = position_df.from_dict(single_position, orient='columns')
                elif len(position_df) >= 1:
                    position_df = position_df.append(single_position_list)

            return account_meta_df, position_df

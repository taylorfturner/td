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
        get [summary]

        [extended_summary]

        :param params: [description], defaults to {"fields": "positions"}
        :type params: dict, optional
        :return: [description]
        :rtype: [type]
        """
        self.auth = Authenticator()

        header = {
            "Authorization": f"Bearer {self.auth.token.access_token}"
        }

        # TODO: handle errors, retry, and token refresh
        content = requests.get(
            url = self.endpoint,
            params = params,
            headers = header
        )

        self.data = content.json()

        self.account_meta_df, self.position_df = self.to_dataframe()



    def put(self):
        """
        put [summary]

        [extended_summary]

        :param account_df: [description]
        :type account_df: [type]
        :param position_df: [description]
        :type position_df: [type]
        """
        today = date.today()
        current_date_string = today.__str__().replace("-", "_")

        # TODO: move this to MySQL
        self.account_meta_df.to_csv(f"data/{current_date_string}_account_df.csv")
        self.position_df.to_csv(f"data/{current_date_string}_position_df.csv")

    def run(self):
        """
        Execute both the get and put method sequentially 
        so that users can have one interaction point to run all
        necessary methods.
        """
        self.get()
        self.put()


    def to_dataframe(self):
        """
        to_dataframe [summary]

        [extended_summary]

        :return: [description]
        :rtype: [type]
        """
        account_meta_df = pd.DataFrame()
        position_df = pd.DataFrame()
        
        for iter_data in self.data:
            iter_data = iter_data["securitiesAccount"]

            positions = iter_data["positions"]
            iter_data.pop("positions", None)

            # account meta data
            account_dict = {}
            for key in iter_data.keys():
                account_dict[key] = iter_data[key]
            account_meta_df = account_meta_df.append(account_dict, ignore_index=True)

            # account's position data
            for single_position in positions:
                instrument = single_position["instrument"]
                single_position.pop("instrument", None)
                for key in instrument.keys():
                    single_position[key] = instrument[key]

                position_df = position_df.append(single_position, ignore_index=True)

        return account_meta_df, position_df

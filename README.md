### td

A simple repository to query account level data from TD Ameritrade `accounts` API endpoint. The core code then processes that data on an account level and portfolio level such that a user can look at position-level exposures across all accounts on a percentage basis.


## Setup and Install
```python
conda create -n td python=3.8
conda activate td
cd td 
pip install -e .
```

Next for setting up the secrets and tokens for the API: 
- 1) Create a `.secrets` file in the root of this repo
- 2) Paste the following URL in your browser: ` https://auth.tdameritrade.com/auth?response_type=code&redirect_uri=https://127.0.0.1&client_id=<app_client_id>%40AMER.OAUTHAP`
- 3) Login using your TD account credentials
- 4) Copy everything in the returned url after the equal sign in `?code=<encoded_key>`
- 5) Decode that key using a URL decoder
- 6) Utilize the [Post Access Token api](https://developer.tdameritrade.com/authentication/apis/post/token-0) to retrieve a dictionary of tokens. The params you need to use are as follows:
```
grant_type: authorization_code
access_type: offline
code: <decoded_key_from_step_5>
client_id: <your_app_client_id>
redirect_url: https://127.0.0.1
```

## Credit 
- [Taylor Turner](https://github.com/taylorfturner)
- [HJCarey](https://github.com/HJCarey)
- [IVIyg0t](https://github.com/IVIyg0t)

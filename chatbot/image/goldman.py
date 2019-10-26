import requests
import json

auth_data = {
    "grant_type": "client_credentials",
    "client_id": "86092afbdb44404fa54b97442e7c8c6a",
    "client_secret": "bb640134957816330efd8adfaf150e30c5907c63d757169377573bc4dd259018",
    "scope": "read_product_data"
}

# create session instance
session = requests.Session()

auth_request = session.post(
    "https://idfs.gs.com/as/token.oauth2", data=auth_data)
access_token_dict = json.loads(auth_request.text)
print(access_token_dict)
access_token = access_token_dict["access_token"]

# update session headers with access token
session.headers.update({"Authorization": "Bearer " + access_token})

request_url = "https://api.marquee.gs.com/v1/data/USCANFPP_MINI/query"

request_query = {
    "where": {
        "gsid": ["75154", "193067", "194688", "902608", "85627"]
    },
    "startDate": "2017-01-15",
    "endDate": "2018-01-15"
}

request = session.post(url=request_url, json=request_query)
results = json.loads(request.text)

print(results)

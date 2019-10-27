import requests
import json
import random


# create session instance
session = requests.Session()


def get_gir_score(ticker, date):
    request_url = "https://api.marquee.gs.com/v1/data/USCANFPP_MINI/query"

    request_query = {
        "where": {
            "ticker": [ticker]
        },
        "startDate": date,
        "endDate": date
    }
    print(request_query)

    try:
        request = session.post(url=request_url, json=request_query)
        results = json.loads(request.text)
        if len(results['data']) > 0:
            return results['data'][0]['integratedScore']
        else:
            return 0
    except Exception:
        return 0

def get_coverage():
    request_url = "https://api.marquee.gs.com/v1/data/USCANFPP_MINI/coverage?limit=110"
    request = session.get(url=request_url)
    results = json.loads(request.text)["results"]
    request_url = "https://api.marquee.gs.com/v1/assets/data/query"
    req_parameter = {
        "where": {
            "gsid": [entry["gsid"] for entry in results]
        },
        "fields": ["ticker"],
        "limit": 10000
    }
    request = session.post(url=request_url, json=req_parameter)
    result = json.loads(request.text)["results"]

    return set([entry["ticker"] for entry in result])

def get_gs_decision(gir_score):
    if gir_score > 0.5:
        return 1
    else:
        return 0

def get_10_stocks():
    a = list(get_coverage())
    random.shuffle(a)
    return a[0:10]

def getStockRecommendation():
    auth_data = {
        "grant_type": "client_credentials",
        "client_id": "86092afbdb44404fa54b97442e7c8c6a",
        "client_secret":
        "bb640134957816330efd8adfaf150e30c5907c63d757169377573bc4dd259018",
        "scope": "read_product_data"
    }

    auth_request = session.post(
        "https://idfs.gs.com/as/token.oauth2", data=auth_data)
    access_token_dict = json.loads(auth_request.text)
    access_token = access_token_dict["access_token"]
    session.headers.update({"Authorization": "Bearer " + access_token})

    largest = 0
    largestTicker = 0
    for entry in get_10_stocks():
        gs = get_gir_score(entry, "2015-11-02")
        print(gs)
        if gs > largest:
            largest = gs
            largestTicker = entry
    return (largestTicker, largest)

def getSellRecommendation(tickers):
    auth_data = {
        "grant_type": "client_credentials",
        "client_id": "86092afbdb44404fa54b97442e7c8c6a",
        "client_secret":
        "bb640134957816330efd8adfaf150e30c5907c63d757169377573bc4dd259018",
        "scope": "read_product_data"
    }

    auth_request = session.post(
        "https://idfs.gs.com/as/token.oauth2", data=auth_data)
    access_token_dict = json.loads(auth_request.text)
    access_token = access_token_dict["access_token"]
    session.headers.update({"Authorization": "Bearer " + access_token})

    smallest = 1
    smallestTicker = ""
    for entry in tickers:
        if entry == "USD":
            continue
        gs = get_gir_score(entry, "2015-11-02")
        if gs < smallest:
            smallest = gs
            smallestTicker = entry
    return (smallestTicker, smallest)

import requests
import json
import math



url_oc      = "https://www.nseindia.com/option-chain"
url_bnf     = 'https://www.nseindia.com/api/option-chain-indices?symbol=BANKNIFTY'
url_nf      = 'https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY'
url_fnf     = "https://www.nseindia.com/api/option-chain-indices?symbol=FINNIFTY"
url_indices = "https://www.nseindia.com/api/allIndices"
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
           'accept-language': 'en,gu;q=0.9,hi;q=0.8',
           'accept-encoding': 'gzip, deflate, br'}


session = requests.Session()
r = session.get(url_oc, headers=headers, timeout=5)

def nearest_strike(x, gap):
    strike = int(math.ceil(float(x)/gap)*gap)
    return strike


def get_data(url):
    r = session.get(url, headers=headers, timeout=5)
    if r.status_code == 200:
        return r.text
    
def strike_price(iname):
    r = get_data(url_indices)
    data = json.loads(r)
    for index in data["data"]:
        if index["indexSymbol"] == "NIFTY 50":
            last_nf_tp = index["last"]
            nf_strike = nearest_strike(last_nf_tp, 50)
        if index["indexSymbol"] == "NIFTY BANK":
            last_bnf_tp = index["last"]
            bnf_strike = nearest_strike(last_bnf_tp, 100)
        if index["indexSymbol"] == "NIFTY FIN SERVICE":
            last_fnf_tp = index["last"]
            fnf_strike = nearest_strike(last_fnf_tp, 50)
    if iname == "nf":
        return nf_strike
    elif iname == "bnf":
        return bnf_strike
    elif iname == "fnf":
        return fnf_strike



def CE(url, stprice, step):
    max_oi = 0
    total_oi = 0
    r = get_data(url)
    data = json.loads(r)
    currentExpDate = data["records"]["expiryDates"][0]
    # print(currentExpDate)
    minstrike = stprice - (10*step)
    maxstrike = stprice + (10*step)
    for item in data["records"]["data"]:
        if item["expiryDate"] == currentExpDate:
            if item["strikePrice"] == minstrike and item["strikePrice"] <= maxstrike:
                total_oi = total_oi + int(item["CE"]["openInterest"])
                if item["CE"]["openInterest"] > max_oi:
                    max_oi = item["CE"]["openInterest"]
                    max_oi_strike = item["strikePrice"]
                minstrike = minstrike + step
    return currentExpDate, total_oi, max_oi_strike


                
def PE(url, stprice, step):
    max_oi = 0
    total_oi = 0
    r = get_data(url)
    data = json.loads(r)
    currentExpDate = data["records"]["expiryDates"][0]
    # print(currentExpDate)
    minstrike = stprice - (10*step)
    maxstrike = stprice + (10*step)
    for item in data["records"]["data"]:
        if item["expiryDate"] == currentExpDate:
            if item["strikePrice"] == minstrike and item["strikePrice"] <= maxstrike:
                total_oi = total_oi + int(item["PE"]["openInterest"])
                if item["PE"]["openInterest"] > max_oi:
                    max_oi = item["PE"]["openInterest"]
                    max_oi_strike = item["strikePrice"]
                minstrike = minstrike + step
    return currentExpDate, total_oi, max_oi_strike


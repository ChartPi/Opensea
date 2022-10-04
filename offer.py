import requests

url = "https://api.opensea.io/v2/orders/ethereum/seaport/offers"

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "X-API-KEY": "xxxxx"
}

payload = {
    "parameters": {
        "offerer": "xxxxx",
        "zone": "xxxxx",
        "zoneHash": "0x3000000000000000000000000000000000000000000000000000000000000000",
        "startTime": "1660827662",
        "endTime": "1660829458",
        "orderType": 2,
        "offer": [
                    {
                "itemType": 0,
                "token": "xxxxx",
                "identifierOrCriteria": "0",
                "startAmount": "3000000000000000",
                "endAmount": "3000000000000000",
            },
        ],
        "consideration": [
            {
                "itemType": 4,
                "token": "xxxxx",
                "identifierOrCriteria": "22994455249115322951562734013192789391166244015578527226297695587109102706827",
                "startAmount": "1",
                "endAmount": "1",
                "recipient": "xxxxx"
            },
            {
                "itemType": 1,
                "token": "xxxxx",
                "identifierOrCriteria": "0",
                "startAmount": "75000000000000",
                "endAmount": "75000000000000",
                "recipient": "xxxxx",
            },
            {
                "itemType": 1,
                "token": "xxxxx",
                "identifierOrCriteria": "0",
                "startAmount": "75000000000000", # Collection Fee
                "endAmount": "75000000000000",
                "recipient": "xxxxx",
            },
        ],
        "totalOriginalConsiderationItems": 2,
        "salt": 6918039068683632,
        "conduitKey": "xxxxx",
        "nonce": 0,
    }
}


response = requests.post(url, json=payload, headers=headers)

print(response.text)

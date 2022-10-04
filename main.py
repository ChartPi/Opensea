import requests
import pandas as pd
from datetime import datetime

now = datetime.now()
timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

collections_query = """
        SELECT * FROM `crypto-xxxxx.opensea.collections`
        """
collections = pd.read_gbq(collections_query, project_id='crypto-xxxxx')
floors = pd.DataFrame()

for index, collection in collections.iterrows():
    collection_name = collection['name']
    print(collection_name)
    collection_address = collection['id']
    asset_number = collection['floor_asset_id']
    url = "https://api.opensea.io/api/v1/collection/" + collection_name
    headers = {
        "Accept": "application/json",
        "X-API-KEY": "xxxxx"
    }
    r = requests.request("GET", url, headers=headers)
    response = r.json()
    # assets = assets['asset_events']

    floor = response['collection']['stats']['floor_price']
    fee = int(response['collection']['primary_asset_contracts'][0]['seller_fee_basis_points']) / 10000
    floor_minus_fee = floor * (1-fee)

    one_day_sales = response['collection']['stats']['one_day_sales']
    one_day_average_price = response['collection']['stats']['one_day_average_price']

    url = "https://api.opensea.io/api/v1/asset/"+collection_address+"/"+asset_number+"/offers"
    headers = {
        "Accept": "application/json",
        "X-API-KEY": "xxxxx"
    }
    r = requests.request("GET", url, headers=headers)
    response = r.json()

    offer_type = response['seaport_offers'][0]['order_type']
    offers = response['seaport_offers']
    df_offers = pd.DataFrame(offers)
    # print(df_offers)
    df_offers = df_offers.loc[df_offers['order_type'] == 'criteria']
    df_offers['type'] = df_offers['protocol_data'].map(lambda x : x['parameters']['offer'][0]['token'])
    df_offers = df_offers.loc[df_offers['type'] == '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2']
    df_offers['bid'] = df_offers['protocol_data'].map(lambda x: x['parameters']['offer'][0]['endAmount'])
    df_offers['bid'] = df_offers['bid'].astype('float') / 1000000000000000000
    df_offers = df_offers.sort_values(by=['bid'], ascending=False).reset_index(drop=True)
    # print(df_offers)

    max_offer = df_offers.iloc[0]['bid']
    # print(max_offer)
    potential_profit = floor_minus_fee - max_offer
    opportunity = potential_profit / max_offer * 100

    # print(timestamp, collection_name, floor, potential_profit, opportunity)
    #
    # print(floor)
    # print(fee)
    # print(floor_minus_fee)
    # print(max_offer)
    # print(potential_profit)
    # print(opportunity)

    row = pd.DataFrame({'collection_name': collection_name,
                        'collection_address': collection_address,
                        'timestamp':timestamp,
                        'floor': float(floor),
                        'fee':float(fee),
                        'floor_minus_fee':float(floor_minus_fee),
                        'max_offer':float(max_offer),
                        'potential_profit':float(potential_profit),
                        'opportunity':float(opportunity),
                        'one_day_sales':int(one_day_sales),
                        'one_day_average_price':float(one_day_average_price)
                        },
                       index=[0])
    floors = pd.concat([row, floors.loc[:]]).reset_index(drop=True)
    # print(floors)

# floors.to_gbq('opensea.collection_offers', project_id='crypto-xxxxx', if_exists='append')

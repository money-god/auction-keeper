#!/usr/bin/env python3
# Debt bidding model that reads auction state from stdin and writes a bid to stdout

import sys
import os
import json
import requests
from pyflex.deployment import GfDeployment
from pyflex.numeric import Wad, Ray, Rad
from web3 import Web3, HTTPProvider


def get_price():
    # Retrieve latest FLX price from coingecko
    resp = requests.get('https://api.coingecko.com/api/v3/simple/price', params={'ids': 'reflexer-ungovernance-token', 'vs_currencies': 'usd'})
    return resp.json()['reflexer-ungovernance-token']['usd']

"""
Sample auction input:
{'id': '9', 'bid_amount': '0.000000000000000000000000001000000000000000000', 'amount_to_sell': '0.500000000000000000', 'block_time': 1656444608, 'auction_deadline': 1656440892, 'price': '0.000000000000000000', 'bid_increase': '1.050000000000000000', 'high_bidder': '0x0000000000000000000000000000000000000000', 'staked_token_auction_house': '0x63e5455824F23e1a0d6157F4C6f400A782Ab9eF1'}
"""

current_flx_usd_price = get_price()
web3 = Web3(HTTPProvider(os.environ['ETH_RPC_URL']))
geb = GfDeployment.from_node(web3, 'rai')
redemption_price = geb.oracle_relayer.redemption_price()

#print(f"{current_flx_usd_price=}, {redemption_price=}")
# Determines FLX Price to bid
MAXIMUM_FLX_MULTIPLIER = 0.99  # Buy FLX for at most 90% of current price
MINIMUM_FLX_MULTIPLIER = 0.01  # Start bidding at 1% of current price

# Custom bid increase 
# The minimum auction bid increase can be low, setting a higher one can prevent too many bids
# If you want to always use the minimum bid increase allowed, set this to 0
MY_BID_INCREASE = 1.10

for auction_input in sys.stdin:
    auction_state = json.loads(auction_input)

    # If we are already the high bidder, do nothing
    if auction_state['high_bidder'] == os.environ['KEEPER_ADDRESS']:
        continue

    # Ensure our custom bid increase is at least the minimum allowed
    MY_BID_INCREASE = max(Wad.from_number(MY_BID_INCREASE), Wad.from_number(auction_state['bid_increase']))

    # Add slight amount to account for possible redemption price change between the time of model output and bid placement
    MY_BID_INCREASE += Wad.from_number(1e-4)

    # Bid price using `MY_BID_INCREASE`
    my_bid_amount = Wad.from_number(auction_state['bid_amount']) * MY_BID_INCREASE

    # Round up from Rad to Wad
    my_bid_price = Wad(Rad.from_number(my_bid_amount) * redemption_price / Rad(Wad.from_number(auction_state['amount_to_sell']))) + Wad(1)

    # Bid price using minimum bid increase allowed
    min_bid_amount = Wad.from_number(auction_state['bid_amount']) * Wad.from_number(auction_state['bid_increase'])
    min_bid_price =  Wad(Rad.from_number(min_bid_amount) * redemption_price / Rad(Wad.from_number(auction_state['amount_to_sell']))) + Wad(1)


    # round up to our minimum FLX price
    my_bid_price = max(my_bid_price, Wad.from_number(MINIMUM_FLX_MULTIPLIER * current_flx_usd_price))
    min_bid_price = max(min_bid_price, Wad.from_number(MINIMUM_FLX_MULTIPLIER * current_flx_usd_price))

    # Try our bid increase first
    # If price is too high, going above MAXIMUM_FLX_MULTIPLIER,  then try minimum bid increase
    if my_bid_price <= Wad.from_number(MAXIMUM_FLX_MULTIPLIER * current_flx_usd_price):
        #print(f"{my_bid_amount=}, {my_bid_price=}")
        bid = {'price': str(my_bid_price)}
        print(json.dumps(bid), flush=True)
    elif min_bid_price <= Wad.from_number(MAXIMUM_FLX_MULTIPLIER * current_flx_usd_price):
        #print(f"{min_bid_amount=}, {min_bid_price=}")
        bid = {'price': str(min_bid_price)}
        print(json.dumps(bid), flush=True)

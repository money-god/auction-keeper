#!/usr/bin/env python3

import sys
import os
import json

"""
Sample input:

{'id': '34', 'bid_amount': '0.003577998710342092', 'amount_to_sell': '5.000000000000000000000000000000000000000000000', 'block_time': 1651509840, 'auction_deadline': 1651764740, 'price': '4323.084918209392304591', 'bid_increase': '1.030000000000000000', 'high_bidder': '0x37918A209697488c3E4C25a8A7e7E21E5532ADFB', 'bid_expiry': '1651510724', 'surplus_auction_house': '0xCdaA2ec0975eD41202E1078b21a4833E414f6379'}
"""

CURRENT_FLX_USD_PRICE = 10000
REDEMPTION_PRICE = 3.01

# FLX Price to bid
STARTING_FLX_MULTIPLIER = 5.0 # Sell FLX for 500% of current price
MINIMUM_FLX_MULTIPLIER = 1.10 # Sell FLX for 110% of current price

for auction_input in sys.stdin:
    auction_state = json.loads(auction_input)

    print(auction_state, file=sys.stderr)
    # If we are already the high bidder, do nothing
    if auction_state['high_bidder'] == os.environ['ACCOUNT_ADDRESS']:
        continue

    # No bids yet, so bid with high, starting multiplier
    if float(auction_state['bid_amount']) == 0:
        bid = {'price': str(STARTING_FLX_MULTIPLIER * CURRENT_FLX_USD_PRICE)}
        print(json.dumps(bid), flush=True)
    else:
        # Must increase FLX amount by `bid_increase` amount
        new_bid_amount = float(auction_state['bid_amount']) * float(auction_state['bid_increase'])
        new_bid_price = float(auction_state['amount_to_sell']) * REDEMPTION_PRICE / new_bid_amount
        if new_bid_price >= MINIMUM_FLX_MULTIPLIER * CURRENT_FLX_USD_PRICE:
            bid = {'price': str(new_bid_price)}
            print(json.dumps(bid), flush=True)

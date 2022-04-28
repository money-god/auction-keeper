#!/usr/bin/env python3

import sys
import os
import json

# Example stdin input
"""
{"id": "6", "bid_amount": "0.000000000000000000", "amount_to_sell": "0.000000000000000000000000500000000000000000000", "block_time": 1651155568, "auction_deadline": 1651412740, "price": null, "bid_increase": "1.030000000000000000", "high_bidder": "0x6073E8FE874B53732b5DdD469a2De4047f33C64B", "surplus_auction_house": "0xCdaA2ec0975eD41202E1078b21a4833E414f6379"}
"""

# FLX Price to bid
MAX_BID_PRICE = 60
MIN_BID_PRICE = 0.00000000001

while True:
    for auction_state in sys.stdin:
        auction_state = json.loads(auction_state)

        # If we are already the high bidder, do nothing
        if auction_state['high_bidder'] == os.environ['ACCOUNT_ADDRESS']:
            continue

        # No bids yet
        if float(auction_state['bid_amount']) == 0:
            bid = {'price': str(MIN_BID_PRICE)}
            print(json.dumps(bid), flush=True)
        else:
            my_bid_price = float(auction_state['price']) * float(auction_state['bid_increase'])
            if my_bid_price <= MAX_BID_PRICE:
                bid = {'price': str(my_bid_price)}
                print(json.dumps(bid), flush=True)

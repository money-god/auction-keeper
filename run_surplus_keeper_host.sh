#!/bin/bash

ACCOUNT_ADDRESS=<KEEPER ADDRESS>
ETH_RPC_URL=<ETH RPC URL>
KEEPER_ADDRESS=<KEEPER ADDRESS>
KEYSTORE_FILE=<KEYSTORE FILE>
GAS_MAXIMUM=200

bin/auction-keeper \
     --type surplus \
     --model surplus_model.py \
     --rpc-uri ${ETH_RPC_URL} \
     --eth-from ${KEEPER_ADDRESS} \
     --eth-key "key_file=${KEYSTORE_FILE}" \
     --block-check-interval 90 \
     --bid-check-interval 30 \
     --min-auction 3 \
     --gas-maximum ${GAS_MAXIMUM}



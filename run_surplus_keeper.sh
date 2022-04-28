#!/bin/bash

KEEPER_ADDRESS=<KEEPER ADDRESS>
ETH_RPC_URL=<ETH RPC URL>

KEYSTORE_DIR=<FULL PATH OF KEYSTORE DIR>
KEYSTORE_FILE=<KEYSTORE FILE>
MODEL_DIR=<FULL PATH OF MODEL DIR>
MODEL_FILE=<MODEL FILE>

docker pull reflexer/auction-keeper:latest

docker run -it \
  -v ${KEYSTORE_DIR}:/keystore \
  -v ${MODEL_DIR}:/models \
  --env ACCOUNT_ADDRESS=${KEEPER_ADDRESS} \
    reflexer/auction-keeper:latest \
        --type surplus \
        --model /models/${MODEL_FILE} \
        --rpc-uri ${ETH_RPC_URL} \
        --eth-from ${KEEPER_ADDRESS} \
        --eth-key "key_file=/keystore/${KEYSTORE_FILE}" \
        --block-check-interval 30 \
        --bid-check-interval 30 \

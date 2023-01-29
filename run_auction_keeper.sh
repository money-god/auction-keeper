#!/bin/bash

docker run -it \
	-v /Users/peakaw/keys:/keystore \
	peakaw/auction-keeper \
        --rpc-uri <ETH_RPC> \
        --eth-from <KEEPER ADDRESS> \
        --eth-key "key_file=/keystore/<KEYSTORE FILE>" \
        --safe-engine-system-coin-target ALL \
        --keep-system-coin-in-safe-engine-on-exit \
        --keep-collateral-in-safe-engine-on-exit \
        --block-check-interval 1 \
        --bid-only \
        --bid-check-interval 4 \
        --graph-endpoints https://subgraph-goerli.tai.money/subgraphs/name/tai

#!/bin/bash

docker run -it \
	-v /Users/peakaw/keys:/keystore \
	peakaw/auction-keeper \
        --rpc-uri https://goerli.infura.io/v3/f674e7ddb53f46a6b10ec1762339b245 \
        --eth-from 0xFfBcA64C28FA16C81755d1A2833eB0D0ca025EFF \
        --eth-key "key_file=/keystore/keeper_keystore.json" \
        --safe-engine-system-coin-target ALL \
        --keep-system-coin-in-safe-engine-on-exit \
        --keep-collateral-in-safe-engine-on-exit \
        --block-check-interval 1 \
        --collateral-type WSTETH-B \
        --bid-check-interval 4 \
        --graph-endpoints https://subgraph-goerli.tai.money/subgraphs/name/tai
        #--bid-only \


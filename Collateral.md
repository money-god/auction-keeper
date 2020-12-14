# Running a collateral keeper

## Quickstart:

### 1) Get RAI

Buy RAI from [Uniswap v2](https://info.uniswap.org/pair/0xEBdE9F61e34B7aC5aAE5A4170E964eA85988008C) or 
[open a SAFE](https://app.gitbook.com/@reflexer-labs/s/geb/pyflex/safe-management/opening-a-safe) and generate it.

### 2\) Create the keeper run file.

Create a file called  `run_auction_keeper.sh` and paste the following code in it:

```text
#!/bin/bash

docker run -it \
	-v <KEYSTORE DIR>:/keystore \
	reflexer/auction-keeper:prai-demo \
        --rpc-uri <ETH_RPC_URL> \
        --eth-from <KEEPER ADDRESS> \
        --eth-key "key_file=/keystore/<KEYSTORE FILE>"
        
```

#### Then, substitute the following variables:

`KEYSTORE_DIR` - this must be the local directory where your keystore file is.

`KEYSTORE_FILE` Your Ethereum UTC JSON wallet.

For more information about this keystore format and how to generate them:

* [Ethereum UTC / JSON Wallet Encryption](https://wizardforcel.gitbooks.io/practical-cryptography-for-developers-book/content/symmetric-key-ciphers/ethereum-wallet-encryption.html)

* [keythereum](https://github.com/ethereumjs/keythereum)

`ETH_RPC_URL` - this is the URL of ethereum RPC connection

`KEEPER_ADDRESS` - this is your keeper's address. It should be in checksummed format, not lowercase

### 3\) Make the keeper script runnable

`chmod +x run_auction_keeper.sh`

### 4\) Run the keeper

`./run_auction_keeper.sh`

```text
$ ./run_auction_keeper.sh
Using default tag: latest
latest: Pulling from reflexer/auction-keeper
Digest: sha256:5d75a47028a0867b618b568269d985ac4a68ea8c63a920ac18093db3c3064134
Status: Image is up to date for reflexer/auction-keeper:latest
docker.io/reflexer/auction-keeper:latest
Password for /keystore/key.json: 
```

### 5\) Enter your keystore file password

**NOTE**: If using the Infura free-tier and you wish to stay under the 100k requests/day quota, add `--block-check-interval 10` and `--bid-check-interval 180` to `run_auction_keeper.sh`. However, this will make your keeper slower in responding to collateral auctions.



# Usage

Run `bin/auction-keeper -h` without arguments to see an up-to-date list of arguments and usage information.

## General
`--type collateral|surplus|debt`
  A keeper can only participate in one type of auction

`--collateral-type NAME`
  If `--type=collateral` is passed, the collateral_type must also be provided. A keeper can only bid on a single collateral type.
  Note: Currently, only the `ETH-A` collateral type is used.

`--eth-from ADDRESS`
  Address of the keeper.
  Warnings: **Do not use the same `eth-from` account on multiple keepers** as it complicates `SAFEEngine` inventory management and
  will likely cause nonce conflicts.  Using an `eth-from` account with an open SAFE is also discouraged.

`--rpc-host HOST`
   URI of ETH JSON-RPC node.
   Default `"http://localhost:8545"`

`--rpc-timeout SECS`
   Default `10`

   This keeper connects to the Ethereum network using [Web3.py](https://github.com/ethereum/web3.py) and interacts with
   the GEB using [pyflex](https://github.com/reflexer-labs/pyflex).  A connection to an Ethereum node
   (`--rpc-host`) is required.  [Parity](https://www.parity.io/ethereum/) and [Geth](https://geth.ethereum.org/) nodes are
   supported over HTTP. Websocket endpoints are not supported by `pyflex`.  A _full_ or _archive_ node is required;
   _light_ nodes are not supported.

   If you don't wish to run your own Ethereum node, third-party providers are available.  This software has been tested
   with [ChainSafe](https://chainsafe.io/) and [QuikNode](https://v2.quiknode.io/). Infura is incompatible, however, because
   it does not support the `eth_sendTransaction` RPC method which is used in pyflex.

## Gas price strategies

The following options determine the keeper's gas strategy and are mutually exclusive:

`--ethgasstation-api-key MY_API_KEY`
    Use [ethgasstation.info](https://ethgasstation.info) for gas prices

`--etherchain-gas-price`
    Use [etherchain.org](https://etherchain.org) for gas prices

 `--fixed-gas-price GWEI`
    Use a fixed gas price in GWEI

 If none of these options is given or the gas API produces not result, the keeper will use gas price from your node.

## Other gas options

`--gas-initial-multiplier MULTIPLIER`
   When using an API source for initial gas price, tunes initial gas price.
   Ignored when using `--fixed-gas-price` or no strategy is given
   default `1.0`

`--gas-reactive-multiplier MULTIPLIER`
   Every 30 seconds, a transaction's gas price will be multiplied by this value until it is mined or `--gas-maxiumum` is reached.
   Not used if `gasPrice` is passed from your bidding model.
   Note: [Parity](https://wiki.parity.io/Transactions-Queue#dropping-conditions), as of this writing, requires a
         minimum gas increase of `1.125` to propagate transaction replacement; this should be treated as a minimum
         value unless you want replacements to happen less frequently than 30 seconds (2+ blocks).
   default `1.125`

`--gas-maximum GWEI`
   Maximum value for gas price

## Accounting options

By default the keeper `join`s system coins to `SAFEEngine` on startup and `exit`s system coin and collateral upon shutdown.
The keeper provides facilities for managing `SAFEEngine` balances, which may be turned off to manage manually.

`--keep-system-coin-in-safe-engine-on-exit`
   Do not `exit` system coin on shutdown

`--keep-collateral-in-safe-engine-on-exit`
   Do not `exit` collateral on shutdown

`--return-collateral-interval SECS`
   Interval to `exit` won collateral to auction-keeper. Pass `0` to disable completely.
   default `300`

`--safe-engine-system-coin-target  ALL|<integer>`
   Amount of system-coin the keeper will try to keep in the `SAFEEngine` through rebalancing with `join`s and `exit`s.
   By default, there is no target.

  Rebalance Notes:
    Rebalances do not account for system coins moved from the `SAFEEngine` to an auction contract for an active bid.  
    System coins are rebalanced per `--safe-engine-system-coin-target` when:
       - The keeper starts up
       - `SAFEEngine` balance is insufficient to place a bid
       - An auction is settled

     To avoid transaction spamming, small "dusty" system coins balances will be ignored (until the keeper exits, if so configured).

## Managing resources

### Retrieving SAFEs

To start collateral auctions, the keeper needs a list of SAFEs and the collateralization ratio of each safe. There are two ways to retrieve the list of SAFEs:

`--from-block BLOCK_NUMBER`
   Scrape the chain for `ModifySAFECollateralization` events, starting at `BLOCK_NUMBER`
   Set this to the block where the first safe was created. After startup, only new blocks will be queried.
   NOTE: This can take significant time as the system matures.
   NOTE: To manage performance for debt auctions, periodically adjust `--from-block` to the block where the first liquidation
   which has not been `popDebtFromQueue`.

 `--subgraph-endpoints NODE1,NODE2`
   Comma-delimited list of [Graph](https://thegraph.com) endpoints to retrieve `ModifySAFECollateralization` events.
   If multiple endpoints are specified, they will be tried in order if a communication failure occurs.
   NOTE: Currently only supported for collateral auctions
   Example with current Reflexer Graph endpoints:
   `--graph-endpoints https://api.thegraph.com/subgraphs/name/reflexer-labs/prai-mainnet,https://subgraph.reflexer.finance/subgraphs/name/reflexer-labs/prai`

### Auctions

`--min-auction AUCTION_ID`
   Ignore auctions older than `AUCTION_ID`

`--max-auctions NUMBER` a
   Limit the number of bidding models created to handle active auctions.  

 Both switches help reduce the number of _requests_ (not just transactions) made to the node.

### Sharding/Settling

Bid management can be sharded across multiple keepers by **auction id**.  If you proceed with sharding, set these options:

`--shards NUMBER_OF_KEEPER`
   Number of keepers you will run. Set on all keepers

`--shard-id SHARD_ID`
   Set on each keeper, counting from 0.  
   For example, to configure three keepers, set `--shards 3` and assign `--shard-id 0`, `--shard-id 1`, `--shard-id 2`
   for the three keepers.  
   Note: **Auction starts are not sharded**. For an auction contract, only one keeper should be configured to `startAuction`.

If you are sharding across multiple accounts, you may wish to have another account handle all your `settleAuction`s.

`--settle-for <ACCOUNT1 ACCOUNT2>|NONE|ALL`
   Space-delimited list of accounts for which keeper will settle auctions or `NONE` to disable. If you'd like to donate your gas
to settle auctions for all participants, `ALL` is also supported.  
   Note: **Auction settlements are sharded**, so remove sharding configuration if running a dedicated auction settlement keeper.

### Transaction management

`--bid-delay FLOAT`

   Too many pending transactions can fill up the transaction queue, causing a subsequent transaction to be dropped.  By
   waiting a small `--bid-delay` after each bid, multiple transactions can be submitted asynchronously while still
   allowing some time for older transactions to complete, freeing up the queue.  Many parameters determine the appropriate
   amount of time to wait.  For illustration purposes, assume the queue can hold 12 transactions, and gas prices are
   reasonable.  In this environment, a bid delay of 1.2 seconds might provide ample time for transactions at the front of
   the queue to complete.  [Etherscan.io](etherscan.io) can be used to view your account's pending transaction queue.

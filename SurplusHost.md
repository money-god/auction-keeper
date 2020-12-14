# Running a Surplus Auction Keeper on a Host(not available on PRAI Demo)

## 1) Get FLX

## 2) Pick a RAI/FLX price and paste the following code into `debt_model.sh`. 

```
#!/usr/bin/env bash
while true; do
  echo "{\"price\": \"325.0\"}"
  sleep 120                   
done
```
For more information about bidding models, see [here](./BiddingModels.md)

## 3) Create the keeper run file.

Create a file called  `run_auction_keeper.sh` and paste the following code in it:

```text
#!/bin/bash
bin/auction-keeper \
    --type surplus \
     --model ./debt_model.sh \
     --rpc-uri <ETH_RPC_URL> \
     --eth-from <KEEPER_ADDRESS> \
     --eth-key "key_file=<KEYSTORE_FILE>"       
```

### Then, substitute the following variables:

`ETH_RPC_URL` - The URL of ethereum RPC connection

`KEEPER_ADDRESS` - The keeper's address. It should be in checksummed format(not lowercase).

`KEYSTORE_FILE` - Your Ethereum UTC JSON keystore filename

For more information about this keystore format and how to generate them:

* [Ethereum UTC / JSON Wallet Encryption](https://wizardforcel.gitbooks.io/practical-cryptography-for-developers-book/content/symmetric-key-ciphers/ethereum-wallet-encryption.html)

* [keythereum](https://github.com/ethereumjs/keythereum)


## 4) Make the keeper script runnable

`chmod +x run_auction_keeper.sh`

## 5) Start the keeper and enter your keystore file password

`./run_auction_keeper.sh`

```text
$ ./run_auction_keeper.sh
Password for /keystore/key.json: 
```

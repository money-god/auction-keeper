# Running a collateral keeper

## 1) Get RAI

Buy RAI from [Uniswap v2](https://info.uniswap.org/pair/0xEBdE9F61e34B7aC5aAE5A4170E964eA85988008C) or 
[open a SAFE](https://app.gitbook.com/@reflexer-labs/s/geb/pyflex/safe-management/opening-a-safe) and generate it.

## 2) Create the keeper run file.

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

### Then, substitute the following variables:

`KEYSTORE_DIR` - this must be the local directory where your keystore file is.

`KEYSTORE_FILE` - Your Ethereum UTC JSON keystore filename

For more information about this keystore format and how to generate them:

* [Ethereum UTC / JSON Wallet Encryption](https://wizardforcel.gitbooks.io/practical-cryptography-for-developers-book/content/symmetric-key-ciphers/ethereum-wallet-encryption.html)

* [keythereum](https://github.com/ethereumjs/keythereum)

`ETH_RPC_URL` - this is the URL of ethereum RPC connection

`KEEPER_ADDRESS` - this is your keeper's address. It should be in checksummed format, not lowercase

## 3) Make the keeper script runnable

`chmod +x run_auction_keeper.sh`

## 4\) Run the keeper

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

## 5) Enter your keystore file password

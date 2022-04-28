---
description: Running a surplus auction-keeper on a host
---

# Running on a Host

{% hint style="info" %}
In order to participate in surplus auctions you need to bid with protocol tokens
{% endhint %}

## Prerequisties

Python 3.6+

### Clone_**:**_

```text
git clone https://github.com/reflexer-labs/auction-keeper.git
cd auction-keeper
git submodule update --init --recursive
```

### Install:

This creates a virtual environment and installs requirements:

`./install.sh`

## 1\) Start virtualenv

`source _virtualenv/bin/activate`

## 2\) Modify model file as needed

A basic surplus auction bidding model can be found in `models/surplus_model.py`. It can be modifed to change `MAX_BID_PRICE` or fetch the latest protocol token price from an external source. 

### Then:

`chmod +x surplus_model.py`

For more information about bidding models, see [Bidding Models](../BiddingModels.md)

## 3\) Create the keeper run file

Create a file called `run_surplus_keeper.sh` and paste the following code in it:

```text
#!/bin/bash
bin/auction-keeper \
     --type surplus \
     --model surplus_model.py \
     --rpc-uri <ETH_RPC_URL> \
     --eth-from <KEEPER_ADDRESS> \
     --eth-key key_file=<KEYSTORE_FILE> \
     --block-check-interval 30 \
     --bid-check-interval 30

```

Modify the following variables in `run_surplus_keeper.sh`

`ETH_RPC_URL` - the URL of your ethereum RPC connection

`KEEPER_ADDRESS` - the keeper's address. It should be in checksummed format \(not lowercase\).

`KEYSTORE_FILE` - your Ethereum UTC JSON keystore filename

For more information about this keystore format and how to generate them, check:

* [Ethereum UTC / JSON Wallet Encryption](https://wizardforcel.gitbooks.io/practical-cryptography-for-developers-book/content/symmetric-key-ciphers/ethereum-wallet-encryption.html)
* [keythereum](https://github.com/ethereumjs/keythereum)

### Ensure script is executable

`chmod +x run_surplus_keeper.sh`

## 4\) Start the keeper and enter your keystore file password

`./run_surplus_keeper.sh`

```text
$ ./run_surplus_keeper.sh
Password for /keystore/key.json:
```

## Surplus Auctioning Process

[Surplus Auctioning Process](surplus-auctions.md)

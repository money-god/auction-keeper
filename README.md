# auction-keeper

[![Build Status](https://travis-ci.org/reflexer-labs/auction-keeper.svg?branch=master)](https://travis-ci.org/reflexer-labs/auction-keeper)
[![codecov](https://codecov.io/gh/reflexer-labs/auction-keeper/branch/master/graph/badge.svg)](https://codecov.io/gh/reflexer-labs/auction-keeper)

## Overview
`auction-keeper` participates in collateral, surplus and debt auctions by directly interacting with auction contracts deployed to the Ethereum blockchain.

## Responsibilities

The keeper is responsible with:

1) Monitoring all active auctions
2) Starting new auctions
2) Discovering new auctions
3) Ensuring a bidding model is running for each active auction
4) Passing auction status to each bidding model
5) Processing each bidding model output and submitting bids



## Architecture

`auction-keeper` can read an auction's status diretly from the Ethereum blockchain or a [Graph](https://thegraph.com/) node. Its unique feature is the ability to plug in external _bidding models_ which tell the keeper when and how much to bid. Bid prices are received from separate _bidding models_.

_Bidding models_ are simple processes that can be implemented in any programming language. They only need to pass JSON objects to and from `auction-keeper`. The simplest example of a bidding model is a shell script which echoes a fixed price. Read more about bidding models [here.](./BiddingModels.md)


For every new block, all auctions from `1` to `auctionsStarted` are checked for active status.
If a new auction is detected, a new bidding model is started.

**NOTE**: _Bidding models_ are only used for surplus and debt auctions, not collateral auctions.

## Running an auction keeper
Follow these links for details on running each type of keeper.

* [Collateral](./Collateral.md)

* [Surplus](./Surplus.md)

* [Debt](./Debt.md)

## Limitations

* If an auction started before the keeper was started, this keeper will not participate in it until the next block
is mined.
* This keeper does not explicitly handle global settlement, and may submit transactions which fail during shutdown.
* Some keeper functions incur gas fees regardless of whether a bid is submitted.  This includes, but is not limited to,
the following actions:
  * submitting approvals
  * adjusting the balance of surplus to debt
  * queuing debt for auction
  * liquidating a SAFE or starting a surplus or debt auction
* The keeper does not check model prices until an auction exists.  When configured to create new auctions, it will
`liquidateSAFE`, start a new surplus or debt auction in response to opportunities regardless of whether or not your RAI or
protocol token balance is sufficient to participate.  This too imposes a gas fee.
* Liquidating SAFEs to start new collateral auctions is an expensive operation.  To do so without a subgraph
subscription, the keeper initializes a cache of safe state by scraping event logs from the chain.  The keeper will then
continuously refresh safe state to detect undercollateralized SAFEs.
   * Despite batching log queries into multiple requests, Geth nodes are generally unable to initialize the safe state
   cache in a reasonable amount of time.  As such, Geth is not recommended for liquidating SAFEs.
   * To manage resources, it is recommended to run separate keepers using separate accounts to liquidate (`--start-auctions-only`)
   and bid (`--bid-only`).

For some known Ubuntu and macOS issues see the [pyflex](https://github.com/reflexer-labs/pyflex) README.


## Testing

This project uses [pytest](https://docs.pytest.org/en/latest/) for unit testing. Testing depends upon a dockerized local testchain included in `lib\pyflex\tests\config`.

In order to be able to run tests:
```
git clone https://github.com/reflexer-labs/auction-keeper.git
git checkout tags/prai-demo
cd auction-keeper
git submodule update --init --recursive
./install.sh
source _virtualenv/bin/activate
pip3 install -r requirements-dev.txt
```

You can then run all tests with:
```
./test.sh
```

## Support

<https://discord.gg/kB4vcYs>

## License

See [COPYING](https://github.com/makerdao/auction-keeper/blob/master/COPYING) file.

### Disclaimer

YOU (MEANING ANY INDIVIDUAL OR ENTITY ACCESSING, USING OR BOTH THE SOFTWARE INCLUDED IN THIS GITHUB REPOSITORY) EXPRESSLY UNDERSTAND AND AGREE THAT YOUR USE OF THE SOFTWARE IS AT YOUR SOLE RISK.
THE SOFTWARE IN THIS GITHUB REPOSITORY IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
YOU RELEASE AUTHORS OR COPYRIGHT HOLDERS FROM ALL LIABILITY FOR YOU HAVING ACQUIRED OR NOT ACQUIRED CONTENT IN THIS GITHUB REPOSITORY. THE AUTHORS OR COPYRIGHT HOLDERS MAKE NO REPRESENTATIONS CONCERNING ANY CONTENT CONTAINED IN OR ACCESSED THROUGH THE SERVICE, AND THE AUTHORS OR COPYRIGHT HOLDERS WILL NOT BE RESPONSIBLE OR LIABLE FOR THE ACCURACY, COPYRIGHT COMPLIANCE, LEGALITY OR DECENCY OF MATERIAL CONTAINED IN OR ACCESSED THROUGH THIS GITHUB REPOSITORY.

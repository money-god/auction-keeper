# auction-keeper

[![Build Status](https://travis-ci.org/reflexer-labs/auction-keeper.svg?branch=master)](https://travis-ci.org/reflexer-labs/auction-keeper)
[![codecov](https://codecov.io/gh/reflexer-labs/auction-keeper/branch/master/graph/badge.svg)](https://codecov.io/gh/reflexer-labs/auction-keeper)

The purpose of `auction-keeper` is to:
 * Start new auctions
 * Detect currently ongoing auctions
 * Bid on auctions

`auction-keeper` can participate in collateral, surplus and debt auctions. It can read an auction's status from an Ethereum or a [Graph](https://thegraph.com/) node. Its unique feature is the ability to plug in external _bidding models_ which tell the keeper when and how much to bid.

The keeper can be safely left running in the background. The moment it notices or starts a new auction, it will spawn a new instance of a _bidding model_ and then act according to its instructions. _Bidding models_ will be automatically terminated by the keeper the moment the auction expires.  The keeper can also settle expired auctions (in the case of English auctions).

**NOTE**: _Bidding models_ are only used for surplus and debt auctions, not collateral auctions.

## Running an auction keeper
Follow these links for details on running each type of keeper.
[collateral](./Collateral.md)
[Surplus](./Surplus.md)
[Debt](./Debt.md)

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

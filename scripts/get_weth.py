from brownie import interface

# this tells Python that there are packages in here that we can do stuff with
def get_weth(account):
    print("Getting WETH...")
    # ABI and Address needed to call this
    # how do you get ABI? 
    weth = interface.IWeth("0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2")
    tx = weth.deposit({"from": account, "value": 0.1 * 1e18})
    tx.wait(1)
    print("Get 0.1 WETH")
    # We're gonna use get_weth to get some WETH so that we can deposit it to Aave
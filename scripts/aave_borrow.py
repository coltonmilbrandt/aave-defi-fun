# Brownie comes with some stuff built in on local chain
# docs.aave.com for Aave docs

from brownie import accounts, config, interface, network
from scripts.get_weth import get_weth
from web3 import Web3

# What is a forked chain?
# we are going to point to a real chain, and make transaction
# as if it were a real chain, but we are just going to simulate txs
# we are going to simulate them on a local chain (Ganache)
# when we send the txs they will be sent AS IF to a main net
# that means we can use main net addresses

def main():
    # Deposit Money
    # The account that is going to call the function
    
    # this retrieves the first account that brownie made for us
    # then prints the account that we retrieved
    account = accounts[0]
    # WETH stands for Wrapped Ether
    # WETH allows us to use ETH as if it were an ERC20
    # We are using the main net address, but it doesn't matter because we are using a forked blockchain
    erc20_address = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
    # Approve the WETH token to be deposited to Aave
    get_weth(account)
    print("Getting WETH")
    # You ALWAYS need the ABI + address to call a function
    # Before we can approve, we should get some WETH
    lending_pool = get_lending_pool()
    amount = Web3.toWei(0.1, "ether")
    approve_erc20(amount, lending_pool.address, erc20_address, account)
    print("Depositing...")
    tx = lending_pool.deposit(
        erc20_address, amount, account.address, 0, {"from":account}
    )
    tx.wait(1)
    print("Done with deposit!")
    # Let's Borrow!
    avail_to_borrow = get_borrowable_data(lending_pool, account)
    # We need to find out how DAI we can borrow in terms of ETH
    print(f"WETH Price is: {get_asset_price()}")

def get_lending_pool():
    lending_pool_address_provider_address = "0xB53C1a33016B2DC2fF3653530bfF1848a515c8c5"
    lending_pool_address_provider = interface.ILendingPoolAddressesProvider(
        lending_pool_address_provider_address
    ) 
    lending_pool_address = lending_pool_address_provider.getLendingPool()
    lending_pool = interface.ILendingPool(lending_pool_address)
    return lending_pool

def approve_erc20(amount, lending_pool_address, erc20_address, account):
    print("Approving ERC20...")
    erc20 = interface.IERC20(erc20_address)
    tx = erc20.approve(lending_pool_address, amount, {"from": account})
    tx.wait(1)
    print("Approved!")

def get_borrowable_data(lending_pool, account):
    (
        total_collateral_eth,
        total_debt_eth,
        available_borrow_eth,
        current_liquidation_threshold,
        tlv,
        health_factor,
    ) = lending_pool.getUserAccountData(account.address)
    total_collateral_human_readable = Web3.fromWei(total_collateral_eth, "ether")
    available_borrow_human_readable = Web3.fromWei(available_borrow_eth, "ether") 
    total_debt_eth_human_readable = Web3.fromWei(total_debt_eth, "ether") 
    print(f"You have {total_collateral_human_readable} ETH in collateral")
    print(f"You have {available_borrow_human_readable} ETH available to borrow")
    print(f"You have {total_debt_eth_human_readable} ETH borrowed")
    return float(available_borrow_eth)

def get_asset_price():
    dai_eth_price_feed = interface.AggregatorV3Interface(
        config["networks"][network.show_active()]["dai_eth_price_feed"]
    )
    latest_price = Web3.fromWei(dai_eth_price_feed.latestRoundData()[1], "ether")
    print(f"The DAI/ETH price is {latest_price}")
    return float(latest_price)

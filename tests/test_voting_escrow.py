from brownie import accounts, ERC20, VotingEscrow
from web3 import Web3
from datetime import datetime
from dateutil.relativedelta import relativedelta


def test_deploy():
    account_deployer = accounts[0]
    account_staker1 = accounts[1]
    account_staker2 = accounts[2]

    staker1_initial_balance = Web3.toWei(100, 'ether')
    staker2_initial_balance = Web3.toWei(200, 'ether')

    token_name = 'Ocean token'
    token_symbol = 'OCEAN'
    token_decimals = 18
    total_supply = 1_000_000

    # deploy smart contracts
    erc20 = ERC20.deploy(token_name, token_symbol, token_decimals, total_supply, {
                         'from': account_deployer})
    voting_escrow = VotingEscrow.deploy(erc20, {'from': account_deployer})

    # check that the contract was deployed
    assert voting_escrow

    # check initial balances
    assert erc20.balanceOf(account_deployer) == Web3.toWei(
        total_supply, 'ether')
    assert erc20.balanceOf(account_staker1) == 0
    assert erc20.balanceOf(account_staker2) == 0

    erc20.transfer(account_staker1, staker1_initial_balance,
                   {'from': account_deployer})
    erc20.transfer(account_staker2, staker2_initial_balance,
                   {'from': account_deployer})

    assert erc20.balanceOf(account_deployer) == Web3.toWei(
        total_supply, 'ether') - staker1_initial_balance - staker2_initial_balance
    assert erc20.balanceOf(account_staker1) == staker1_initial_balance
    assert erc20.balanceOf(account_staker2) == staker2_initial_balance

    # deposit_for()
    # create_lock()
    # increase_amount()
    # increase_unlock_time()
    # withdraw()

    assert voting_escrow.get_last_user_slope(account_staker1) == 0
    assert voting_escrow.user_point_history__ts(account_staker1, 0) == 0
    assert voting_escrow.locked__end(account_staker1) == 0
    assert voting_escrow.balanceOf(account_staker1) == 0
    assert voting_escrow.totalSupply() == 0

    erc20.approve(voting_escrow, Web3.toWei(1, 'ether'), {'from': account_staker1})
    voting_escrow.create_lock(
        Web3.toWei(1, 'ether'),
        int((datetime.now() + relativedelta(years = 1)).strftime('%s')),
        {'from': account_staker1}
    )

    print(f"get_last_user_slope: {voting_escrow.get_last_user_slope(account_staker1)}")
    print(f"user_point_history__ts: {voting_escrow.user_point_history__ts(account_staker1, 0)}")
    print(f"locked__end: {voting_escrow.locked__end(account_staker1)}")
    print(f"balanceOf: {voting_escrow.balanceOf(account_staker1)}")
    print(f"totalSupply: {voting_escrow.totalSupply()}")

    assert False

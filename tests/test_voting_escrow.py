import pytest
from brownie import accounts, ERC20, VotingEscrow
from web3 import Web3
from datetime import datetime
from dateutil.relativedelta import relativedelta

staker1_initial_balance = Web3.toWei(100, 'ether')
staker2_initial_balance = Web3.toWei(200, 'ether')

token_name = 'Ocean token'
token_symbol = 'OCEAN'
token_decimals = 18
total_supply = 1_000_000

@pytest.fixture
def deploy():
    pytest.account_deployer = accounts[0]
    pytest.account_staker1 = accounts[1]
    pytest.account_staker2 = accounts[2]

    # deploy smart contracts
    pytest.erc20 = ERC20.deploy(token_name, token_symbol, token_decimals, total_supply, {
                         'from': pytest.account_deployer})
    pytest.voting_escrow = VotingEscrow.deploy(pytest.erc20, {'from': pytest.account_deployer})

    # check that the contract was deployed
    assert pytest.voting_escrow

def test_create_lock(deploy):
    # check initial balances
    assert pytest.erc20.balanceOf(pytest.account_deployer) == Web3.toWei(
        total_supply, 'ether')
    assert pytest.erc20.balanceOf(pytest.account_staker1) == 0
    assert pytest.erc20.balanceOf(pytest.account_staker2) == 0

    pytest.erc20.transfer(pytest.account_staker1, staker1_initial_balance,
                   {'from': pytest.account_deployer})
    pytest.erc20.transfer(pytest.account_staker2, staker2_initial_balance,
                   {'from': pytest.account_deployer})

    assert pytest.erc20.balanceOf(pytest.account_deployer) == Web3.toWei(
        total_supply, 'ether') - staker1_initial_balance - staker2_initial_balance
    assert pytest.erc20.balanceOf(pytest.account_staker1) == staker1_initial_balance
    assert pytest.erc20.balanceOf(pytest.account_staker2) == staker2_initial_balance

    # deposit_for()
    # create_lock()
    # increase_amount()
    # increase_unlock_time()
    # withdraw()

    assert pytest.voting_escrow.get_last_user_slope(pytest.account_staker1) == 0
    assert pytest.voting_escrow.user_point_history__ts(pytest.account_staker1, 0) == 0
    assert pytest.voting_escrow.locked__end(pytest.account_staker1) == 0
    assert pytest.voting_escrow.balanceOf(pytest.account_staker1) == 0
    assert pytest.voting_escrow.totalSupply() == 0

    pytest.erc20.approve(pytest.voting_escrow, Web3.toWei(1, 'ether'), {'from': pytest.account_staker1})
    pytest.voting_escrow.create_lock(
        Web3.toWei(1, 'ether'),
        int((datetime.now() + relativedelta(years = 1)).strftime('%s')),
        {'from': pytest.account_staker1}
    )

    print(f"get_last_user_slope: {pytest.voting_escrow.get_last_user_slope(pytest.account_staker1)}")
    print(f"user_point_history__ts: {pytest.voting_escrow.user_point_history__ts(pytest.account_staker1, 0)}")
    print(f"locked__end: {pytest.voting_escrow.locked__end(pytest.account_staker1)}")
    print(f"balanceOf: {pytest.voting_escrow.balanceOf(pytest.account_staker1)}")
    print(f"totalSupply: {pytest.voting_escrow.totalSupply()}")

    # assert False

def test_pp(deploy):
    print(pytest.account_deployer)
    pass
from brownie import accounts, ERC20, VotingEscrow

def test_deploy():
    account = accounts[0]
    token_name = 'Ocean token'
    token_symbol = 'OCEAN'
    token_decimals = 18
    total_supply = 1_000_000
    version = '1.2'

    erc20 = ERC20.deploy(token_name, token_symbol, token_decimals, total_supply, {'from': account})

    voting_escrow = VotingEscrow.deploy(erc20, {'from': account})

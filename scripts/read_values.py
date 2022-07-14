from brownie import accounts, config, network, VotingEscrow

def read_contract():
    # -1 --> read the latest deployment
    voting_escrow = VotingEscrow[-1]
    print("VotingEscrow deployed on %s" % network.show_active())
    print("Address %s" % voting_escrow)

def main():
    read_contract()
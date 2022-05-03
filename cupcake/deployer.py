from cupcake import packages, compiler, utils

def _deploy(source=None, args=None, provider=None, key_pair=None):
    print(utils.colors.fail, end="\r")
    config_init = open("config.yaml", "r")
    config_file = packages.safe_load(config_init)
    try:
        gas_limit = config_file["Gas"]["Limit"]
    except:
        gas_limit = None
    compiled = compiler._compile(source)
    source_bytecode = compiled[0]
    source_abi = compiled[1]
    if key_pair != None:
        Token = provider.eth.contract(abi=source_abi, bytecode=source_bytecode)
        if args != None:
            tx = Token.constructor(*args).buildTransaction({ "from" : key_pair[1] })
        else:
            tx = Token.constructor().buildTransaction({ "from" : key_pair[1] })
        if gas_limit != None:
            tx.update({ "gas" : gas_limit })
        tx.update({ "nonce" : provider.eth.get_transaction_count(key_pair[1]) })
        signed_tx = provider.eth.account.sign_transaction(tx, key_pair[0])
        tx_hash = provider.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_receipt = provider.eth.wait_for_transaction_receipt(tx_hash)
        contract = provider.eth.contract(address=tx_receipt.contractAddress, abi=source_abi)
        return contract
    else:
        Token = provider.eth.contract(abi=source_abi, bytecode=source_bytecode)
        if args != None:
            tx = Token.constructor(*args).transact({ "from" : provider.eth.accounts[0] })
        else:
            tx = Token.constructor().transact({ "from" : provider.eth.accounts[0] })
        tx_receipt = provider.eth.wait_for_transaction_receipt(tx)
        contract = provider.eth.contract(address=tx_receipt.contractAddress, abi=source_abi)
        return contract

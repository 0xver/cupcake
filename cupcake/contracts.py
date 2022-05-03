from cupcake import packages, utils

def _contract(provider=None, address=None, abi=None):
    print(utils.colors.fail, end="\r")
    contract = provider.eth.contract(address=address, abi=abi)
    return contract

def _read(contract=None, function=None, args=None, expect=None):
    if args != None:
        called = getattr(contract.functions, function)(args).call()
    else:
        called = getattr(contract.functions, function)().call()
    if expect != None:
        message = f"{utils.colors.fail}expect: {expect} {utils.colors.warning}result: {called}"
        assert called == expect, message
        return message
    else:
        print(utils.colors.fail, end="\r")
        called
        print(f"{utils.colors.success}{called}")
        return called

def _write(contract=None, function=None, args=None, value=None, gas=None, caller=None, key_pair=None, provider=None):
    print(utils.colors.fail, end="\r")
    if key_pair != None:
        if args != None and value == None:
            tx = getattr(contract.functions, function)(args).buildTransaction({ "from" : key_pair[1] })
        elif args != None and value != None:
            tx = getattr(contract.functions, function)(args).buildTransaction({ "from" : key_pair[1], "value" : value })
        else:
            if value == None:
                tx = getattr(contract.functions, function)().buildTransaction({ "from" : key_pair[1] })
            else:
                tx = getattr(contract.functions, function)().buildTransaction({ "from" : key_pair[1], "value" : value })
        tx.update({ "nonce" : provider.eth.get_transaction_count(key_pair[1]) })
        tx.update({ "maxFeePerGas" : gas * 1000000000, "maxPriorityFeePerGas" : 2000000000 })
        signed_tx = provider.eth.account.sign_transaction(tx, key_pair[0])
        tx_hash = provider.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_receipt = provider.eth.wait_for_transaction_receipt(tx_hash)
        try:
            init = open("txs/log.txt", "a")
            init.write(str(f"\n\n{tx_receipt.transactionHash.hex()}"))
        except:
            packages.os.mkdir("txs/")
            init = open("txs/log.txt", "w+")
            init.write(str(f"{tx_receipt.transactionHash.hex()}"))
        return tx_receipt.transactionHash.hex()
    else:
        if args != None and value == None:
            tx = getattr(contract.functions, function)(args).transact({ "from" : caller })
        elif args != None and value != None:
            tx = getattr(contract.functions, function)(args).transact({ "from" : caller, "value" : value })
        else:
            if value == None:
                tx = getattr(contract.functions, function)().transact({ "from" : caller })
            else:
                tx = getattr(contract.functions, function)().transact({ "from" : caller, "value" : value })
        return tx.hex()

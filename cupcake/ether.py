from cupcake import packages, utils

def _send(provider=None, to=None, amount=None, gas=None, sender=None, key_pair=None, chain=1):
    print(utils.colors.fail, end="\r")
    if chain == 1 or chain == "mainnet":
        chain_id = 1
    elif chain == "ropsten":
        chain_id = 3
    elif chain == "kovan":
        chain_id = 42
    elif chain == "rinkeby":
        chain_id = 4
    else:
        chain_id = chain
    if key_pair != None:
        signed_tx = provider.eth.account.signTransaction({
            "maxFeePerGas" : gas * 1000000000,
            "maxPriorityFeePerGas" : 2000000000,
            "to" : to,
            "from" : key_pair[1],
            "value" : amount,
            "nonce" : provider.eth.get_transaction_count(key_pair[1]),
            "gas" : 21000,
            "chainId" : chain_id
            },
            key_pair[0]
        )
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
        tx_receipt = provider.eth.send_transaction({ "to" : to, "from" : sender, "value" : amount })
        return tx_receipt.hex()

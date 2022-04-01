from solcx import install_solc, compile_standard
from web3 import Web3, HTTPProvider, EthereumTesterProvider
from web3.middleware import geth_poa_middleware
from json import load, dump, dumps
from yaml import safe_load
from glob import glob
from dotenv import load_dotenv
from pathlib import Path
import os
from cupcake import templates


# Classes

class colors:
    try:
        init = open("config.yaml", "r")
        config_file = safe_load(init)
        if config_file["Colors"]["Disable"] == True:
            success = "\033[0m"
            warning = "\033[0m"
            fail = "\033[0m"
        else:
            success = "\033[95m"
            warning = "\033[93m"
            fail = "\033[91m"
    except:
        success = "\033[95m"
        warning = "\033[93m"
        fail = "\033[91m"


# Templates

def contract_template():
    return templates.greeter_contract

def tests_template():
    return templates.tests

def deploy_template():
    return templates.deploy

def empty_contract_template():
    return templates.empty_contract

def empty_tests_template():
    return templates.empty_tests

def scripts_workspace_template():
    return templates.scripts_workspace

def cupcake_config_template():
    return templates.cupcake_config

def project_config_template():
    return templates.project_config

def script_config_template():
    return templates.script_config


# Check if config exists

def config_exists():
    try:
        init = open("config.yaml", "r")
        config_file = safe_load(init)
        if config_file != None:
            return True
    except:
        return False


# Package functions

def Install():
    print(colors.fail, end="\r")
    init = open("config.yaml", "r")
    config_file = safe_load(init)
    try:
        v = config_file["Solidity"]["Version"]
    except:
        v = None
    if v != None:
        s = str(v)
        install_solc(version=s)
    else:
        install_solc(version="latest")

def Compile():
    print(colors.fail, end="\r")
    Install()
    init = open("config.yaml", "r")
    config_file = safe_load(init)
    source = config_file["Solidity"]["Source"]
    version = str(config_file["Solidity"]["Version"])
    compiler_standard = {
        "language": "Solidity",
        "sources": {},
        "settings": {
            "optimizer": {
            "enabled": True
            },
            "outputSelection": {
                "*": {
                    "*": [
                        "metadata", "evm.bytecode", "abi"
                    ]
                }
            }
        }
    }
    try:
        dir_object = glob("contracts/**/**/*.sol")
        for file in dir_object:
            source_file = os.path.basename(file)
            source_path = {f"{file[10:]}": {"urls": [f"{file}"]}}
            compiler_standard["sources"].update(source_path)
    except:
        pass
    try:
        dir_object = glob("contracts/**/*.sol")
        for file in dir_object:
            source_file = os.path.basename(file)
            source_path = {f"{file[10:]}": {"urls": [f"{file}"]}}
            compiler_standard["sources"].update(source_path)
    except:
        pass
    dir_object = glob("contracts/*.sol")
    for file in dir_object:
        if ".sol" in file:
            source_file = os.path.basename(file)
            source_path = {f"{source_file}": {"urls": [f"{file}"]}}
            compiler_standard["sources"].update(source_path)
    convert_to_json = dumps(compiler_standard, indent = 4)
    try:
        init = open("build/compiler/interface.json", "w")
    except:
        os.mkdir("build/compiler")
        init = open("build/compiler/interface.json", "w")
    init.write(convert_to_json)
    init.close()
    f = open("build/compiler/interface.json", "r")
    json_standard = load(f)
    compiled = compile_standard(json_standard, solc_version=version, allow_paths=".")
    for name in json_standard["sources"]:
        abi = compiled["contracts"][name][os.path.basename(name)[:-4]]["abi"]
        with open(f"build/{os.path.basename(name)[:-4]}.json", "w") as f:
            dump(abi, f)
            f.close()
    abi = compiled["contracts"][f"{source}.sol"][source]["abi"]
    bytecode = compiled["contracts"][f"{source}.sol"][source]["evm"]["bytecode"]["object"]
    return bytecode, abi

def Deploy(provider, keys=None):
    print(colors.fail, end="\r")
    config_init = open("config.yaml", "r")
    config_file = safe_load(config_init)
    constructor_args = config_file["Solidity"]["Constructor"]
    try:
        gas_limit = config_file["Gas"]["Limit"]
    except:
        gas_limit = None
    compiled = Compile()
    source_bytecode = compiled[0]
    source_abi = compiled[1]
    if keys != None:
        Token = provider.eth.contract(abi=source_abi, bytecode=source_bytecode)
        if constructor_args != None:
            tx = Token.constructor(*constructor_args).buildTransaction({ "from" : keys[1] })
        else:
            tx = Token.constructor().buildTransaction({ "from" : keys[1] })
        if gas_limit != None:
            tx.update({ "gas" : gas_limit })
        tx.update({ "nonce" : provider.eth.get_transaction_count(keys[1]) })
        signed_tx = provider.eth.account.sign_transaction(tx, keys[0])
        tx_hash = provider.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_receipt = provider.eth.wait_for_transaction_receipt(tx_hash)
        contract = provider.eth.contract(address=tx_receipt.contractAddress, abi=source_abi)
        return contract
    else:
        Token = provider.eth.contract(abi=source_abi, bytecode=source_bytecode)
        if constructor_args != None:
            tx = Token.constructor(*constructor_args).transact({ "from" : provider.eth.accounts[0] })
        else:
            tx = Token.constructor().transact({ "from" : provider.eth.accounts[0] })
        tx_receipt = provider.eth.wait_for_transaction_receipt(tx)
        contract = provider.eth.contract(address=tx_receipt.contractAddress, abi=source_abi)
        return contract

def Contract(provider, address, abi):
    print(colors.fail, end="\r")
    contract = provider.eth.contract(address=address, abi=abi)
    return contract

def Provider(p=None):
    init = open("config.yaml", "r")
    file = safe_load(init)
    try:
        provider_info = str(file["Network"][p])
        provider = Web3(HTTPProvider(provider_info))
        provider.middleware_onion.inject(geth_poa_middleware, layer=0)
        return provider
    except:
        provider = Web3(EthereumTesterProvider())
        from warnings import filterwarnings
        filterwarnings("ignore", category=ResourceWarning)
        return provider 

def Account(provider=None):
    print(colors.fail, end="\r")
    init = open("config.yaml", "r")
    file = safe_load(init)
    try:
        key_path = file["Key"]["Location"]
    except:
        key_path = ".env"
    dotenv_path = Path(key_path)
    load_dotenv(dotenv_path=dotenv_path)
    private_key = os.getenv("PRIVATE_KEY")
    if provider == None:
        pk_object = Web3().eth.account.privateKeyToAccount(private_key)
        public_key = pk_object.address
        return private_key, public_key
    else:
        addr1 = provider.eth.accounts[0]
        addr2 = provider.eth.accounts[1]
        addr3 = provider.eth.accounts[2]
        addr4 = provider.eth.accounts[3]
        addr5 = provider.eth.accounts[4]
        addr6 = provider.eth.accounts[5]
        addr7 = provider.eth.accounts[6]
        addr8 = provider.eth.accounts[7]
        addr9 = provider.eth.accounts[8]
        return None, addr1, addr2, addr3, addr4, addr5, addr6, addr7, addr8, addr9

def Read(contract, function, args=None, expect=None):
    if args != None:
        called = getattr(contract.functions, function)(args).call()
    else:
        called = getattr(contract.functions, function)().call()
    if expect != None:
        message = f"{colors.fail}expect: {expect} {colors.warning}result: {called}"
        assert called == expect, message
        return message
    else:
        print(colors.fail, end="\r")
        called
        print(f"{colors.success}{called}")
        return called

def Write(contract, function, args=None, value=None, caller=None, keys=None, provider=None):
    print(colors.fail, end="\r")
    if keys != None:
        if args != None and value == None:
            tx = getattr(contract.functions, function)(args).buildTransaction({ "from" : keys[1] })
        elif args != None and value != None:
            tx = getattr(contract.functions, function)(args).buildTransaction({ "from" : keys[1], "value" : value })
        else:
            if value == None:
                tx = getattr(contract.functions, function)().buildTransaction({ "from" : keys[1] })
            else:
                tx = getattr(contract.functions, function)().buildTransaction({ "from" : keys[1], "value" : value })
        tx.update({ "nonce" : provider.eth.get_transaction_count(keys[1]) })
        signed_tx = provider.eth.account.sign_transaction(tx, keys[0])
        tx_hash = provider.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_receipt = provider.eth.wait_for_transaction_receipt(tx_hash)
        try:
            init = open("txs/log.txt", "a")
            init.write(str(f"\n\n{tx_receipt.transactionHash.hex()}"))
        except:
            os.mkdir("txs/")
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

def Send(provider, to=None, amount=None, sender=None, keys=None, chainId=1):
    print(colors.fail, end="\r")
    if chainId == 1 or chainId == "mainnet":
        chain = 1
    elif chainId == "ropsten":
        chain = 3
    elif chainId == "kovan":
        chain = 42
    elif chainId == "rinkeby":
        chain = 4
    else:
        chain = chainId
    if keys != None:
        signed_tx = provider.eth.account.signTransaction({
            "maxFeePerGas" : 3000000000,
            "maxPriorityFeePerGas" : 2000000000,
            "to" : to,
            "from" : keys[1],
            "value" : amount,
            "nonce" : provider.eth.get_transaction_count(keys[1]),
            "gas" : 100000,
            "chainId" : chain
            },
            keys[0]
        )
        tx_hash = provider.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_receipt = provider.eth.wait_for_transaction_receipt(tx_hash)
        try:
            init = open("txs/log.txt", "a")
            init.write(str(f"\n\n{tx_receipt.transactionHash.hex()}"))
        except:
            os.mkdir("txs/")
            init = open("txs/log.txt", "w+")
            init.write(str(f"{tx_receipt.transactionHash.hex()}"))
        return tx_receipt.transactionHash.hex()
    else:
        tx_receipt = provider.eth.send_transaction({ "to" : to, "from" : sender, "value" : amount })
        return tx_receipt.hex()

def msg(message=None, public_key=None, contract=None, tx=None):
    if public_key != None and contract != None:
        print(f"{colors.success}Successfully served cupcakes!\nDeployer account: {public_key}\nContract address: {contract.address}")
    if tx != None:
        print(f"{colors.success}Successfully sent cupcakes!\nTransaction: {tx}")
    if message == "frosted":
        print(f"{colors.success}Cupcakes have been successfully frosted!")
    if message == "baked":
        print(f"{colors.success}Cupcakes have been successfully baked!")

def loads(path):
    print(colors.fail, end="\r")
    json_file = open(path, "r")
    json_data = load(json_file)
    return json_data

def eth(eth):
    print(colors.fail, end="\r")
    wei = int(eth*1000000000000000000)
    return wei

def p(object):
    print(f"{colors.success}{object}")
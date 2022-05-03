empty_deploy = """from cupcake import account, deploy, msg, provider

# Provider
mainnet = provider("Custom")

# Accounts
key_pair = account()
public_key = key_pair[1]

# Deploy
contract = deploy("", provider=mainnet, key_pair=key_pair)

# Notification
msg(public_key=public_key, contract=contract)
"""

empty_config = """Solidity:
    Version: 0.8.0
Network:
    Custom:
    Ganache: http://127.0.0.1:7545
"""

empty_contract = """// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract Contract {}
"""

empty_tests = """from cupcake import account, deploy, eth, msg, provider, read, send, write

# Provider
py_evm = provider()

# Accounts
accounts = account(py_evm)
addr1 = accounts[1]
addr2 = accounts[2]

# Deploy
contract = deploy("contract", provider=py_evm)

# Tests
# read(contract, "function", expect="expected")
# write(contract, "function", caller=addr1)
# send(py_evm, to=addr2, amount=eth(2), sender=addr1)

# Notification
# msg("frosted")
"""

greeter_config = """Solidity:
    Version: 0.8.0
Network:
    Custom:
    Ganache: http://127.0.0.1:7545
"""

greeter_contract = """// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract Greeter {
    string private message;

    constructor(string memory _message) {
        message = _message;
    }

    function greeting() public view returns (string memory) {
        return message;
    }

    function setGreeting(string memory _message) public {
        message = _message;
    }
}
"""

greeter_deploy = """from cupcake import account, deploy, msg, provider

# Provider
mainnet = provider("Custom")

# Accounts
key_pair = account()
public_key = key_pair[1]

# Deploy
contract = deploy("Greeter", ["Hello world!"], mainnet, key_pair)

# Notification
msg(public_key=public_key, contract=contract)
"""

greeter_tests = """from cupcake import account, deploy, eth, msg, provider, read, write

# Provider
py_evm = provider()

# Accounts
accounts = account(py_evm)
addr1 = accounts[1]
addr2 = accounts[2]

# Deploy
contract = deploy("Greeter", ["Hello world!"], py_evm)

# Tests
read(contract, "greeting", expect="Hello world!")
write(contract, "setGreeting", args="Hello!", caller=addr1)
read(contract, "greeting", expect="Hello!")

# Notification
msg("frosted")
"""

workspace_config = """Scripts:
    Source: scripts
Network:
    Custom:
    Ganache: http://127.0.0.1:7545
"""

workspace_scripts = """from cupcake import account, contract, eth, msg, provider, read, send, source, write

# Provider
mainnet = provider("Custom")

# Accounts
key_pair = account()
public_key = key_pair[1]

# Contract
address = ""
abi = source("api/<contract>.json")
contract = contract(mainnet, address, abi)

# Smart contracts
read(contract, "function", expect="expected")
tx = write(contract, "function", args=eth(1), gas=20, key_pair=key_pair, provider=mainnet)

# Notification
msg(tx=tx)

# Send ETH
tx = send(provider, to="0x...", amount=eth(0.001), gas=20, key_pair=key_pair, chain="mainnet")

# Notification
msg(tx=tx)
"""

empty_deploy = """from cupcake import Account, Deploy, Provider, msg

# Provider
provider = Provider("Custom")

# Accounts
key_pair = Account()
public_key = key_pair[1]

# Deploy
contract = Deploy("", provider=provider, key_pair=key_pair)

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

empty_tests = """from cupcake import Account, Deploy, Provider, Read, Send, Write, eth, msg

# Provider
provider = Provider()

# Accounts
accounts = Account(provider)
addr1 = accounts[1]
addr2 = accounts[2]

# Deploy
contract = Deploy("Contract", provider=provider)

# Tests
# Read(contract, "function", expect="expected")
# Write(contract, "function", caller=addr1)
# Send(provider, to=addr2, amount=eth(2), sender=addr1)

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

greeter_deploy = """from cupcake import Account, Deploy, Provider, msg

# Provider
provider = Provider("Custom")

# Accounts
key_pair = Account()
public_key = key_pair[1]

# Deploy
contract = Deploy("Greeter", ["Hello world!"], provider, key_pair)

# Notification
msg(public_key=public_key, contract=contract)
"""

greeter_tests = """from cupcake import Account, Deploy, Provider, Read, Write, eth, msg

# Provider
provider = Provider()

# Accounts
accounts = Account(provider)
addr1 = accounts[1]
addr2 = accounts[2]

# Deploy
contract = Deploy("Greeter", ["Hello world!"], provider)

# Tests
Read(contract, "greeting", expect="Hello world!")
Write(contract, "setGreeting", args="Hello!", caller=addr1)
Read(contract, "greeting", expect="Hello!")

# Notification
msg("frosted")
"""

workspace_config = """Scripts:
    Source: scripts
Network:
    Custom:
    Ganache: http://127.0.0.1:7545
"""

workspace_scripts = """from cupcake import Account, Contract, Provider, Read, Send, Write, eth, loads, msg

# Provider
provider = Provider("Custom")

# Accounts
key_pair = Account()
public_key = key_pair[1]

# Contract
address = ""
abi = loads("abi/<contract>.json")
contract = Contract(provider, address, abi)

# Smart contracts
Read(contract, "function", expect="expected")
tx = Write(contract, "function", args=eth(1), key_pair=key_pair, provider=provider)

# Notification
msg(tx=tx)

# Send ETH
# tx = Send(provider, to="0x...", amount=eth(1), key_pair=key_pair, chain="mainnet")

# Notification
msg(tx=tx)
"""

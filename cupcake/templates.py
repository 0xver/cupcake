greeter_contract = '''// SPDX-License-Identifier: MIT

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
'''

empty_contract = '''// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract Contract {}
'''

tests = '''from cupcake import Account, Deploy, Provider, Read, Write, eth, msg

# Provider
provider = Provider()

# Accounts
accounts = Account(provider)
addr1 = accounts[1]
addr2 = accounts[2]

# Deploy
contract = Deploy(provider)

# Tests
Read(contract, "greeting", expect="Hello world!")
Write(contract, "setGreeting", args="Hello!", caller=addr1)
Read(contract, "greeting", expect="Hello!")

# Notification
msg("frosted")'''

deploy = '''from cupcake import Account, Deploy, Provider, msg

# Provider
provider = Provider("Custom")

# Accounts
public_key = Account()[1]
keys = Account()

# Deploy
contract = Deploy(provider, keys)

# Notification
msg(public_key=public_key, contract=contract)'''

empty_tests = '''from cupcake import Account, Deploy, Provider, Read, Send, Write, eth, msg

# Provider
provider = Provider()

# Accounts
accounts = Account(provider)
addr1 = accounts[1]
addr2 = accounts[2]

# Deploy
contract = Deploy(provider)

# Tests
# Read(contract, "function", expect="expected")
# Write(contract, "function", caller=addr1)
# Send(provider, to=addr2, amount=eth(2), sender=addr1)

# Notification
# msg("frosted")'''

cupcake_config='''Solidity:
    Version: 0.8.0
    Source: Greeter
    Constructor:
        - Hello world!
Network:
    Custom:
    Ganache:'''

project_config='''Solidity:
    Version: 0.8.0
    Source: Contract
    Constructor:
Network:
    Custom:
    Ganache:'''

script_config='''Scripts:
    Source: scripts
Network:
    Custom:
    Ganache:'''

scripts_workspace = '''from cupcake import Account, Contract, Provider, Read, Send, Write, eth, loads, msg

# Provider
provider = Provider("Custom")

# Keys
public_key = Account()[1]
keys = Account()

# Contract
address = ""
abi = loads("abi/<contract>.json")
contract = Contract(provider, address, abi)

# Blockchain interactions
# Read(contract, "function", expect="expected")
# tx = Write(contract, "function", args=eth(1), keys=keys, provider=provider)
# tx = Send(provider, to="0x...", amount=eth(1), keys=keys, chainId="mainnet")

# Notification
msg(tx=tx)'''
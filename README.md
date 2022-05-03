# <img src="https://bafybeidfcld7pk7bt2lirks6tkwseicbp6vdgvko2bmhzkriwhfolifg4u.ipfs.dweb.link/cupcake-logo.svg" width="25" height="20"> Cupcake

[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/0xver/cupcake/blob/master/LICENSE.md)

## Easily compile, test, and deploy smart contracts
Cupcake is a development enviroment to compile, test, and deploy Ethereum smart contracts. It automates the process down to a few lines of code for most complex operations, while continuing to maintain versatility. The built-in network makes testing just work without any additional setup. Optionally, Ganache can easily be used as a provider.

## Interact with existing contracts and send ether
Cupcake comes with a scripting workspace for sending ether and interacting with other smart contracts on the blockchain.

#

## Source
Clone cupcake
```
gh repo clone 0xver/cupcake
```
Install cupcake
```
pip install .
```

#

## PyPi
Install cupcake
```
pip install cupcakes
```

#

## Getting Started
Start new cupcake project and select option
```
cupcake
```
Open the project
```
cd name
```
View the command options
```
cupcake
```

#

## Compile
Compile smart contracts
```
cupcake bake
```

#

## Test
Test smart contracts
```
cupcake frost
```

#

## Deploy
Deploy smart contracts
```
cupcake serve
```

#

## Interact
Interact with smart contracts through the script workspace
```
cupcake shop
```

#

## API
| Function | Parameters |
| --- | --- |
| `account(provider)` | (Optional) `provider(type)` |
| `compile(source)` | (Optional) `"Contract"` |
| `contract(provider, address, abi)` | `provider(type)`, `0x...`, "[]" |
| `deploy(source, constructor, provider, key_pair)` | `"Contract"`, (Optional) [`"constructor arguments"`], `provider(type)`, (Optional) `account()` |
| `install(version)` | (Optional) `0.0.0` |
| `provider(type)` | `"Custom"`, `"Ganache"` |
| `read(contract, function, args, expect)` | `contract(provider, address, abi)`, `"function"`, (Optional) `"args"`, (Optional) `<expect>` |
| `send(provider, to, amount, gas, sender, key_pair, chain)` | `provider(type)`, `0x...`, `eth(1)`, (Optional) `50`, (Optional) `account()[1]`, (Optional) `account()`, (Optional) `1` |
| `write(contract, function, args, value, gas, caller, key_pair, provider)` | `contract(provider, address, abi)`, `"function"`, (Optional) `"args"`, (Optional) `eth(1)`, (Optional) `50`, (Optional) `account()[1]`, (Optional) `account()`, (Optional) `provider(type)` |

#

### `account(provider)`
The account function will convert a private key into a public key without any parameter argument or derive accounts from the provider. Returns key_pair `account()` and public key `account()[1]` from the private key in .env or public addresses from a provider as `account(provider)[1]` through `account(provider)[9]`.

#

### `compile(source)`
Optionally set source argument to return object. Compiler outputs contract ABIs to `build/`. Runs `Install()` before compiling. Returns the source bytecode `compile()[0]` and source ABI `compile()[1]` only if the source argument is set.

#

### `contract(provider, address, abi)`
Access an existing contract by giving a provider, contract address, and the contract's ABI. Returns `contract` object.

#

### `deploy(source, constructor, provider, key_pair)`
Will `compile(source)` contracts and deploy contracts from the provider. Optionally use an array of constructor arguments. Use `account()` for the optional `key_pair` parameter. The first address from the provider is used if no `key_pair` are provided. Returns `contract` object.

#

### `install(version)`
Installs version of Solidity or latest version if not argument is not set.

#

### `provider(type)`
`"Custom"` and `"Ganache"` are `type` arguments. `"Custom"` and `"Ganache"` types are defined in config.yaml. Use the built in local network with `provider()`.

#

### `read(contract, function, args, expect)`
Use `contract()` or `deploy()` for the `contract` argument. Specify the `function` as a string. Optionally use `args` for the contract function arguments. Optionally use the `expect` argument to override the return.

#

### `send(provider, to, amount, gas, sender, key_pair, chain)`
Sends ether from an account. Use `account(provider)[1]` for the `sender` or use `account()` for the `key_pair`. Using `key_pair` does not require the `sender` argument. Use `gas` and `chain` only if `key_pair` is used. Supported `chain` string arguments are `"mainnet"`, `"ropsten"`, `"kovan"`, and `"rinkeby"`. If no `chain` is provided, the Ethereum mainnet is used. Logs transaction hash to `txs/`.  Returns `transaction hash`.

#

### `write(contract, function, args, value, gas, caller, key_pair, provider)`
Use `contract()` or `deploy()` for the `contract` argument. Specify the `function` as a string. Optionally use `args` for the contract function's argument. Optionally use `value` if function requires ether. Use `caller` or use `gas`, `key_pair` and `provider` depending on the setup. Logs transaction hash to `txs/`. Returns `transaction hash`.

#

## Add private key
Create .env file in project folder
```
touch .env
```
Add the private key to PRIVATE_KEY in the .env file and include 0x
```
PRIVATE_KEY=0x...
```

#

## Enable Ganache
Add Ganache host and port in config.yaml
```
Network:
    Ganache: http://127.0.0.1:7545
```
Set the `provider(type)` to Ganache
```
provider("Ganache")
```

#

## Return automated messages
Use `msg("baked")` or `msg("frosted")` to return success messages. Use `msg(public_key=public_key, contract=contract)` to return deployment message. Use `msg(tx=tx)` to return transaction message.

#

## Convert ETH to WEI
Use `eth(value)` to convert ETH to WEI

#

## Load ABI from json file
Use `source(abi/contract.json)` to return ABI

#

## Set gas limit
Add the following to config.yaml
```
Gas:
    Limit: 200000
```

#

## Change the .env file path location
Add the following to config.yaml
```
Key:
    Location: "path/.env"
```

#

## Change config.yaml network names
Change the config.yaml custom network name to enable `provider("Infura")`
```
Network:
    Infura:
```

#

## Print with color
Use `p(object)` to `print()` with color

#

## Disable Colors
Add the following to config.yaml to disable colors
```
Colors:
    Disable: True
```

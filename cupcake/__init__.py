from cupcake import accounts, compiler, contracts, deployer, installer, providers, ether, utils

def account(provider=None):
    return accounts._account(provider)

def compile(source=None):
    return compiler._compile(source)

def contract(provider=None, address=None, abi=None):
    return contracts._contract(provider, address, abi)

def read(contract=None, function=None, args=None, expect=None):
    return contracts._read(contract, function, args, expect)

def write(contract=None, function=None, args=None, value=None, gas=None, caller=None, key_pair=None, provider=None):
    return contracts._write(contract, function, args, value, gas, caller, key_pair, provider)

def deploy(source=None, args=None, provider=None, key_pair=None):
    return deployer._deploy(source, args, provider, key_pair)

def install(v=None):
    return installer._install(v)

def provider(p=None):
    return providers._provider(p)

def send(provider=None, to=None, amount=None, gas=None, sender=None, key_pair=None, chain=1):
    return ether._send(provider, to, amount, gas, sender, key_pair, chain)

def source(path):
    return utils._source(path)

def msg(message=None, public_key=None, contract=None, tx=None):
    return utils._msg(message, public_key, contract, tx)

def eth(eth):
    return utils._eth(eth)

def p(object):
    return utils._p(object)

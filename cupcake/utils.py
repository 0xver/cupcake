from cupcake import packages

class colors:
    try:
        init = open("config.yaml", "r")
        config_file = packages.safe_load(init)
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

def config_exists():
    try:
        init = open("config.yaml", "r")
        config_file = packages.safe_load(init)
        if config_file != None:
            return True
    except:
        return False

def _source(path):
    print(colors.fail, end="\r")
    json_file = open(path, "r")
    json_data = packages.load(json_file)
    return json_data

def _msg(message=None, public_key=None, contract=None, tx=None):
    if public_key != None and contract != None:
        print(f"{colors.success}Successfully served cupcakes!\nDeployer account: {public_key}\nContract address: {contract.address}")
    if tx != None:
        print(f"{colors.success}Successfully sent cupcakes!\nTransaction: {tx}")
    if message == "frosted":
        print(f"{colors.success}Cupcakes have been successfully frosted!")
    if message == "baked":
        print(f"{colors.success}Cupcakes have been successfully baked!")

def _eth(eth):
    print(colors.fail, end="\r")
    wei = int(eth*1000000000000000000)
    return wei

def _p(object):
    print(f"{colors.success}{object}")

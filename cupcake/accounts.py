from cupcake import packages, utils

def _account(provider=None):
    print(utils.colors.fail, end="\r")
    init = open("config.yaml", "r")
    file = packages.safe_load(init)
    try:
        key_path = file["Key"]["Location"]
    except:
        key_path = ".env"
    dotenv_path = packages.Path(key_path)
    packages.load_dotenv(dotenv_path=dotenv_path)
    private_key = packages.os.getenv("PRIVATE_KEY")
    if provider == None:
        pk_object = packages.Web3().eth.account.privateKeyToAccount(private_key)
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

from cupcake import packages

def _provider(p=None):
    init = open("config.yaml", "r")
    file = packages.safe_load(init)
    try:
        provider_info = str(file["Network"][p])
        provider = packages.Web3(packages.HTTPProvider(provider_info))
        provider.middleware_onion.inject(packages.geth_poa_middleware, layer=0)
        return provider
    except:
        provider = packages.Web3(packages.EthereumTesterProvider())
        from warnings import filterwarnings
        filterwarnings("ignore", category=ResourceWarning)
        return provider

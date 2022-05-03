from cupcake import packages, utils

def _install(v=None):
    print(utils.colors.fail, end="\r")
    if v != None:
        s = str(v)
        packages.install_solc(version=s)
    else:
        packages.install_solc(version="latest")

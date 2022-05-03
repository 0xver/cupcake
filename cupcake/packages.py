from solcx import install_solc, compile_standard, set_solc_version
from web3 import Web3, HTTPProvider, EthereumTesterProvider
from web3.middleware import geth_poa_middleware
from json import load, dump, dumps
from yaml import safe_load
from glob import glob
from dotenv import load_dotenv
from pathlib import Path
import os

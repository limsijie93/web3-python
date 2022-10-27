import os
import json
from web3 import Web3
from dotenv import load_dotenv

import solcx
from solcx import compile_standard

solcx.install_solc('0.6.0')
load_dotenv("./web3-python/web3-simple-storage/.env")

with open("./SimpleStorage.sol", "r") as f:
    s2_file = f.read()
    print(s2_file)

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": s2_file}},
        "settings": {"outputSelection":
            {"*":
                {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"] # TODO: Find out what are these
                }
            }
        }
    },
    solc_version="0.6.0"
)

with open("compiled_code.json", "w") as f:
    json.dump(compiled_sol, f)

## Getting the bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]

## Getting the abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# Blockchain connecting details
w3 = Web3(Web3.HTTPProvider(os.getenv("HTTP_PROVIDER")))
chain_id = os.getenv("CHAIN_ID")
my_addr = os.getenv("ADDRESS")
private_key = os.getenv("PRIVATE_KEY")

# Create contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
print(SimpleStorage)

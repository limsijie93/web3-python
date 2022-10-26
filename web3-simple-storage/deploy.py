import json

from solcx import compile_standard

solcx.install_solc('0.6.0')

with open("./SimpleStorage.sol", "r") as f:
    s2_file = f.read()
    print(s2_file)

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleSotrage.sol": {"content": s2_file}},
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

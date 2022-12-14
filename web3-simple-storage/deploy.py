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

# Build a transaction
## To make a state change on the blockchain.

####### Nounce
nonce = w3.eth.getTransactionCount(my_addr) #NOTE: Make sure that your blockchain (i.e. Ganache) is running
print(nonce)

### 1. Build contract Deploy Transaction
transaction = SimpleStorage.constructor().build_transaction({
    "gasPrice":  w3.eth.gas_price,
    "chainId":  w3.eth.chain_id, #NOTE: chain_id is not the same as network_id. Use chain_id from w3.eth instead
    "from": my_addr,
    "nonce": nonce
})
## This returns the data key. The value encompasses what happens in the SimpleStorage blockchain

### 2. Sign the Transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

### 3. Send Transaction to the blockchaincal

txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash) # this waits for transaction to go through

## When working with the contract, you need 2 things
## 1. Contract Address
## 2. ABI
simple_storage = w3.eth.contract(address=txn_receipt.contractAddress, abi=abi)

## NOTE: We can't just use print. We need to add either Call or Transact method behind
print(simple_storage.functions.retrieve().call()) # this is the rerieve function from the SimpleStorage.sol
print(simple_storage.functions.store(15).call()) # This returns [] becuase the rerieve function from the SimpleStorage.sol doesn't return anything
## Call: Doesn't make a state change to the blockchain. It's just a simulation
## Transact: We make a state change
store_txn = simple_storage.functions.store(15).buildTransaction({
    "gasPrice": w3.eth.gas_price,
    "chainId": w3.eth.chain_id,
    "from": my_addr, "nonce": nonce+1
})
signed_store_txn = w3.eth.account.sign_transaction(store_txn,
                                                   private_key=private_key)
send_store_txn = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
txn_receipt = w3.eth.wait_for_transaction_receipt(send_store_txn)
print(simple_storage.functions.retrieve().call()) # this now returns 15 because we stored 15 in line 84


from solcx import compile_standard, install_solc
install_solc("0.6.0")
import json
from dotenv import load_dotenv
import os
from web3 import Web3

load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    source_code = file.read()

# Compiler Our Solidity code

compile_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": source_code}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": [
                        "abi",
                        "metadata",
                        "evm.bytecode",
                        "evm.bytecode.sourceMap",
                    ]
                }
            }
        },
    },
    solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compile_sol, file)

#get bytecode
bytecode = compile_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]

#get abi
abi = compile_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"] 

#web3 for connecting to ganache
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
chain_id = 5777
my_address = "0x919A02D32273a1DEd65873dC99a2965483257aA1"
private_key = os.getenv("PRIVATE_KEY")

#Create the contract in python
SimpaleStore = w3.eth.contract(abi=abi, bytecode=bytecode)

#Get the lastest transaction
nonce = w3.eth.getTransactionCount(my_address)
#1 Build a transaction
transaction = SimpaleStore.constructor().buildTransaction(
    {
        "from": my_address,
        "nonce": nonce,
        "chainId": chain_id,
        "gas": 1000000,
        "gasPrice": w3.toWei("10", "gwei"),
    }
)
#2 Sign the transaction
signed_txn = w3.eth.account.signTransaction(transaction, private_key=private_key)

#3 Send the transaction
#Send this signed transaction
tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

#Work with the contract, you allways need
#Contract Address
#Contract ABI
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

#Call -> Getting a return value
#Transact -> Make the state change

#Initial value of favorite number
print(simple_storage.functions.retrieve().call())
store_transaction = simple_storage.funcations.store(15).buildTransaction({
    "from": my_address,
    "nonce": nonce +1,
    "chainId": chain_id,
})
signed_store_tx = w3.eth.account.signTransaction(store_transaction, private_key=private_key)
send_store_tx = w3.eth.sendRawTransaction(signed_store_tx.rawTransaction)
transaction_hash = w3.eth.sendRawTransaction(signed_store_tx.rawTransaction)
tx_receipt = w3.eth.waitForTransactionReceipt(send_store_tx)
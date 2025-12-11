from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from web3 import Web3
from eth_account import Account
import os

app = FastAPI(title="DeFi Without Borders - QIE Live Backend")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# QIE Testnet
w3 = Web3(Web3.HTTPProvider("https://rpc1testnet.qie.digital/"))
CHAIN_ID = 1983

# WALLET
PRIVATE_KEY = "d27a320373072466539d5d47f573c786f3e791a80c1e358f6e18c24652461b51"
account = Account.from_key(PRIVATE_KEY)

@app.get("/")
def home():
    balance = w3.from_wei(w3.eth.get_balance(account.address), "ether")
    return {
        "project": "DeFi Without Borders",
        "address": account.address,
        "QIE_balance": float(balance),
        "block": w3.eth.block_number,
        "status": "LIVE on QIE Testnet"
    }

@app.post("/send")
def send(to: str, amount: float):
    nonce = w3.eth.get_transaction_count(account.address)
    tx = {
        "nonce": nonce,
        "to": to,
        "value": w3.to_wei(amount, "ether"),
        "gas": 21000,
        "gasPrice": w3.to_wei("5", "gwei"),
        "chainId": CHAIN_ID
    }
    signed = account.sign_transaction(tx)
    hash = w3.eth.send_raw_transaction(signed.raw_transaction).hex()
    return {"success": True, "tx": hash, "explorer": f"https://testnet.qie.digital/tx/{hash}"}
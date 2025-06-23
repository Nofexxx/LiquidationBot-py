# config.py

import json

# import logging
import os
from typing import Any, Dict, List

from dotenv import load_dotenv
from eth_account import Account
from eth_account.signers.local import LocalAccount
from eth_typing import ChecksumAddress
from web3 import Web3
from web3.contract import Contract

load_dotenv()
MY_LIQUIDATION_CONTRACT_ADDRESS: ChecksumAddress = Web3.to_checksum_address(
    "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"
)


def getWeb3Provider() -> Web3:
    rpcUrl: str | None = os.getenv("RPC_URL")
    if not rpcUrl:
        raise ValueError("RPC_URL environment variable is not set")
    return Web3(Web3.HTTPProvider(rpcUrl))


def getAccount() -> LocalAccount:
    privateKey: str | None = os.getenv("PRIVATE_KEY")
    if not privateKey:
        raise ValueError("PRIVATE_KEY environment variable is not set")
    return Account.from_key(privateKey)


def getContract(w3: Web3, abiFileName: str) -> Contract:
    abi_path: str = os.path.join("abi", abiFileName)
    with open(abi_path) as f:
        data: Dict[str, Any] | List[Dict[str, Any]] = json.load(f)

    abi: Any
    if isinstance(data, dict) and "abi" in data:
        abi = data["abi"]
    elif isinstance(data, list):
        abi = data
    else:
        raise ValueError("Invalid abi format")

    return w3.eth.contract(address=MY_LIQUIDATION_CONTRACT_ADDRESS, abi=abi)

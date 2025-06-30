import json
import logging
import os
from logging import Logger
from typing import Any, Dict, List

from eth_account import Account
from eth_account.signers.local import LocalAccount
from eth_typing import ChecksumAddress
from web3 import AsyncWeb3
from web3.contract import AsyncContract

logger: Logger = logging.getLogger("botLogs")


async def getWeb3Provider() -> AsyncWeb3:
    rpcUrl: str | None = os.getenv("RPC_URL")
    if not rpcUrl:
        raise ValueError("RPC_URL environment variable is not set")

    w3: AsyncWeb3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(rpcUrl))

    logger.info("Connected to network (Chain ID: %i)", await w3.eth.chain_id)
    logger.info("Latest block: %i", await w3.eth.block_number)

    return w3


async def getAccount() -> LocalAccount:
    privateKey: str | None = os.getenv("PRIVATE_KEY")
    if not privateKey:
        raise ValueError("PRIVATE_KEY environment variable is not set")

    account: LocalAccount = Account.from_key(privateKey)
    logger.info("Account loaded: %s", account.address)

    return account


async def getContract(
    w3: AsyncWeb3, contractAddress: ChecksumAddress, abiFileName: str
) -> AsyncContract:
    abi_path: str = os.path.join("abi", abiFileName)
    logger.debug("abi path: %s", abi_path)
    with open(abi_path) as f:
        data: Dict[str, Any] | List[Dict[str, Any]] = json.load(f)

    abi: Any
    if isinstance(data, dict) and "abi" in data:
        abi = data["abi"]
    elif isinstance(data, list):
        abi = data
    else:
        raise ValueError("Invalid abi format")

    if not abi:
        raise ValueError("Empty abi")

    contract: Any = w3.eth.contract(address=contractAddress, abi=abi)

    code: Any = await w3.eth.get_code(contract.address)

    if len(code) < 2:
        raise ValueError("Invalid address contract")

    if not contract:
        raise ValueError("Contract is not exists")
    logger.info("Contract exists at: %s", contractAddress)

    return contract

import asyncio
from typing import List

from eth_account.signers.local import LocalAccount
from eth_typing import ChecksumAddress
from web3 import Web3
from web3.contract import Contract

from models.schemas.schemas import UserDebtData
from scripts.contract_methods import (
    LiquidationCall,
    calculateMaxProfitableLiquidationData,
    getHealthFactor,
)
from scripts.web3_config import getAccount, getContract, getWeb3Provider
from utils.db_service import getAddressUsersFromDb


async def run_process() -> None:
    w3: Web3 = getWeb3Provider()
    account: LocalAccount = getAccount()
    contract: Contract = getContract(w3, "liquidation.json")

    receiveAToken: bool = False
    batchSize: int = 3

    while True:
        borrowers: List[str] = await getAddressUsersFromDb()
        print("Borrowers: ", borrowers)
        await batchProcessLiquidation(
            w3, account, contract, borrowers, receiveAToken, batchSize
        )


async def batchProcessLiquidation(
    w3: Web3,
    account: LocalAccount,
    contract: Contract,
    _borrowers: List[str],
    receiveAToken: bool,
    batchSize: int,
) -> None:

    borrowers: List[ChecksumAddress] = [
        w3.to_checksum_address(borrower) for borrower in _borrowers
    ]

    for i in range(0, len(borrowers), batchSize):
        batch: List[ChecksumAddress] = borrowers[i : i + batchSize]
        print("Users butches: ", batch)

        task = [
            processUser(
                w3=w3,
                account=account,
                contract=contract,
                userAddress=userAddress,
                receiveAToken=receiveAToken,
            )
            for userAddress in batch
        ]

        result: list[BaseException | None] = await asyncio.gather(
            *task, return_exceptions=True
        )

        for i, error in enumerate(result):
            if isinstance(result, Exception):
                print(f"User: {i}, execute with error: {error}")

        await asyncio.sleep(2)


async def processUser(
    w3: Web3,
    account: LocalAccount,
    contract: Contract,
    userAddress: ChecksumAddress,
    receiveAToken: bool,
) -> None:
    try:
        hf: int = await getHealthFactor(contract, userAddress)

        if hf < 1e18:
            userDebtData: UserDebtData = await calculateMaxProfitableLiquidationData(
                contract, userAddress
            )
            await LiquidationCall(w3, account, contract, userDebtData, receiveAToken)
    except Exception as e:
        print(f"Error processing {userAddress}: {e}")

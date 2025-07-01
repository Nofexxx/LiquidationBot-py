import asyncio
import logging
from logging import Logger
from typing import List

from eth_account.signers.local import LocalAccount
from eth_typing import ChecksumAddress
from web3 import AsyncWeb3
from web3.contract import AsyncContract

from models.schemas.schemas import TxData, UserDebtData
from scripts.contract_methods import (
    LiquidationCall,
    calculateMaxProfitableLiquidationData,
    getHealthFactor,
)
from utils.db_service import getAddressUsersFromDb

logger: Logger = logging.getLogger("botLogs")


async def run_process(
    w3: AsyncWeb3,
    account: LocalAccount,
    contract: AsyncContract,
    receiveAToken: bool,
    batchSize: int,
) -> None:
    while True:
        borrowers: List[str] = await getAddressUsersFromDb()
        await batchProcessLiquidation(
            w3, account, contract, borrowers, receiveAToken, batchSize
        )


async def batchProcessLiquidation(
    w3: AsyncWeb3,
    account: LocalAccount,
    contract: AsyncContract,
    _borrowers: List[str],
    receiveAToken: bool,
    batchSize: int,
) -> None:

    borrowers: List[ChecksumAddress] = [
        w3.to_checksum_address(borrower) for borrower in _borrowers
    ]

    for i in range(0, len(borrowers), batchSize):
        batch: List[ChecksumAddress] = borrowers[i : i + batchSize]

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

        result: list[BaseException | bool] = await asyncio.gather(
            *task, return_exceptions=True
        )

        for i, error in enumerate(result):
            if isinstance(result, Exception):
                logger.error("User: %i, execute with error: %s", i, error)

        await asyncio.sleep(10)


async def processUser(
    w3: AsyncWeb3,
    account: LocalAccount,
    contract: AsyncContract,
    userAddress: ChecksumAddress,
    receiveAToken: bool,
) -> bool:
    try:
        logger.debug("User %s in process", userAddress)
        logger.debug("account: %s", account.address)
        logger.debug("contract: %s", contract.address)

        hf: int = await getHealthFactor(contract, userAddress)
        logger.debug("hf: %f, user address: %s", hf / 10**18, userAddress)

        if hf < 10**18:
            userDebtData: UserDebtData = await calculateMaxProfitableLiquidationData(
                contract, userAddress
            )
            txData: TxData = await LiquidationCall(
                w3, account, contract, userDebtData, receiveAToken
            )
            if txData.status == 1:
                logger.debug("User %s was liquidate", userAddress)
                return True
    except Exception as e:
        logger.error("Error processing %s: %s", userAddress, e)
    return False

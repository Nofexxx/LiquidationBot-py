import logging
from logging import Logger
from typing import Any, Tuple

from eth_account.datastructures import SignedTransaction
from eth_account.signers.local import LocalAccount
from eth_typing import ChecksumAddress
from hexbytes import HexBytes
from web3 import AsyncWeb3
from web3.contract import AsyncContract

from models.schemas.schemas import UserAccountData, UserDebtData
from utils.calculateGasPrice import calculateGasPrice

logger: Logger = logging.getLogger("botLogs")


async def getHealthFactor(contract: AsyncContract, userAddress: ChecksumAddress) -> int:
    data: Any = await contract.functions.getStructUserAccountData(userAddress).call()

    userAccountData: UserAccountData = UserAccountData.from_tuple(data)
    return userAccountData.healthFactor


async def calculateMaxProfitableLiquidationData(
    contract: AsyncContract, userAddress: ChecksumAddress
) -> UserDebtData:
    data: Any = await contract.functions.calculateMaxProfitableLiquidationData(
        userAddress
    ).call()

    calculatedData: UserDebtData = UserDebtData.from_tuple(data)

    logger.debug("Calculated data:")
    logger.debug("userAddress: %s", calculatedData.userAddress)
    logger.debug("collateralAssetAddress: %s", calculatedData.collateralAssetAddress)
    logger.debug("debtAssetAddress: %s", calculatedData.debtAssetAddress)
    logger.debug("debtToCover: %i", calculatedData.debtToCover)

    return calculatedData


async def LiquidationCall(
    w3: AsyncWeb3,
    account: LocalAccount,
    contract: AsyncContract,
    calculatedData: UserDebtData,
    receiveAToken: bool,
) -> HexBytes:
    tupleFromStruct: Tuple[str, str, str, int] = calculatedData.to_tuple()

    tx: Any = {
        "from": account.address,
        "gas": calculateGasPrice(),
        "gasPrice": await w3.eth.gas_price,
        "nonce": await w3.eth.get_transaction_count(account.address),
    }

    liquidation_tx: Any = await contract.functions.liquidationCall(
        tupleFromStruct, receiveAToken
    ).build_transaction(tx)

    signed_tx: SignedTransaction = account.sign_transaction(liquidation_tx)

    tx_hash_bytes: HexBytes = await w3.eth.send_raw_transaction(
        signed_tx.raw_transaction
    )
    receipt: Any = await w3.eth.get_transaction_receipt(tx_hash_bytes)

    tx_hash_hex: str = "0x" + tx_hash_bytes.hex()
    status: int = receipt.status
    gasUsed: int = receipt.gasUsed

    logger.debug("tx_hash_bytes: %s", tx_hash_hex)
    logger.debug("status: %i", status)
    logger.debug("gas used: %i", gasUsed)

    return tx_hash_bytes

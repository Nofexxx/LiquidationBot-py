from typing import Any, Dict

from dotenv import load_dotenv
from eth_account.signers.local import LocalAccount
from eth_typing import ChecksumAddress
from hexbytes import HexBytes
from web3 import Web3
from web3.contract import Contract

from models.schemas.schemas import UserAccountData, UserDebtData

load_dotenv()


async def getHealthFactor(contract: Contract, userAddress: ChecksumAddress) -> int:
    data: Dict[str, int] = contract.functions.getStructUserAccountData(
        userAddress
    ).call()
    userAccountData: UserAccountData = UserAccountData.from_Dict(data)

    return userAccountData.healthFactor


async def calculateMaxProfitableLiquidationData(
    contract: Contract, userAddress: ChecksumAddress
) -> UserDebtData:
    data: Dict[str, Any] = contract.functions.calculateMaxProfitableLiquidationData(
        userAddress
    ).call()
    calculatedData: UserDebtData = UserDebtData.from_Dict(data)

    return calculatedData


async def LiquidationCall(
    w3: Web3,
    account: LocalAccount,
    contract: Contract,
    calculatedData: UserDebtData,
    receiveAToken: bool,
) -> HexBytes:
    tx: Any = contract.functions.verifyLiquidationCall(
        calculatedData, receiveAToken
    ).build_transaction(
        {
            "from": account.address,
            "nonce": w3.eth.get_transaction_count(account.address),
            "gas": w3.eth.estimate_gas(
                {
                    "from": account.address,
                    "to": contract.address,
                }
            ),
            "gasPrice": w3.eth.gas_price,
            "chainId": 1,
        }
    )

    signed_tx: Any = w3.eth.account.sign_transaction(tx, account.key)

    tx_hash: HexBytes = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    return tx_hash

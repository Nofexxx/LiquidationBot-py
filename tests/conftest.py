from typing import List

import pytest
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
from scripts.web3_config import getAccount, getContract, getWeb3Provider
from utils.db_service import getAddressUsersFromDb

LIQUIDATION_CONTRACT_ADDRESS: ChecksumAddress = AsyncWeb3.to_checksum_address(
    "0x77AD263Cd578045105FBFC88A477CAd808d39Cf6"
)

"""Fixtures for web3_config"""


@pytest.fixture(scope="session")
async def web3_client():
    w3: AsyncWeb3 = await getWeb3Provider()

    yield w3


@pytest.fixture(scope="function")
async def account() -> LocalAccount:
    return await getAccount()


@pytest.fixture(scope="function")
async def contract(web3_client: AsyncWeb3) -> AsyncContract:
    return await getContract(
        web3_client, LIQUIDATION_CONTRACT_ADDRESS, "liquidation.json"
    )


"""Fixture for db_service"""


@pytest.fixture(scope="function")
async def addressesUsersFromDb(web3_client: AsyncWeb3) -> List[ChecksumAddress]:
    _borrowers: List[str] = await getAddressUsersFromDb()
    borrowers: List[ChecksumAddress] = [
        web3_client.to_checksum_address(borrower) for borrower in _borrowers
    ]
    return borrowers


"""Fixture for getHealthFactor"""


@pytest.fixture(scope="function")
async def healthFactor(
    contract: AsyncContract, addressesUsersFromDb: List[ChecksumAddress]
) -> int:
    return await getHealthFactor(contract, addressesUsersFromDb[0])


@pytest.fixture(scope="function")
async def getUserDebtData(
    contract: AsyncContract, addressesUsersFromDb: List[ChecksumAddress]
) -> UserDebtData:
    return await calculateMaxProfitableLiquidationData(
        contract, addressesUsersFromDb[0]
    )


@pytest.fixture(scope="function")
async def liquidateUser(
    web3_client: AsyncWeb3,
    account: LocalAccount,
    contract: AsyncContract,
    getUserDebtData: UserDebtData,
) -> TxData:
    receiveAToken: bool = True
    return await LiquidationCall(
        web3_client, account, contract, getUserDebtData, receiveAToken
    )

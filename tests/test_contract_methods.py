from typing import Tuple

import pytest
from eth_account.signers.local import LocalAccount
from eth_typing import ChecksumAddress
from web3 import AsyncWeb3
from web3.contract import AsyncContract

from models.schemas.schemas import UserDebtData
from scripts.contract_methods import LiquidationCall
from scripts.web3_config import getContract

WETH_ADDRESS_CONTRACT: ChecksumAddress = AsyncWeb3.to_checksum_address(
    "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
)


@pytest.mark.asyncio
async def test_getHealthFactor(healthFactor: int):
    validHealthFactorRange: Tuple[int, int] = (624275000000000000, 624275699999999999)

    assert healthFactor >= validHealthFactorRange[0]
    assert healthFactor <= validHealthFactorRange[1]


@pytest.mark.asyncio
async def test_calculateMaxProfitableLiquidationData(getUserDebtData: UserDebtData):
    validUserAddress: str = "0x70997970C51812dc3A010C7d01b50e0d17dc79C8"
    validCollateralAddress: str = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
    validDebtAssetAddress: str = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
    validDebtToCoverRange: Tuple[int, int] = (11463188000, 11463188999)

    assert getUserDebtData.userAddress == validUserAddress
    assert getUserDebtData.collateralAssetAddress == validCollateralAddress
    assert getUserDebtData.debtAssetAddress == validDebtAssetAddress
    assert getUserDebtData.debtToCover >= validDebtToCoverRange[0]
    assert getUserDebtData.debtToCover <= validDebtToCoverRange[1]


@pytest.mark.asyncio
async def test_liquidateUser(
    web3_client: AsyncWeb3,
    account: LocalAccount,
    contract: AsyncContract,
    getUserDebtData: UserDebtData,
):

    wethContract: AsyncContract = await getContract(
        web3_client, WETH_ADDRESS_CONTRACT, "weth.json"
    )

    balanceLiquidationContractBefore = await wethContract.functions.balanceOf(
        "0x77AD263Cd578045105FBFC88A477CAd808d39Cf6"
    ).call()

    receiveAToken: bool = False

    await LiquidationCall(
        web3_client, account, contract, getUserDebtData, receiveAToken
    )

    balanceLiquidationContractAfter = await wethContract.functions.balanceOf(
        "0x77AD263Cd578045105FBFC88A477CAd808d39Cf6"
    ).call()

    assert balanceLiquidationContractBefore < balanceLiquidationContractAfter

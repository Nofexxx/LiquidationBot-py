from typing import Any

import pytest
from eth_account.signers.local import LocalAccount
from eth_typing import BlockNumber
from web3 import AsyncWeb3
from web3.contract import AsyncContract


@pytest.mark.asyncio
async def test_getWeb3Provider(web3_client: AsyncWeb3):
    block: BlockNumber = await web3_client.eth.block_number
    chainId: int = await web3_client.eth.chain_id

    blockNumberFromSetup: int = 17944912
    rightChainId: int = 1

    assert block >= blockNumberFromSetup
    assert chainId == rightChainId


@pytest.mark.asyncio
async def test_getAccount(account: LocalAccount):
    rightAccountAddress: str = "0x3C44CdDdB6a900fa2b585dd299e03d12FA4293BC"

    assert account.address == rightAccountAddress


@pytest.mark.asyncio
async def test_getContract(web3_client: AsyncWeb3, contract: AsyncContract):
    code: Any = await web3_client.eth.get_code(contract.address)

    assert len(code) > 2

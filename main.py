import asyncio
import logging
from logging import Logger

from eth_account.signers.local import LocalAccount
from eth_typing import ChecksumAddress
from web3 import AsyncWeb3
from web3.contract import AsyncContract

from scripts.logs_config import configureLogs
from scripts.web3_config import getAccount, getContract, getWeb3Provider
from src.bot import run_process

logger: Logger = logging.getLogger("botLogs")

LIQUIDATION_CONTRACT_ADDRESS: ChecksumAddress = AsyncWeb3.to_checksum_address(
    "0x77AD263Cd578045105FBFC88A477CAd808d39Cf6"
)


async def main():
    configureLogs()

    w3: AsyncWeb3 = await getWeb3Provider()
    account: LocalAccount = await getAccount()
    contract: AsyncContract = await getContract(
        w3, LIQUIDATION_CONTRACT_ADDRESS, "liquidation.json"
    )

    receiveAToken: bool = False
    batchSize: int = 3

    try:
        logger.info("Start working...")
        await run_process(
            w3=w3,
            account=account,
            contract=contract,
            receiveAToken=receiveAToken,
            batchSize=batchSize,
        )

    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.critical("Critical error: %s", e)


if __name__ == "__main__":
    asyncio.run(main())

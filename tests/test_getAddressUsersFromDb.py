from typing import List

import pytest
from eth_typing import ChecksumAddress


@pytest.mark.asyncio
async def test_getUsersAddresses(addressesUsersFromDb: List[ChecksumAddress]):
    assert addressesUsersFromDb[0] == "0x70997970C51812dc3A010C7d01b50e0d17dc79C8"

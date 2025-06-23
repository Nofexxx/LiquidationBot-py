from sqlalchemy import select

from models.db.db_model import Borrow
from scripts.db_config import get_db_session


async def getAddressUsersFromDb() -> list[str]:
    async with get_db_session() as session:
        user = await session.execute(select(Borrow.user_address.distinct()))
        return list(user.scalars().all())

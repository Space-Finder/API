import asyncio
from prisma import Prisma
from prisma.models import User


async def main() -> None:
    db = Prisma(
        datasource={
            "url": "file:./src/core/db/database.db",
        },
        auto_register=True,
    )
    await db.connect()

    _ = await User.prisma().create(
        data={"name": "Test User", "email": "the.test@testing.testeer"},
    )

    await db.disconnect()


if __name__ == "__main__":
    asyncio.run(main())

__all__ = ("prisma",)

import os

from prisma import Prisma
from dotenv import load_dotenv

load_dotenv()

prisma = Prisma(datasource={"url": os.environ["DATABASE_URL"]})

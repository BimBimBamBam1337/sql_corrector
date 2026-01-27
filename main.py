import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

from sql_corrector import SQLSchemaCorrector


load_dotenv()
PROD_POSTGRES_DSN = os.getenv("PROD_POSTGRES_DSN")
TEST_POSTGRES_DSN = os.getenv("TEST_POSTGRES_DSN")

test_engine = create_engine(TEST_POSTGRES_DSN)
prod_engine = create_engine(PROD_POSTGRES_DSN)
corrector = SQLSchemaCorrector(prod_engine=prod_engine, test_engine=test_engine)


def main():
    corrector.run(True)


if __name__ == "__main__":
    main()

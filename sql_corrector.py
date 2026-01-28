from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.engine import Engine
from sqlalchemy.sql.schema import Table


class SQLSchemaCorrector:
    """
    Класс для сравнения структуры базы данных и генерации sql-миграций.
    """

    def __init__(self, test_engine: Engine, prod_engine: Engine):
        self.test_engine = test_engine
        self.prod_engine = prod_engine

    def load_schema(self, engine: Engine) -> MetaData:
        """
        Функция для получения структуры в базе данных

        :param engine: sqlalchemy Engine для подключения к БД
        :return: MetaData с отражённой схемой базы данных
        """

        metadata = MetaData()
        metadata.reflect(bind=engine)
        return metadata

    def compare_columns(self, test_table: Table, prod_table: Table) -> list[str]:
        """
        Функция для нахождения различий в базе дaнных


        :param test_table: Таблица из test базы данных
        :param prod_table: Таблица из prod базы данных
        :return: список sql зпросов (ALTER TABLE ...)
        """
        statements = []

        test_columns = test_table.columns
        prod_columns = prod_table.columns

        for col_name, test_col in test_columns.items():
            if col_name not in prod_columns:
                sql = f"ALTER TABLE {test_table.name} ADD COLUMN {col_name} {test_col.type}"
                statements.append(sql)

        return statements

    def generate_migration(
        self,
        test_meta: MetaData,
        prod_meta: MetaData,
    ) -> list[str]:
        """
        Генерирует список sql-миграций для синхронизации схем.

        :param test_meta: MetaData test базы
        :param prod_meta: MetaData prod базы
        :return: список sql-запросов для миграции
        """
        sql_statements = []

        for table_name, test_table in test_meta.tables.items():
            if table_name not in prod_meta.tables:
                continue

            prod_table = prod_meta.tables[table_name]
            sql_statements.extend(self.compare_columns(test_table, prod_table))

        return sql_statements

    def apply_migration(self, engine: Engine, statements: list[str]):
        """
        Применяет SQL-миграции к базе данных.

        :param engine: Engine базы данных, к которой применяется миграция
        :param statements: Список sql-запросов
        """
        try:
            with engine.begin() as conn:
                for statement in statements:
                    conn.execute(text(statement))
        except Exception as e:
            print(f"Возникла ошибка: {e}")

    def run(self, apply: bool = False):
        """
        Запускает процесс сравнения и миграции схемы.

        :param apply: Флаг применения миграций
        """
        test_meta = self.load_schema(self.test_engine)
        prod_meta = self.load_schema(self.prod_engine)

        sql = self.generate_migration(test_meta, prod_meta)

        if not apply:
            print("Изменения, которые будут внесены")
            for s in sql:
                print(s)
        else:
            self.apply_migration(self.prod_engine, sql)

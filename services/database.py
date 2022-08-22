
class Database:
    def __init__(self, engine):
        self.engine = engine
        pass

    def insert_raw_json(self, table_name: str, raw_json: str, schema: str = 'public'):
        with self.engine.connect() as conn:
            insert_query = f"""
                INSERT INTO {schema}.{table_name} (json_data)
                VALUES ('{raw_json}')
            """
            conn.execute(insert_query)

            select_query = f"SELECT id FROM {schema}.{table_name} order by collected_on DESC"
            raw_json_pk = conn.execute(select_query).first()
            return raw_json_pk[0]

    def update(self, table_name: str, **kwargs):
        pass

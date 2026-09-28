from sqlalchemy import create_engine

def get_engine(database_url: str):
    return create_engine(database_url, pool_pre_ping=True)

def write_frame(df, table_name: str, database_url: str, if_exists="append") -> int:
    engine = get_engine(database_url)
    with engine.begin() as conn:
        df.to_sql(table_name, conn, if_exists=if_exists, index=False, method="multi", chunksize=5000)
    return len(df)

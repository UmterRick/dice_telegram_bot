import aiopg


async def init_db():
    conn = await aiopg.connect(
        database='telegram_bot_db',
        user='postgres',
        password='postgres',
        host='127.0.0.1'
    )

    cursor = await conn.cursor()
    await cursor.execute("""
    CREATE TABLE IF NOT EXISTS games_results (
    game_id serial PRIMARY KEY,
    chat_id INTEGER NOT NULL,
    user_score INTEGER default 0,
    bot_score INTEGER default 0,
    game_type VARCHAR(50),
    timestamp TIMESTAMP NOT NULL,
    )
    """
                         )
    await conn.close()


async def get_conn():
    conn = await aiopg.connect(
        database='telegram_bot_db',
        user='postgres',
        password='postgres',
        host='127.0.0.1'
    )
    return conn

from datetime import datetime, timezone
import aiosqlite

DB_PATH = "logs.db"

async def init_db() -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("CREATE TABLE IF NOT EXISTS requests_logs (" \
        "id INTEGER PRIMARY KEY AUTOINCREMENT," \
        "timestamp TEXT NOT NULL," \
        "prompt TEXT NOT NULL," \
        "response TEXT," \
        "latency_ms REAL NOT NULL," \
        "status TEXT Not NULL)")

        await db.commit()

async def log_request(
    prompt: str,
    response: str | None,
    latency_ms: float,
    status: str = "success",
) -> None:
    timestamp = datetime.now(timezone.utc).isoformat()
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """
            INSERT INTO requests_logs (timestamp, prompt, response, latency_ms, status)
            VALUES (?, ?, ?, ?, ?)
            """,
            (timestamp, prompt, response, round(latency_ms, 2), status))

        await db.commit()

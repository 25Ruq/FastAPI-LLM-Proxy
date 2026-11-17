import logging
import os
import backoff
import httpx

logger = logging.getLogger("requests_logger")

API_BASE_URL = os.getenv("LLM_BASE_URL")
MODEL_ID = os.getenv("LLM_MODEL")


@backoff.on_exception(
    backoff.expo,
    (httpx.HTTPStatusError, httpx.RequestError, httpx.TimeoutException),
    max_tries=4,
    on_backoff=lambda details: logger.warning(
        f"LLM request failed. Retrying in {details['wait']:.1f}s (Attempt {details['tries']})..."
    ),
)
async def generate_response(prompt:str)-> str:
    api_key = os.getenv("LLM_API_KEY")
    if not api_key:
        raise RuntimeError("LLM_API_KEY environment variable is not set.")

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            f"{API_BASE_URL}/chat/completions",
            json={
                "model": MODEL_ID,
                "messages": [{"role": "user", "content": prompt}],
                "stream": False,
            },
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
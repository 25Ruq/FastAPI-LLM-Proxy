# FastAPI LLM Proxy

A lightweight, asynchronous, and provider-agnostic FastAPI proxy service for OpenAI-compatible Large Language Model (LLM) APIs. Built with persistent SQLite request logging, exponential backoff retries, and centralized environment configuration.

## Installation & Setup

1. **Clone the repository and navigate to the project directory:**

   ```
   git clone <your-repository-url>
   cd <project-folder>
   
   ```

2. **Create and activate a virtual environment:**

   ```
   # Windows (PowerShell)
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   
   # macOS / Linux
   python3 -m venv venv
   source venv/bin/activate
   
   ```

3. **Install dependencies:**

   ```
   pip install -r requirements.txt
   
   ```

4. **Configure environment variables:**
   Create a `.env` file in the root directory and configure your target provider:

   ```
   # API Authentication
   LLM_API_KEY=your_api_key_here
   
   # LLM Configuration (Example: Google AI Studio Free Tier)
   LLM_MODEL=gemini-2.5-flash
   LLM_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/

## Running the Server

Start the FastAPI application using Uvicorn:

```
uvicorn main:app --reload

```

The server will start at `http://127.0.0.1:8000` and automatically initialize `logs.db`. Interactive API documentation (Swagger UI) is available at `http://127.0.0.1:8000/docs`.

## API Usage

### `POST /chat`

Sends a prompt to the configured LLM provider and logs the transaction to SQLite.

**Request Body:**

```
{
  "prompt": "Explain asynchronous programming in two sentences."
}

```

**Example Request (`curl` on Windows PowerShell):**

```
curl.exe -X POST "http://127.0.0.1:8000/chat" `
     -H "Content-Type: application/json" `
     -d '{\"prompt\": \"Say hello in three words.\"}'

```

**Example Request (`curl` on macOS / Linux):**

```
curl -X POST "http://127.0.0.1:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Say hello in three words."}'

```

**Example Response:**

```
{
  "response": "Hello there, friend!",
  "latency_ms": 412.5
}

```
## Database & Analytics (`stats.sql`)

The proxy automatically creates and logs every request into a local SQLite database (`logs.db` by default).

### Daily Usage and Latency Summary

The `stats.sql` file contains a query that aggregates your request logs by day, printing the total number of requests handled and the average response latency in milliseconds for each active day.

#### `stats.sql`
```sql
SELECT
    DATE(timestamp) AS day,
    COUNT(*) AS total_requests,
    ROUND(AVG(latency_ms), 2) AS avg_latency_ms
FROM request_logs
GROUP BY DATE(timestamp)
ORDER BY day DESC;
```

#### How to Run `stats.sql`
  ```bash
  sqlite3 -header -column logs.db < stats.sql
  ```

## Switching Providers

No code changes are required to switch LLM providers. Update `LLM_API_KEY`, `LLM_MODEL`, and `LLM_BASE_URL` in your `.env` file and restart the Uvicorn server:

| Provider | `LLM_BASE_URL` | Example `LLM_MODEL` | 
| ----- | ----- | ----- | 
| **Google AI Studio (Free)** | `https://generativelanguage.googleapis.com/v1beta/openai/` | `gemini-2.5-flash` | 
| **Groq (Free Tier)** | `https://api.groq.com/openai/v1` | `llama-3.3-70b-versatile` | 
| **OpenRouter (Free Tier)** | `https://openrouter.ai/api/v1` | `openrouter/free` | 
| **OpenAI** | `https://api.openai.com/v1` | `gpt-4o-mini` | 

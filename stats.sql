SELECT
    DATE(timestamp) AS day,
    COUNT(*) AS total_requests,
    ROUND(AVG(latency_ms), 2) AS avg_latency_ms
FROM request_logs
GROUP BY DATE(timestamp)
ORDER BY day DESC;
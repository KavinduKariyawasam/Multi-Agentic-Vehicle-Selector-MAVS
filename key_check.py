import os, requests, json
payload = {
    "model": "llama3-70b-8192",
    "messages": [{"role":"user", "content":"hello"}]
}
r = requests.post(
    "https://api.groq.com/openai/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {os.environ['GROQ_API_KEY']}",
        "Content-Type": "application/json",
    },
    data=json.dumps(payload),
    timeout=30,
)
print(r.status_code, r.text)

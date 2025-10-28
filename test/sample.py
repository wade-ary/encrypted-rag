import ollama
response = ollama.chat(
    model="mistral",
    messages=[{"role": "user", "content": "3 funny jokes"}]
)

print(response["message"]["content"])
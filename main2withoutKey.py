import os
from openai import OpenAI

client = OpenAI(api_key="")

def load_data(folder_path):
    data = {}
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if filename.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                data[filename] = f.read()
    return data

def chunk_text(text, chunk_size=1000):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

folder = "data"
files_data = load_data(folder)

chunks = []
for name, content in files_data.items():
    file_chunks = chunk_text(content)
    for i, chunk in enumerate(file_chunks):
        chunks.append({
            "file": name,
            "index": i,
            "content": chunk
        })

print(f"Загружено {len(files_data)} файлов, создано {len(chunks)} чанков.")

while True:
    user_input = input("\nВопрос: ")
    if user_input.lower() in ["q", "й"]:
        break

    words = [w.lower() for w in user_input.split()]
    scored_chunks = []

    for ch in chunks:
        score = sum(ch["content"].lower().count(w) for w in words)
        if score > 0:
            scored_chunks.append((score, ch))

    scored_chunks.sort(reverse=True, key=lambda x: x[0])
    selected_chunks = [ch for _, ch in scored_chunks[:5]]

    if not selected_chunks:
        selected_chunks = chunks[:5]

    print("\nИспользуемые чанки:")
    for ch in selected_chunks:
        print(f"- {ch['file']} часть {ch['index']}")

    context = "\n\n".join([f"[{ch['file']} - часть {ch['index']}]\n{ch['content']}" for ch in selected_chunks])

    messages = [
        {"role": "system", "content": "Ты аналитик художественных произведений. Отвечай кратко и по существу."},
        {"role": "user", "content": f"Вот выдержки из файлов:\n{context}"},
        {"role": "user", "content": f"Вопрос пользователя: {user_input}"}
    ]

    response = client.chat.completions.create(
        model="gpt-5-nano",
        messages=messages
    )

    print("\nОтвет:", response.choices[0].message.content)

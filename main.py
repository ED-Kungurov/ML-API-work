import os
from openai import OpenAI

client = OpenAI(api_key="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")

def load_data(folder_path):
    data = {}
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if filename.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                data[filename] = f.read()
    return data

folder = "data"
files_data = load_data(folder)
summary_text = "\n\n".join([f"Файл: {name}\nСодержимое:\n{content}" for name, content in files_data.items()])

print(f"Загружено {len(files_data)} файлов.")
while True:
    user_input = input("\nВопрос:")
    if user_input.lower() in ["exit", "quit", "q", "й"]:
        break

    messages = [
        {"role": "system", "content": "Ты аналитик разных художественных произведений"},
        {"role": "user", "content": f"Вот содержимое файлов компании:\n{summary_text}"},
        {"role": "user", "content": user_input}
    ]

    response = client.chat.completions.create(
        model="gpt-5-nano",
        messages=messages
    )

    print("\nОтвет:", response.choices[0].message.content)
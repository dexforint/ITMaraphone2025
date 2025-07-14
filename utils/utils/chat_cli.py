# chat_cli.py
import os
import openai

MODEL = "gpt-3.5-turbo"  # или "gpt-4o-mini" / "gpt-4o"
TEMPERATURE = 0.7  # насколько креативные ответы


def main():
    # 1) Базовая "система"-реплика описывает роль ассистента
    messages = [
        {"role": "system", "content": "Ты — дружелюбный русскоязычный ассистент."}
    ]

    print("🤖 Чат-бот запущен! Для выхода напишите /exit\n")

    while True:
        user_input = input("👤 Вы: ").strip()
        if user_input.lower() in ("/exit", "exit", "quit", "q"):
            print("До встречи!")
            break

        # 2) Добавляем сообщение пользователя в историю
        messages.append({"role": "user", "content": user_input})

        try:
            # 3) Отправляем всю историю в API
            response = openai.ChatCompletion.create(
                model=MODEL,
                messages=messages,
                temperature=TEMPERATURE,
                stream=False,  # можно True — тогда получите поток
            )
        except openai.error.OpenAIError as e:
            print(f"Ошибка OpenAI: {e}")
            continue

        # 4) Извлекаем ответ ассистента
        assistant_reply = response.choices[0].message.content.strip()

        # 5) Сохраняем его в историю и печатаем
        messages.append({"role": "assistant", "content": assistant_reply})
        print(f"🤖 Бот: {assistant_reply}\n")


if __name__ == "__main__":
    main()

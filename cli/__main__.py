from pygments.lexers import get_lexer_by_name, guess_lexer, PythonLexer, TextLexer
from pygments.formatters import TerminalFormatter
from pygments import highlight
from dotenv import load_dotenv
from groq import Groq
import re

load_dotenv()

GREEN = "\033[0;32m"
RED = "\033[0;31m"
BLUE = "\033[0;34m"
YELLOW = "\033[0;33m"
NC = "\033[0m"  # No Color

assistant_prompt = "you are a helpful assistant."
model_name = "llama-3.2-90b-vision-preview"
temperature_setting = 0.75

messages = [{"role": "system", "content": assistant_prompt}]


def configure_settings():
    global assistant_prompt, model_name, temperature_setting
    while True:
        menu = input(
            f"menu:\n\n1. Assistant prompt: {assistant_prompt}.\n2. Model: {model_name}.\n3. Temperature: {temperature_setting}.\n\nSilahkan pilih: "
        )

        if menu == "1":
            assistant_prompt = input("Masukkan prompt baru: ")
        elif menu == "2":
            model_name = input("Masukkan model baru: ")
        elif menu == "3":
            temperature_setting = float(input("Masukkan temperature baru: "))
        else:
            return

        messages.append({"role": "system", "content": assistant_prompt})


def format_content(content):
    formatted_content = f"{GREEN}### Bot Response ###\n{NC}"
    parts = re.split(r"(```.*?```|`.*?`)", content, flags=re.DOTALL)

    for part in parts:
        if part.startswith("```") and part.endswith("```"):
            code = part[3:-3].strip()
            formatted_content += f"```\n{code}\n```\n\n"
        elif part.startswith("`") and part.endswith("`"):
            code = part[1:-1].strip()
            formatted_content += f"`{code}`"
        else:
            formatted_content += part

    return formatted_content


def log_content(content):
    parts = re.split(r"(```(\w+)?\n.*?```|`.*?`)", content, flags=re.DOTALL)
    for part in parts:
        if part is None:
            continue  # Skip None values
        elif part.startswith("```") and part.endswith("```"):
            lines = part.strip("`").split("\n", 1)
            lang = lines[0] if len(lines) > 1 and lines[0] else None
            code = lines[1] if len(lines) > 1 else ""
            try:
                lexer = get_lexer_by_name(lang) if lang else guess_lexer(code)
            except:
                lexer = PythonLexer()
            highlighted_code = highlight(code, lexer, TerminalFormatter())
            print(highlighted_code, end="")
        elif part.startswith("`") and part.endswith("`"):
            code = part.strip("`")
            try:
                lexer = guess_lexer(code)
            except:
                lexer = TextLexer()
            highlighted_code = highlight(code, lexer, TerminalFormatter())
            print(highlighted_code, end="")
        else:
            print(part, end="")
    print()


def main():
    global assistant_prompt, model_name, temperature_setting
    client = Groq()

    while True:
        user_input = input(f"{BLUE}User{NC}: ")

        if user_input.strip().upper() == "MENU":
            configure_settings()
            continue
        elif user_input.strip().upper() == "Q":
            print(f"{YELLOW}Mengakhiri percakapan...{NC}")
            break

        if len(user_input.strip()) < 3:
            print(f"{RED}Pesan terlalu pendek. Masukkan minimal 3 karakter.{NC}")
            continue
        messages.append(
            {"role": "user", "content": user_input},
        )

        try:
            chat_completion = client.chat.completions.create(
                messages=messages,
                model=model_name,
                temperature=temperature_setting,
                max_tokens=1024,
                top_p=1,
                stop=None,
                stream=False,
            )

            response = chat_completion.choices[0].message.content
            formatted_response = format_content(response)
            log_content(formatted_response)

            messages.append({"role": "assistant", "content": response})

        except Exception as e:
            print(f"{RED}Terjadi error saat memproses permintaan: {e}{NC}")
            continue


if __name__ == "__main__":
    main()

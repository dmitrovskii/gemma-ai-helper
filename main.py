import os
import pathlib
import json
from google import genai
from collections import deque

ROOT = pathlib.Path(__file__).resolve().parent

class GoogleTerminalGets:
    def __init__(self, api_key, model_name="gemma-3-27b-it"):
        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name
        self._config = None

    @property
    def config(self):
        file_conf = pathlib.Path(ROOT / 'config' / 'config.txt')
        file_conf.touch(exist_ok=True)
        self._config = file_conf.read_text(encoding='utf-8')
        return self._config

    def ask(self, prompt):
        full_response = ''
        try:
            print("\n[Gemma]: ", flush=True)
            response = self.client.models.generate_content_stream(
                model = self.model_name, 
                contents= f"### Instruction ###\n{self.config}\n\n### Question ###\n{prompt}"
            )

            for chunk in response:
                if chunk.text:
                    print(chunk.text, end="", flush=True)
                    full_response += chunk.text
            print("\n")
            return full_response

        except Exception as e:
            print(f"\r\033[31m[Помилка API]: {e}\033[0m\n")

    def save_response(self, info):
        with open(ROOT / 'context.json', 'w', encoding='utf-8') as f:
            json.dump(list(info), f, indent=4, ensure_ascii=False)

def main():
    GEMINI_API_KEY = (ROOT / 'key.txt').read_text(encoding='utf-8').strip()
    grequest = GoogleTerminalGets(GEMINI_API_KEY)
    window = deque(maxlen=20)
    try:
        while True:
            prompt = input("[You]: ")
            response = grequest.ask(prompt)
            data_to_save = [
                {"role": "user", "parts": prompt},
                {"role": "model", "parts": response}
            ]
            window.extend(data_to_save)

    except KeyboardInterrupt:
        print("\nClosing program...")
    finally: 
        grequest.save_response(window)

if __name__ == '__main__':
    main()


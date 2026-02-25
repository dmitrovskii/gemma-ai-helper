import os
import pathlib
from google import genai

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
        try:
            print("\n[Gemma]: ", flush=True)
            response = self.client.models.generate_content_stream(
                model = self.model_name, 
                contents= f"### Instruction ###\n{self.config}\n\n### Question ###\n{prompt}"
            )

            for chunk in response:
                if chunk.text:
                    print(chunk.text, end="", flush=True)
            print("\n")
        except Exception as e:
            print(f"\r\033[31m[Помилка API]: {e}\033[0m\n")

def main():
    GEMINI_API_KEY = (ROOT / 'key.txt').read_text(encoding='utf-8').strip()
    grequest = GoogleTerminalGets(GEMINI_API_KEY)
    try:
        while True:
            user = input("[You]: ")
            grequest.ask(user)

    except KeyboardInterrupt:
        print("\nClosing program...")

if __name__ == '__main__':
    main()


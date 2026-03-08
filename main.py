import pathlib
import json
import platform
from google import genai
from collections import deque

ROOT = pathlib.Path(__file__).resolve().parent

class GoogleTerminalGets:
    def __init__(self, model_name="gemma-3-27b-it"):
        self.client = genai.Client(api_key=self.key)
        self.model_name = model_name
        self._config = None
        self._key = None

    @property
    def key(self):
        if hasattr(self, '_key') and self._key:
            return self._key

        home = pathlib.Path.home()
        if platform.system() == 'Windows':
            key_path = home / "AppData" / "Roaming" / "gemini" / "key.txt"
        else:
            key_path = home / ".config" / "gemini" / "key.txt"
        
        key_path.parent.mkdir(parents=True, exist_ok=True)

        if not key_path.exists():
            key_path.touch()
            print(f"The key.txt file has been created in {key_path}.")
            print("Please insert into file your API-key")

        self._key = key_path.read_text(encoding='utf-8')
        return self._key

    @property
    def config(self):
        if hasattr(self, '_config') and self._config:
            return self._config
        
        file_conf = pathlib.Path(ROOT / 'config' / 'config.txt')
        file_conf.touch(exist_ok=True)
        self._config = file_conf.read_text(encoding='utf-8')
        return self._config

    def ask(self, prompt: str) -> str:
        try:
            response = self.client.models.generate_content(
                model = self.model_name, 
                contents = [self.config, prompt]
            )
            return response.text

        except Exception as e:
            print(f"\r\033[31m[Помилка API]: {e}\033[0m\n")

    def save_response(self, info: list) -> None:
        with open(ROOT / 'context.json', 'w', encoding='utf-8') as f:
            json.dump(list(info), f, indent=4, ensure_ascii=False)

def main():
    grequest = GoogleTerminalGets()
    try:
        while True:
            prompt = input("[You]: ")
            response = grequest.ask(prompt)
            print(f"\n[Gemma]: {response}")

    except KeyboardInterrupt:
        print("\nClosing program...")

if __name__ == '__main__':
    main()


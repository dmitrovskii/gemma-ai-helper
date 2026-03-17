import pathlib
import json
import platform
from collections import deque
from google import genai

ROOT = pathlib.Path(__file__).resolve().parent

class GoogleTerminalGets:
    def __init__(self, model_name="gemma-3-27b-it"):
        self._key = None
        self._instruct = None
        self.model_name = model_name
        self.client = genai.Client(api_key=self.key)

    @property
    def key(self):
        if self._key is None:
            self._key = self._key_load()
        return self._key

    def _key_load(self):
        home = pathlib.Path.home()
        if platform.system() == 'Windows':
            key_path = home / "AppData" / "Roaming" / "gemini" / "key.txt"
        else:
            key_path = home / ".config" / "gemini" / "key.txt"
        
        key_path.parent.mkdir(parents=True, exist_ok=True)

        if not key_path.exists():
            key_path.touch()
            print(f"The key.txt file has been created in {key_path}.\nPlease insert into file your API-key")
        return key_path.read_text(encoding='utf-8').strip()

    @property
    def instruct(self):
        if self._instruct is None:
            self._instruct = self._instruct_load()
        return self._instruct

    def _instruct_load(self):
        file_conf = pathlib.Path(ROOT / 'config' / 'config.txt')
        file_conf.touch(exist_ok=True)
        return file_conf.read_text(encoding='utf-8') 

    def ask(self, data: str) -> str:
        try:
            response = self.client.models.generate_content(
                model = self.model_name, 
                contents = data
            )
            return response.text

        except Exception as e:
            print(f"\r\033[31m[Error API]: {e}\033[0m\n")

class ChatMemory:
    def __init__(self, filepath="context.json", max_len=20):
        self.filepath = pathlib.Path(ROOT / filepath)
        self.max_len = max_len
        self._history = None

    @property
    def history(self):
        if self._history is None:
            self._history = self._history_load()
        return self._history

    def _history_load(self):
        if self.filepath.exists(): 
            try:
                with open(self.filepath, "r", encoding='utf-8') as f:
                    data = json.load(f)
                    return deque(data, maxlen=self.max_len)
                
            except Exception as e:
                print(f"The error is: {e}")
                return deque([], maxlen=self.max_len)
        else:
            print(f"File '{self.filepath}' is not found.")
            self.filepath.touch(exist_ok=True)
            return deque([], maxlen=self.max_len)
    
    def save_history(self, data: list) -> None:
        with open(self.filepath, "w") as f:
            json.dump(list(data), f, indent=4, ensure_ascii=False)

    def convert(self, data: list) -> list:
        return [{"role": d.role, "parts": d.parts[0].text} for d in data]

    def deconvert(self, json_data: list) -> list:
        deconvert_data = []
        for item in json_data:
            content = genai.types.Content(role=item["role"], parts=[genai.types.Part(text=item["parts"])])
            deconvert_data.append(content)
        return deconvert_data
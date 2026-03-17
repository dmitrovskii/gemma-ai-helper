from engine import GoogleTerminalGets
from engine import ChatMemory
from google.genai import types

def main():

    model = GoogleTerminalGets()
    chat = ChatMemory() 

    try:
        instructions = [
            types.Content(role="user", parts=[types.Part(text=f"SYSTEM INSTRUCTION: {model.instruct}")])
        ]
        
        history = chat.history
        
        while True:
            user_text = input("[User]: ")
            history.extend([
                types.Content(role="user", parts=[types.Part(text=user_text)])
            ])

            response = model.ask(
                [*instructions, *history]
            )  

            history.extend([
                types.Content(role="user", parts=[types.Part(text=response)])
            ])

            print(f"\n[Model]: {response}")

    except KeyboardInterrupt:
        print("\nClose...")
    finally:
        chat.save_history(chat.convert(history))

if __name__ == '__main__':
    main()


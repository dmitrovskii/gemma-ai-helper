from genai import GoogleTerminalGets

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


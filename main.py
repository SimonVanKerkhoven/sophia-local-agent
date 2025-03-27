from memory_manager import init_db
from sophia_agent import ask_sophia

def main():
    init_db()
    print("Bienvenue dans SophiaBot - Agent relecteur 🧠🐍")
    print("Tape 'exit' pour quitter")

    while True:
        user_input = input("\nVous: ")
        if user_input.strip().lower() == 'exit':
            print("À bientôt !")
            break

        reply = ask_sophia(user_input)
        print("\nSophiaBot :", reply)

if __name__ == "__main__":
    main()

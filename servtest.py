import subprocess

def menu():
    while True:
        print("1. Start server")
        print("2. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            num_players = input("Enter number of players: ")
            print("Starting server...")
            subprocess.Popen(["python", "player.py", num_players])
            print("Server started.")
        elif choice == "2":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    menu()

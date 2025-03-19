import xmlrpc.client

def client():
    proxy = xmlrpc.client.ServerProxy("http://localhost:8000")
    while True:
        print("\nClient")
        print("1. Add a note")
        print("2. Get all notes")
        print("3. Fetch Wikipedia data")
        print("4. Exit")
        choice = input("Enter choice: ")
        
        if choice == "1":
            topic = input("Enter topic: ")
            text = input("Enter note text: ")
            print(proxy.add_note(topic, text))
        elif choice == "2":
            topic = input("Enter topic: ")
            print(proxy.get_notes(topic))
        elif choice == "3":
            topic = input("Enter topic: ")
            print(proxy.fetch_wikipedia(topic))
        elif choice == "4":
            print("Exiting client...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    client()
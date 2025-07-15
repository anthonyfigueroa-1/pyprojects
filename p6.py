def checktxt(contacts, fileexist):
    with open("contacts.txt", "r")as file:   
        for line in file:
            cleanedline = line.strip()
            name, number = cleanedline.split(",")
            contacts.append([name, number])
    fileexist = True

def namesearch(contacts, choice, question):
    namesearch = input(f"{question}")
    found = False
    for contact in contacts:
        if contact[0].lower() == namesearch.lower():
            print("\nFound: ", contact[0], " - ", contact[1])
            if choice == 4:
                update = input("\nEnter new phone number: ")
                contact[1] = update
            elif choice == 5:
                contacts.remove(contact)
                print("\nContact deleted")
            found = True
            break
    if not found:
        print("\nCould not find contact.")

def main():
    contacts = []
    fileexist = False

    try:
        checktxt(contacts, fileexist)
    except FileNotFoundError:
        print("\nCould not find contacts.txt, creating file.\n")

    print("\nWelcome to Contact Book\n")

    while True:
        print("\n1. View Contacts")
        print("2. Search Contact by Name")
        print("3. Add New Contact")
        print("4. Update Existing Contact")
        print("5. Delete Contact")
        print("6. Exit")

        try:
            choice = int(input("\nChoose an option: "))
        except ValueError:
            print("\nInvalid input! Please enter in a valid option.")
            continue

        match choice:
            case 1:
                length = len(contacts)
                if length <= 0:
                    print("There are no saved contacts.")
                    length = int(0)
                else:
                    print("\n----- Contacts -----")
                    for i, contact in enumerate(contacts, start=1):
                        print(f"{i}. {contact[0]} - {contact[1]}")
                    print("--------------------")
            case 2:
                namesearch(contacts, choice, "\nEnter name to search: ")
            case 3:
                namein = input("\nEnter contact name: ").strip()
                phonein = input("Enter phone number: ").strip()
                contacts.append([namein, phonein])
            case 4:
                namesearch(contacts, choice, "\nEnter name of contact to update: ")
            case 5:
                namesearch(contacts, choice, "\nEnter contact name to delete: ")
            case 6:
                print("\nExiting and saving to contacts.txt.")
                if fileexist == False:
                    with open("contacts.txt", "w") as file:
                        for contact in contacts:
                            line = f"{contact[0]},{contact[1]}\n"
                            file.write(line)
                else:
                    with open("contacts.txt", "a") as file:
                        for contact in contacts:
                            line = f"{contact[0]},{contact[1]}\n"
                            file.write(line)
                break
            case _:
                print("\nInvalid option. Please enter in a valid option.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting without saving...")

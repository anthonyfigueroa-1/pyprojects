def main():
    
    while True:
        print ("1. View Tasks")
        print ("2. Add Task")
        print ("3. Remove Task")
        print ("4. Exit")

        try:
            choice = int(input("Choose an option: "))
        except ValueError:
            print("INVALID INPUT. Please enter in a valid choice.")
            continue
        
        match choice:
            case 1:


if __name__ == "__main__":
    main()

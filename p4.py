def main():

    tasks = []
   
    while True:
        print ("\n1. View Tasks")
        print ("2. Add Task")
        print ("3. Remove Task")
        print ("4. Exit")

        try:
            choice = int(input("\nChoose an option: "))
        except ValueError:
            print("INVALID INPUT. Please enter in a valid choice.")
            continue
        
        match choice:
            case 1:
                length = len(tasks)
                if length <= 0:
                    print("There are no tasks.")
                    length = 0
                else:                    
                    print("-----")
                    for i, task in enumerate(tasks, start=1):
                        print(f"{i}. {task}")
                    print("-----")
            case 2:
                tasks.append(input("Enter task to add: "))
                for i in range(len(tasks)):
                    tasks[i] = tasks[i].strip()
                print("Task added.")
            case 3:
                delete = input("Enter task to remove: ")
                if delete in tasks:
                    tasks.remove(delete)
                    print("Task removed.")
                else:
                    print(f"No tasks found that match {delete}")
            case 4:
                print("Goodbye!")
                break
            case _:
                print("INVALID INPUT. Please enter in a valid choice.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")

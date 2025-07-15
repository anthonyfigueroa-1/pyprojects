def filehandle(tasks):
    with open("tasks.txt", "r") as file:
        for line in file:
            tasks.append(line.strip())

def main():
    tasks = []

    try:
        filehandle(tasks)
    except FileNotFoundError:
        print("No tasks.txt file found. Creating new tasks.txt.")

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
                new_task = input("Enter task to add: ").strip()
                tasks.append(new_task)
                print("Task added.")
            case 3:
                delete = input("Enter task to remove: ")
                if delete in tasks:
                    tasks.remove(delete)
                    print("Task removed.")
                else:
                    print(f"No tasks found that match {delete}")
            case 4:
                print("Saving tasks to tasks.txt.")
                print("Goodbye!")
                break
            case _:
                print("INVALID INPUT. Please enter in a valid choice.")

    with open("tasks.txt", "w") as file:
        for task in tasks:
            file.write(task + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting without saving to tasks.txt...")

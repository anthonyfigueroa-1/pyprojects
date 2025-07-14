def filehandle(tasks):
    with open("tasks.txt", "r") as file:
        for line in file:
            tasks.append = line

def main():
    tasks = []
    try:
        filehandle(tasks)
    except FileNotFoundError:
        print("No tasks.txt file found. Creating new tasks.txt.")

    tasks.append(input("Please enter in tasks followed by enter for each task: "))
    for i in range(len(tasks)):
        tasks[i] = tasks[i].strip    
    
    with open("tasks.txt", "w") as file:
        for task in tasks:
            file.write(task + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")

#Takes .json file data and stores those into a list of dictionaries, in this case, tickets.
def load_tickets(): 
    import json

    with open("tickets.json", "r") as file:
        tickets = json.load(file)
    return tickets

#As what the function says it does. Uses a for loop to loop through each entry in tickets, that was passed in from main to search through each entry, making sure to check status if it is in an open or pending status. t in the beggining being what get's stored in active_tickets.
def filter_tickets_by_status(tickets):  
    active_tickets = [t for t in tickets if t["status"].lower() in ["open", "pending"]]

    return active_tickets

#As what the function says it does. Used a for loop to store only the sites field into a list named temp. Did this to be able to use .join() to print the sites to tts_message.txt.
def format_tts_message(tickets): 
    temp = [t["site"] for t in tickets]

    with open("tts_message.txt", "w") as file:
            file.write(f"Currently affected sites are: {' and '.join(temp)}.")

def write_markdown_table(tickets): #Creates a table that will be written to status_table.md
    with open("status_table.md", "w") as file: 
        header = ["Site", "Ticket ID", "Status"]
        width = [10, 9, 8]
        #Allows for cleaner adjustment of the the pipes that seperate each field. Allows me to edit distance using {value[x]:<x}, for example, instead of having to manually type all the spaces seperating the field titles from the pipes. 
        head = f"| {header[0]:<10} | {header[1]:^9} | {header[2]:>8} |\n"         
        #This allows for cleaner adjustment of the pipes and dashes which also helps me avoid manually having to just print(|------|), for example.
        seperator = "|-" + "-|-".join("-" * width[i] for i in range(len(header))) + "-|\n" 
        file.write(head)
        file.write(seperator)
        #Reads every entry in list tickets and temporarily stores each entry in the for loop within ticket to allow me to print out the fields contained within site, ticket_id, and status of each entry within ticket.
        for ticket in tickets: 
            row = f"| {ticket['site']:<10} | {ticket['ticket_id']:^9} | {ticket['status']:<8} |\n"
            file.write(row)

#Saves active sites, e.g. open or pending, that is passed in from main() into file status_update.txt.
def save_file(filename, content): 
    with open(filename, "w") as file:
        for line in content:
            file.write(line + "\n")
def main():
    # The below attempts to open the .json file, if it does not exists the program closes or if it is empty, it closes out then as well.
    try:
        tickets = load_tickets()
    except FileNotFoundError:
        print("Error: tickets.json not found.")
        exit()
    if not tickets:
        print("Error: tickets.json is empty.")
        exit()
        
    while True:
        print("\n1. View All Tickets")
        print("2. Filter by Status")
        print("3. Export Active Sites to status_update.txt")
        print("4. Export TTS Message")
        print("5. Export Markdown-style Status Table")
        print("6. Exit")

        #Makes sure a number is inputted. Needed to add a while loop due to there being a different error dump despite except ValueError being used.
        while True: 
            try:
                choice = int(input("\nEnter option: ").strip())
                break
            except ValueError:
                print("Enter in a valid option!!!")

        match choice:
            case 1:
                print()
                for ticket in tickets:
                    print(f"Ticket #{ticket.get("ticket_id", "N/A")}","-", ticket.get("site", "N/A"), f"({ticket.get("status", "N/A")})")
            case 2:
                active = filter_tickets_by_status(tickets)
                print("Active Outages:")
                for site in active:
                    print("- Site:", site.get("site", "N/A"), "| Ticket-ID:", site.get("ticket_id", "N/A"), "| Status:", site.get("status", "N/A"))
            case 3:
                active = filter_tickets_by_status(tickets)
                #Stores strings in a list that come already filled out with the site, ticket_id, and status that allows for easy printing to file when passing lines to save_file.
                lines = [f"{t['site']} (Ticket #{t['ticket_id']}) - {t['status']}" for t in active] 
                save_file("status_update.txt", lines)
                print("Saved Active Sites to status_update.txt successfully.")
            case 4:
                active = filter_tickets_by_status(tickets)
                format_tts_message(active)
                print("Updated tts message.")
            case 5:
                write_markdown_table(tickets)
                print("Updated table file.")
            case 6:
                print("Exiting...")
                break
            case _:
                print("Error: Enter in a valid option.")


if __name__ == "__main__":
    try:
        main()
    #Allows user to exit the program using ctrl+c without dumping an error and instead just prints "Exiting...".
    except KeyboardInterrupt: 
        print("Exiting...")

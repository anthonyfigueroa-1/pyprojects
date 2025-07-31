def load_ticket_data(filepath):
    import json

    with open(filepath, "r") as file:
        tickets = json.load(file)

    return tickets

def get_parse_args():
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("--status", help="Filter by status")
    parser.add_argument("--priority", help="Filter by priority")
    parser.add_argument("--save", help="Filename to save report to")

    return parser.parse_args()

def format_ticket(ticket):
    from datetime import datetime
    formatted_ticket = []

    try:
        ts = datetime.strptime(ticket.get("created", "Not Found"), "%Y-%m-%dT%H:%M:%S")
        date = ts.strftime("%Y-%m-%d")
    except (KeyError, ValueError):
        ts = None

    formatted_ticket.append(f"[{date}] - #{ticket.get("id", "Not Found")} {ticket.get("title", "Not Found")}")

    if "assigned_to" in ticket:
       formatted_ticket.append(f"Status: {ticket.get("status", "Not Found")} | Priority: {ticket.get("priority", "Not Found")} | Assigned: {ticket.get("assigned_to", "Not Found")}")
    else:
        formatted_ticket.append(f"Status: {ticket.get("status", "Not Found")} | Priority: {ticket.get("priority", "Not Found")}")

        
    if "resolution_hours" in ticket:
        formatted_ticket.append(f"Resolution Time: {ticket.get("resolution_hours", "Not Found"):.1f} hours")

    return formatted_ticket

def filter_tickets(tickets, status=None, priority=None):
    return [
        t for t in tickets if 
        (status is None or t.get("status", "Not Found").lower() == status.lower()) and
        (priority is None or t.get("priority", "Not Found").lower() == priority.lower())]

def generate_ticket_report(tickets, status, priority, save=None):
    report = []
    total_tickets = int(0)
    report.append("===== Ticket Summary Report =====")
    for ticket in tickets:
        formatted_ticket = format_ticket(ticket)
        total_tickets += 1
        for line in formatted_ticket:
            report.append(line)
        report.append("")
            

    report.append(f"Total Tickets: {total_tickets}")

    res = [t["resolution_hours"] for t in tickets if "resolution_hours" in t]
    if res:
        art_avg = sum(res) / len(res)
        report.append(f"Average Resolution Time: {art_avg} hours")

    filters = []
    if status:
        filters.append(f"status={status}")
    if priority:
        filters.append(f"priority={priority}")
    if filters:
        report.append(f"Filtered by: {' ,'.join(filters)}")
    report.append("=================================")

    for line in report:
        print(line)

    if save:
        print(f"\nSaving to {save}")
        with open(save, "w") as file:
            for line in report:
                file.write(line + "\n")

def main():
    try:
        tickets = load_ticket_data("tickets.json")
    except FileNotFoundError:
        print("\ntickets.json not found. Exiting...")
        exit()
    if not tickets:
        print("\ntickets.json is empty. Exiting...")
        exit()
    
    args = get_parse_args()
    status = args.status.strip() if args.status else None
    priority = args.priority.strip() if args.priority else None
    save = args.save.strip() if args.save else None

    filtered_tickets = filter_tickets(tickets, status=status, priority=priority)
    generate_ticket_report(filtered_tickets, status, priority, save)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")

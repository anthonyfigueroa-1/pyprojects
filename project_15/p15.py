import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime
import argparse
import re
import json

def get_tickets_and_agents(save_json):
    tickets_url = "https://eastwest.freshservice.com/api/v2/tickets"
    agents_url = "https://eastwest.freshservice.com/api/v2/agents"
    my_api = ""
    a_api = ""

    response = requests.get(tickets_url, auth=HTTPBasicAuth(my_api, "X"))
    tickets = response.json()["tickets"]
    tickets.reverse()

    response = requests.get(agents_url, auth=HTTPBasicAuth(a_api, "X"))
    agents = response.json()["agents"]
    

    return tickets, agents

def parse_args():
    parse = argparse.ArgumentParser()

    parse.add_argument("--save", help ="Filepath where to save report to")
    parse.add_argument("--save-json", help="Filepath to file where to dump .json respone from FreshService ticket GET call.")
    parse.add_argument("--status", help="Filters recent tickets by status")
    parse.add_argument("--priority", help="Filters recent tickets by priority")
    parse.add_argument("--date", help="Filters tickets by date (MM/DD/YY)")

    return parse.parse_args()

def format_date(dt, date=None):
    ts = datetime.strptime(dt, "%Y-%m-%dT%H:%M:%SZ")

    if date:
        ticket_date = ts.strftime("%m/%d/%y")
        return ticket_date
    
    formatted_date = ts.strftime("%Y-%m-%d")
    return formatted_date

def filter_tickets(tickets, status, priority, date):
    filtered_tickets = []

    status_map = [{"open":2, "pending":3, "closed":4, "resolved":5}]
    priority_map = [{"low":1, "medium":2, "high":3, "urgent":4}]

    for ticket in tickets:
        ticket_strg = f"{ticket}"
        if status:
            ticket_status = status_map[0].get(f"{status.lower()}", "")
        if priority:
            ticket_priority = priority_map[0].get(f"{priority.lower()}", "")
        if date:
            ticket_date = format_date(ticket.get("created_at", ""), date=date)
        if (status is None or ticket.get("status", "") == ticket_status) and (priority is None or ticket.get("priority", "") == ticket_priority) and (date is None or ticket_date == date):
            filtered_tickets.append(ticket)


    return filtered_tickets

def get_agent(agents, responder_id):
    for agent in agents:
        agent_id = agent.get("id", None)
        if agent_id == responder_id:
            first_name = agent.get("first_name", "")
            last_name = agent.get("last_name", "")
            return first_name, last_name
        else:
            return None, None

def get_items(ticket, agents):
    items = []
    items.append({})

    id = ticket.get("id", "")
    items[0]["id"] = id

    priority = ticket.get("priority", "")
    match priority:
        case 1:
            items[0]["priority"] = "Low"
        case 2:
            items[0]["priority"] = "Medium"
        case 3:
            items[0]["priority"] = "High"
        case 4:
            items[0]["priority"] = "Urgent"
        case _:
            items[0]["priority"] = "Unkown"

    subject = ticket.get("subject", "NO SUBJECT")
    items[0]["subject"] = subject

    if ticket.get("responder_id", ""):
        first_name, last_name = get_agent(agents, ticket.get("responder_id", ""))
        if first_name and last_name:
            full_name = f"{first_name} {last_name}"
            items[0]["agent"] = full_name

    created = format_date(ticket.get("created_at", ""))
    items[0]["created"] = created

    due_by = format_date(ticket.get("due_by", ""))
    items[0]["due_by"] = due_by

    return items

def format_ticket(ticket, agents):
    items = get_items(ticket, agents)

    return f"[Ticket #{items[0].get('id', '?')}] {items[0].get('priority', '?')} - {items[0].get('subject', '?')}\n Agent: {items[0].get('agent', '?')}\n Created: {items[0].get('created', '?')} | Due: {items[0].get('due_by', '?')}\n"

def save_report(save, report):
    with open(save, "w") as file:
        for line in report:
            file.write(line + "\n")

def save_json_raw(save_json, filtered_tickets):
    with open(save_json, "w") as file:
        json.dump(filtered_tickets, file, indent=4)

def report(tickets, agents, save):
    report = []
    filtered_count = 0
    
    for ticket in tickets:
        filtered_count += 1
        formatted_ticket = format_ticket(ticket, agents)
        report.append(formatted_ticket)
        print("")
        print(formatted_ticket)

    print(f"{filtered_count} tickets matched filter.\n")

    if save:
        save_report(save, report)
        print(f"Saving report to {save}")

def main():
    args = parse_args()

    save_json = args.save_json.strip() if args.save_json else None
    status = args.status.strip() if args.status else None
    priority = args.priority.strip() if args.priority else None
    date = args.date.strip() if args.date else None
    save = args.save.strip() if args.save else None

    tickets, agents = get_tickets_and_agents(save_json)
    filtered_tickets = filter_tickets(tickets, status, priority, date)
    report(filtered_tickets, agents, save)

    if save_json:
        json.dumps(filtered_tickets)
        save_json_raw(save_json, filtered_tickets)
        print(f"Saving raw json to {save_json}")
    
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...\n")

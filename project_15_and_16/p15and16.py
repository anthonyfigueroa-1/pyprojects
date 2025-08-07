import requests
from requests.api import put
from requests.auth import HTTPBasicAuth
from datetime import datetime
import argparse
import json
import re

def get_tickets():
    tickets_url = f"https://eastwest.freshservice.com/api/v2/tickets"
    my_api = ""
    response = requests.get(tickets_url, auth=HTTPBasicAuth(my_api, "X"))
    tickets = response.json()["tickets"]
    tickets.reverse()

    return tickets

def parse_args():
    parse = argparse.ArgumentParser()

    parse.add_argument("--save", help ="Filepath where to save report to")
    parse.add_argument("--save-json", help="Filepath to file where to dump .json respone from FreshService ticket GET call.")
    parse.add_argument("--status", help="Filters recent tickets by status")
    parse.add_argument("--priority", help="Filters recent tickets by priority")
    parse.add_argument("--date", help="Filters tickets by date (MM/DD/YY)")
    parse.add_argument("--acknowledge",action="store_true" , help="Acknowledges tickets filtered, by setting ticket status to 'Pending'")
    parse.add_argument("--resolve", action="store_true", help="Marks filtered tickets to 'Resolved'")
    parse.add_argument("--add-note", help="Add note to filtered tickets")
    parse.add_argument("--agent", help="Filter tickets by agent(e.g. John Doe)")
    parse.add_argument("--notify-teams", action="store_true", help="Notifies team regarding changes")

    return parse.parse_args()

def format_date(dt, date=None):
    if not dt:
        return "N/A"

    ts = datetime.strptime(dt, "%Y-%m-%dT%H:%M:%SZ")

    if date:
        ticket_date = ts.strftime("%m/%d/%y")
        return ticket_date
    
    formatted_date = ts.strftime("%Y-%m-%d")
    return formatted_date

def filter_tickets(tickets, status, priority, date, agent):
    filtered_tickets = []

    status_map = {"open":2, "pending":3, "closed":4, "resolved":5}
    priority_map = {"low":1, "medium":2, "high":3, "urgent":4}

    for ticket in tickets:
        if status:
            ticket_status = status_map.get(f"{status.lower()}", "")
        if priority:
            ticket_priority = priority_map.get(f"{priority.lower()}", "")
        if date:
            ticket_date = format_date(ticket.get("created_at", ""), date=date)
        if agent:
            items = get_items(ticket)
        if (status is None or ticket.get("status", "") == ticket_status) and (priority is None or ticket.get("priority", "") == ticket_priority) and (date is None or ticket_date == date) and (agent is None or agent.lower() == items.get("agent", "").lower()):
            filtered_tickets.append(ticket)

    return filtered_tickets

def get_agent(responder_id):
    if not responder_id:
        return "Unkown"

    s_url = f"https://eastwest.freshservice.com/api/v2/agents/{responder_id}"
    a_api = ""
    response = requests.get(s_url, auth=HTTPBasicAuth(a_api, "X"))
    agent = response.json()["agent"]

    return f"{agent.get('first_name')} {agent.get('last_name')}"

def get_items(ticket):
    items = {}

    id = ticket.get("id", "")
    items["id"] = id

    priority = ticket.get("priority", "")
    priority_map = {1:"low", 2:"medium", 3:"high", 4:"urgent"}
    items["priority"] = priority_map.get(priority, "Unkown")

    subject = ticket.get("subject", "NO SUBJECT")
    items["subject"] = subject

    full_name = get_agent(ticket.get("responder_id", ""))
    items["agent"] = full_name

    created = format_date(ticket.get("created_at", ""))
    items["created"] = created

    due_by = format_date(ticket.get("due_by", ""))
    items["due_by"] = due_by

    return items

def format_ticket(ticket):
    items = get_items(ticket)

    return f"[Ticket #{items.get('id', '?')}] {items.get('priority', '?')} - {items.get('subject', '?')}\n Agent: {items.get('agent', '')}\n Created: {items.get('created', '?')} | Due: {items.get('due_by', '?')}\n"

def save_report(save, report):
    with open(save, "w") as file:
        for line in report:
            file.write(line + "\n")

def save_json_raw(save_json, filtered_tickets):
    with open(save_json, "w") as file:
        json.dump(filtered_tickets, file, indent=4)

def put_status(ticket, status_code):
    ticket_id = ticket.get("id", "")

    if not ticket_id:
       return
    print(status_code)

    url = f'https://eastwest.freshservice.com/api/v2/tickets/{ticket_id}'
    api = ""
    header = {"Content-Type": "application/json"}
    payload = {"status": status_code}

    response = requests.put(url, json=payload, auth=HTTPBasicAuth(api, "X"), headers=header)

def post_note(ticket, body):
    ticket_id = ticket.get("id", "")

    if not ticket_id:
       return 

    url = f'https://eastwest.freshservice.com/api/v2/tickets/{ticket_id}/notes'
    api = api = ""
    header = {"Content-Type": "application/json"}
    payload = {"body": f"{body}", "private": True}

    response = requests.post(url, json=payload, auth=HTTPBasicAuth(api, "X"), headers=header)

def post_teams_message(tickets, acknowledge, resolve, add_note):
    if not tickets:
        return

    updated_tickets = []

    for ticket in tickets:
        items = get_items(ticket)
        updated_tickets.append(f"[Ticket #{items.get('id')}] {items.get('priority')} - {items.get('subject')}")

    items_updated = []
    if acknowledge == True:
        items_updated.append("Status set to pending")
    if resolve == True:
        items_updated.append("Status set to resolved")
    if add_note:
        items_updated.append("note added")

    text = f"{', '.join(updated_tickets)}<br>Updated: {', '.join(items_updated)}."

    url = ""
    payload = {"text": text}

    response = requests.post(url, json=payload)

def report_GET(tickets, save):
    report = []
    filtered_count = 0
    
    for ticket in tickets:
        filtered_count += 1
        formatted_ticket = format_ticket(ticket)
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
    agent = args.agent.strip() if args.agent else None
    acknowledge = args.acknowledge
    resolve = args.resolve
    add_note = args.add_note.strip() if args.add_note else None
    notify_teams = args.notify_teams

    tickets = get_tickets()
    filtered_tickets = filter_tickets(tickets, status, priority, date, agent)
    report_GET(filtered_tickets, save)

    for ticket in filtered_tickets:
        if acknowledge == True:
            status = int(3)
            put_status(ticket, status)
        if resolve == True:
            status = int(4)
            put_status(ticket, status)
        if add_note:
            post_note(ticket, add_note)

    if notify_teams == True:
        post_teams_message(filtered_tickets, acknowledge, resolve, add_note)

    if save_json:
        save_json_raw(save_json, filtered_tickets)
        print(f"Saving raw json to {save_json}")
    
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...\n")

def load_email_data(filepath):
    import json

    with open(filepath, "r") as file:
        emails = json.load(file)

    return emails
def parse_args():
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("--priority", help="Filters by priority")
    parser.add_argument("--attachment-only", action="store_true", help="Sorts by emails with an attachment") 
    parser.add_argument("--save", help= "Where to save report to")

    return parser.parse_args()

def filter_emails(emails, priority = None, attachment_only = False):
    return [
            t for t in emails if
            (priority is None or t.get("priority", "") == priority) and
            (not attachment_only or not t.get("has_attachment", False))]

def detect_intent(email_body):
    if "disk" in email_body.get("body", "").lower():
        return "Looks like you are talking about disks", "smart"
    if "cpu" in email_body.get("body", "").lower():
        return "Looks like you are talking about cpu's", "smart"
    if "network" in email_body.get("body", "").lower():
        return "Looks like you are talking about networks", "smart"
    else:
        return "Someone will get back to you about this", "general"

def generate_response(email_dict):
    email_reply = []

    email_reply.append("From: anthony@routestack.net")
    email_reply.append(f"To: {email_dict.get('from_address', '')}")
    email_reply.append(f"Subject: Re: {email_dict.get('subject', '')}")
    body, count = detect_intent(email_dict)
    email_reply.append(f"Body: {body}")

    from datetime import datetime

    ts = datetime.strptime(email_dict.get("received_at", ""), "%Y-%m-%dT%H:%M:%S")
    sent = ts.strftime("%Y-%m-%d %H:%M")

    email_reply.append(f"Sent on: {sent}\n")

    return email_reply, count

def generate_responder_report(responses, save = None):
    report = []
    smart = int(0)
    general = int(0)

    report.append("\n===== AUTO-REPONSE DIGEST =====\n")

    for response in responses:
        generated_response, count = generate_response(response)
        if "smart" in count:
            smart += 1
        if "general" in count:
            general += 1 
        for line in generated_response:
            report.append(line)

    report.append("===============================")
    report.append(f"Total replies: {general + smart}")
    report.append(f"Smart replies: {smart} | Default replies: {general}\n")

    for line in report:
        print(line)

    if save:
        with open(save, "w") as file:
            for line in report:
                file.write(line + "\n")
        print(f"Saving to {save}")
    
def main():
    try:
        emails = load_email_data("emails.json")
    except FileNotFoundError:
        print("emails.json not found. Exiting...")
        exit()
    if not emails:
        print("emails.json is empty. Exiting...")
        exit()
        
    args = parse_args()

    priority = args.priority.strip() if args.priority else None
    attachment_only = args.attachment_only if args.attachment_only else False
    save = args.save.strip() if args.save else None

    filtered_emails = filter_emails(emails, priority = priority, attachment_only = attachment_only)
    generate_responder_report(filtered_emails, save = save)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")

def load_alert_data(filepath):
    import json

    with open(filepath, "r") as file:
        data = json.load(file)

    return data

def parse_filters():
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("--severity", help="Filters by severity of alert")
    parser.add_argument("--unacknowledged-only", action="store_true", help="Filters alert by unacknowledged-only")
    parser.add_argument("--save", help="Filename to save report to")

    return parser.parse_args()

def filter_alerts(alerts, severity=None, unack_only=False):
    return [
            t for t in alerts if
            (severity is None or t.get("severity", "").lower() == severity.lower()) and
            (unack_only is False or t.get("acknowledged", "") == unack_only)]

def format_alert(alert):
    from datetime import datetime

    ts = datetime.strptime(alert.get("timestamp", ""), "%Y-%m-%dT%H:%M:%S")
    dandt = ts.strftime("[%Y-%m-%d %H:%M]")

    formatted_alert = f"{dandt} {alert.get("host", "")} - {alert.get("message", "")} ({alert.get("severity", "")})"
    
    return formatted_alert

def generate_alert_report(filtered_alerts, severity=None, unack_only=False, save=None):
    report = []

    report.append("\n===== ALERT DIGEST =====")
    
    for alert in filtered_alerts:
        formatted_alert = format_alert(alert)
        report.append(formatted_alert) 
        

    if unack_only is True:
        report.append("Unacknowledged Only: Yes")

    if severity:
        report.append(f"Filtered by: severity={severity}")

    report.append("========================\n")
    
    for line in report:
        print(line)

    if save:
        print(f"Saving to {save}...")
        with open(save, "w") as file:
            for line in report:
                file.write(line + "\n")
            
def main():
    try:
        data = load_alert_data("alerts.json")
    except FileNotFoundError:
        print("alerts.json not found")
    if not data:
        print("alerts.json is empty")

    args = parse_filters()
    severity = args.severity.strip() if args.severity else None
    unack_only = args.unacknowledged_only if args.unacknowledged_only else False
    save = args.save.strip() if args.save else None

    filtered_alerts = filter_alerts(data, severity = severity, unack_only = unack_only)
    generate_alert_report(filtered_alerts, severity= severity, unack_only = unack_only, save = save)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")


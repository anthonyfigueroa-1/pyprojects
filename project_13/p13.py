from datetime import datetime

def get_csv_data(filepath):
    import csv

    with open(filepath) as file:
        alerts = list(csv.DictReader(file))

    return alerts
def parse_args():
    import argparse

    parse = argparse.ArgumentParser()
    parse.add_argument("--activity", help="Filter by activitiy happening in each log entry")
    parse.add_argument("--date", help="Filter logs by date")
    parse.add_argument("--save", help="Where to save report to")

    return parse.parse_args()

def convert_time(alert, date = None):
    alert_ts = datetime.strptime(alert.get("Date", ""), "%Y-%m-%dT%H:%M:%S.%f%z")
    if date:
        date_ts = datetime.strptime(date, "%Y-%m-%d")
        return alert_ts, date_ts

    return alert_ts

def filter_alerts(alerts, activity, date):
    import re

    filtered_alerts = []

    for t in alerts:
        if date:
            alert_ts, date_ts = convert_time(t, date = date)
        else:
            alert_ts = convert_time(t)
        if (date is None or date_ts.date() == alert_ts.date()) and (activity is None or re.search(rf"{re.escape(activity)}", t["Activity"], re.IGNORECASE)):
            filtered_alerts.append(t) 

    return filtered_alerts


def format_alert(alert):
    alert_ts = convert_time(alert)

    time_stamp = alert_ts.strftime("[%Y-%m-%d %H:%M]")

    format = []

    format.append(f"{time_stamp} {alert.get("Group", "")} - {alert.get("Activity", "")}")
    format.append(f"Device: {alert.get("Device", "")} | Org: {alert.get("Hospitality")}")
    format.append(f"Description: {alert.get("Description", "")}\n")
    
    return format

def report(alerts, save = None):
    filter_count = 0

    for temp in alerts:
        formatted_alert = format_alert(temp)
        filter_count += 1
        for line in formatted_alert:
            print(line)
    if save:
        with open(save, "w") as file:
            for temp in alerts:
                formatted_alert = format_alert(temp)
                for line in formatted_alert:
                    file.write(line + "\n")

    print(f"\n{filter_count} entries matched filter.")

    if save:
        print(f"\nSaving to {save}\n")

def main():
    try:
        alerts = get_csv_data("mycomp.csv")
    except FileNotFoundError:
        print("File not found. Exiting...")
        exit()
    if not alerts:
        print("File is empty. Exiting...")
        exit()

    arg = parse_args()

    activity = arg.activity if arg.activity else None
    date = arg.date if arg.date else None
    save = arg.save if arg.save else None

    filtered_alerts = filter_alerts(alerts, activity, date)     

    report(filtered_alerts, save = save)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")

import argparse 
from datetime import datetime
import re

def import_data(filepath):
    data = []

    with open(filepath, "r") as file:
        for line in file:
            data.append(line)

    return data

def parseargs():
    parse = argparse.ArgumentParser()

    parse.add_argument("file", help="File to import data from")
    parse.add_argument("--keyword", help="Searches each log for inputted keyword")
    parse.add_argument("--ip", help="Filters logs for inputted ip address")
    parse.add_argument("--error-only", action="store_true", help="Filters logs for those that are errors")
    parse.add_argument("--save", help="Where to save report to")

    return parse.parse_args()

def filter_logs(logs, keyword, ip, error_only):
    filtered_logs = []
    check_filter = []

    for log in logs:
        if keyword or ip or error_only:
            if keyword:
                keyword_match = re.search(rf"({re.escape(keyword).lower()})", log.lower())
                if keyword_match:
                    check_filter.append(keyword_match.group(1))
                else:
                    continue 

            if ip:
                ip_match = re.search(rf"IP:\s({re.escape(ip)})\s", log)
                if ip_match:
                    check_filter.append(ip_match.group(1))     
                else:
                    continue 

            if error_only == True:
                error_match = re.search(r"\[(ERROR)\]", log)
                if error_match:
                    check_filter.append(error_match.group(1))
                else:
                    continue 
            
            if None in check_filter:
                check_filter.append(False)
            else:
                check_filter.append(True)

            if True in check_filter:
                filtered_logs.append(log)
            else:
                break 

        else:
            filtered_logs.append(log)

    return filtered_logs

def grab_items(log):

    items = []

    tempstamp = re.search(r"(\d+-\d+-\d+\s\d+:\d+:\d+)", log)
    items.append(f"[{tempstamp.group(1)}]")

    status = re.search(r"\[(ERROR|INFO|WARNING)\]", log)
    items.append(status.group(1))

    device = re.search(r"Device:\s([^\s]+)", log)
    items.append(device.group(1))

    ip_add = re.search(r"IP:\s(\d+.\d+.\d+.\d+)", log)
    items.append(ip_add.group(1))

    mac = re.search(r"MAC:\s(..:..:..:..:..:..)", log)
    items.append(mac.group(1))

    message = re.search(r"Message:\s([^\n]+)", log)
    items.append(message.group(1))

    return items

def format_log(log):
    items = grab_items(log)
    format = []

    return [f"{items[0]} {items[1]}", f"Device: {items[2]}", f"IP: {items[3]} | MAC: {items[4]}", f"Message: {items[5]}"]

def report(filtered_logs, save):
    report = []

    report.append("")
    for log in filtered_logs:
        formatted_log = format_log(log)
        for line in formatted_log:
            report.append(line)
        report.append("")

    for line in report:
        print(line)

    if save:
        with open(save, "w") as file:
            for line in report:
                file.write(line + "\n")

def main():
    arg = parseargs()

    keyword = arg.keyword.strip() if arg.keyword else None
    ip = arg.ip.strip() if arg.ip else None
    error_only = arg.error_only if True else False
    save = arg.save.strip() if arg.save else None
    file = arg.file.strip() if arg.file else None

    try:
        logs = import_data(file)
    except FileNotFoundError:
        print(f"{file} not found. Exiting...")
        exit()
    if not logs:
        print(f"{file} is empty. Exiting...")
        exit()

    filtered_logs = filter_logs(logs, keyword, ip, error_only)
    report(filtered_logs, save)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")

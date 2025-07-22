def load_transaction_data(filepath):
    import json

    with open(filepath, "r") as file:
        transactions = json.load(file)        

    return transactions

def filter_transactions(transactions, category=None, min_amount=None):
    if category is not None and min_amount is not None:
        filtered = [t for t in transactions if float(t.get("amount")) > min_amount]
        filtered = [t for t in transactions if t.get("category", "").lower() == category.lower()]
        print(filtered)
        return filtered
    elif min_amount is not None and category is None:
        filtered = [t for t in transactions if float(t.get("amount")) > min_amount]
        return filtered
    elif category is not None and min_amount is None:
        filtered = [t for t in transactions if t.get("category", "").lower() == category.lower()]
        return filtered
    else:
        return transactions

def format_transaction(txn):
    formatted_txn = []
    for temp in txn:
        add = f"[{temp.get('date')}] - ${temp.get('amount'):.2f} at {temp.get('merchant')} ({temp.get('category', 'Uncategorized')})"
        formatted_txn.append(add) 

    return formatted_txn

def generate_report(filtered_txns, category=None, min_amount=None):
    formatted_txn = format_transaction(filtered_txns)

    total = sum(txn.get("amount") for txn in filtered_txns)

    report = []
    filters = []

    if category:
        filters.append(f"category={category}")
    if min_amount:
        filters.append(f"min_amount=${min_amount:.2f}")

    report.append(" ===== Budget Summary Report ===== \n")

    for line in formatted_txn:
        report.append(line)
        
    report.append(f"\nTotal: ${total:.2f}")

    if filters:
        report.append(f"Filtered by: {', '.join(filters)}") 
        
    report.append("\n ================================= ")

    for line in report:
        print(line)

    with open("budget_report.txt", "w") as file:
        for line in report:
            file.write(line + "\n")

def main():
    try:
        trxn = load_transaction_data("transactions.json")
    except FileNotFoundError:
        print("No transactions.json file found")
        exit()
    if not trxn:
        print("transactions.json is empty.")
        exit()

    cat = input("Enter a category to filter by (or leave blank): ")
    min = input("Enter a minimum amount (or leave blank): ")

    cat = cat if cat else None
    min = float(min) if min else None

    filtered = filter_transactions(trxn, category = cat, min_amount=min)
    generate_report(filtered, category=cat, min_amount=min)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")

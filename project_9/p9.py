def load_transaction_data(filepath):
    import json

    with open(filepath, "r") as file:
        transactions = json.load(file)        

    return transactions

def filter_transactions(transactions, category=None, min_amount=None):
    return [
        t for t in transactions
        if (category is None or t.get("category", "").lower() == category.lower()) 
        and (min_amount is None or float(t.get("amount")) > min_amount)]
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

    report.append("\n ===== Budget Summary Report ===== \n")

    for line in formatted_txn:
        report.append(line)
        
    report.append(f"\nTotal: ${total:.2f}")

    if filters:
        report.append(f"Filtered by: {', '.join(filters)}") 
        
    report.append("\n ================================= \n")

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

    ctgry = input("Enter a category to filter by (or leave blank): ")
    min_amt = input("Enter a minimum amount (or leave blank): ")

    ctgry = ctgry if ctgry else None
    min_amt = float(min_amt) if min_amt else None

    filtered = filter_transactions(trxn, category = ctgry, min_amount=min_amt)
    generate_report(filtered, category=ctgry, min_amount=min_amt)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")

def testint(this):
    while True:
        try:
            option = int(input(f"\n{this}"))
            break
        except ValueError:
            print("\nInvalid input. Only numbers are accepted.")
    return option

def main():
    balance = int(1000)
    change = int(0)
    keepgoing = True

    print ("Welcome to the ATM!")

    while keepgoing:
        print ("1. Check balance")
        print ("2. Deposit")
        print ("3. Withdraw")
        print ("4. Exit")
        try:
            option = int(input("\nChoose an option: "))
        except ValueError:
            print("\nInvalid input. Only numbers are accepted.\n")
            continue

        match option:
            case 1:
                print (f"\nCurrent balance is ${balance}\n")
            case 2:
                change = testint("How much would you like to deposit: ")
                balance += change
                print (f"Deposited ${change}. New balance is ${balance}\n")
            case 3:
                withdraw = int
                withdraw = testint("How much would you like to withdraw: ")
                if balance < withdraw:
                    print("Insufficient Funds!\n")
                else:
                    balance -= withdraw
                    print(f"Withdrew ${withdraw}. New balance is ${balance}\n")
            case 4:
                print("\nThank you, come again!")
                keepgoing = False
            case _:
                print("\nEnter in a valid option!\n")

if __name__ == "__main__":
    main()

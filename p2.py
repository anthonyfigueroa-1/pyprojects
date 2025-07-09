def main():
    password = input("Enter your password: ")
    
    if (len(password) < 6):
        print("Weak Password")
    elif (any (char.isdigit() for char in password)):
        print("Medium Password")
    else:
        print("Strong Password")

if __name__ == "__main__":
    main()

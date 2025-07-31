def tryfile(downsites):
    with open("outages.txt", "r") as file:
        for line in file:
            cleanline = line.strip()
            downsites.append(cleanline)

def wfile(file, downsites, option):
    with open(file, "w") as file:
        if option == 4:
            print("\nTTS message exported to tts_message.txt:")
            tts = f"The following sites are currently down: {', '.join(downsites)}"
            print(tts)
            file.write(tts)
        elif option == 5:
            print("\nEmail message exported to ooo_email.txt:")
            ooo = f"Outages currently affect: {', '.join(downsites)}. Our network team is working on resolution."
            print(ooo)
            file.write(ooo)
        elif option == 6:
            for site in downsites:
                file.write(site + "\n")

def main():
    downsites = [] 

    try:
        tryfile(downsites)
    except FileNotFoundError:
        print("\noutages.txt does not exist... creating file")


    print("\nWelcome to the Network Outage Tracker")

    while True:
        print("\n1. View Down Site")
        print("2. Add Down Site")
        print("3. Remove Down Site")
        print("4. Export TTS Message Format")
        print("5. Export Email Format")
        print("6. Exit")

        while True:
            try:
                option = int(input("\nChoose an option: ").strip())
                break 
            except ValueError:
                print("\nInvalid Option! Please enter in a valid option.")

        match option:
            case 1:
                if len(downsites) <= 0:
                    print("No down sites right now.")
                else:
                    print("\n----- Down Sites -----")
                    for i, site in enumerate(downsites, start=1):
                        print(f"{i}. {site}")
                    print("----------------------")
            case 2:
                newdown = input("\nEnter site name to add: ").strip()
                downsites.append(newdown)
            case 3:
                if len(downsites) <= 0:
                    print("No down sites to remove as there are no sites down.")
                else:
                    delete = input("\nEnter site name to remove: ").strip()
                    found = False
                    for site in downsites:
                        if site.lower() == delete.lower():
                            print(f"{site} has been removed from the outage list.")
                            downsites.remove(site)
                            found = True
                            break
                    if not found:
                        print(f"Could not find '{delete}' in Down Sites")
            case 4:
                if len(downsites) <= 0:
                    print("No down sites to generate tts message for.")
                else:
                    wfile("tts_message.txt", downsites, option) 
            case 5:
                if len(downsites) <= 0:
                    print("No down sites to generate ooo email for.")
                else:
                    wfile("ooo_email.txt", downsites, option)
            case 6:
                wfile("outages.txt", downsites, option)
                print("\nSaving outages to outages.txt...")
                print("Goodbye!")
                break
            case _:
                print("\nInvalid option! Please enter in a valid option")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting without saving...")

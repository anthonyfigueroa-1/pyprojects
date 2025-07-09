def main():
    breakfast = int(input("How many calories for breakfast? "))
    lunch = int(input("How many calories for lunch? "))
    dinner = int(input("How many calories for dinner? "))
    goal = int(input("\nWhat is your daily caloric budget? "))

    total_calories = int(breakfast + lunch + dinner)
    
    print(f"\nYour total caloric intake for that day was {total_calories}")
    if goal <= total_calories:
        print(f"You had {total_calories - goal} calories more than your goal of {goal}")
    else:
        print(f"You had {goal - total_calories} calories less than your goal of {goal}")

if __name__ == "__main__":
    main()

from datetime import datetime, timedelta
import os
from flask import Flask, render_template, request

app = Flask(__name__)

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def add_business_days(start_date, days_to_add):
    """
    Increment 'start_date' by 'days_to_add' business days (skipping weekends).
    Returns a datetime object.
    """
    business_days_passed = 0
    current_date = start_date
    
    while business_days_passed < days_to_add:
        current_date += timedelta(days=1)
        # weekday() => Monday=0 ... Sunday=6
        if current_date.weekday() < 5:  
            business_days_passed += 1
            
    return current_date
def add_weekend_days(start_date, days_to_add):
    """
    Increment 'start_date' by 'days_to_add' weekend days (count only Sat & Sun).
    Counting start_date as day #1 if it's on a weekend, otherwise we still move
    forward until we've counted the specified number of weekend days.
    Returns a datetime object.
    """
    weekend_days_passed = 0
    current_date = start_date

    # First, if the start_date itself is a weekend (weekday() >= 5),
    # consider it as day #1:
    if current_date.weekday() >= 5:
        weekend_days_passed = 1

    # Keep moving forward until we've counted 'days_to_add' weekend days
    while weekend_days_passed < days_to_add:
        current_date += timedelta(days=1)
        if current_date.weekday() >= 5:  # Saturday or Sunday
            weekend_days_passed += 1
            
    return current_date

def add_all_days(start_date, days_to_add):
    """
    Increment 'start_date' by 'days_to_add' days (including weekends).
    Counting start_date as day #1.
    Returns a datetime object.
    """
    days_counted = 1
    current_date = start_date
    
    while days_counted < days_to_add:
        current_date += timedelta(days=1)
        days_counted += 1
    
    return current_date

def Calculate(date_obj):
    print("Enter the number of days you want to count:")
    print("Business = 1\nWeekend = 2\nAll = 3")
    choice = input(": ")
    
    if choice == "1":
        print("Enter the number of BUSINESS days you want to count:")
        days = int(input(": "))
        result = add_business_days(date_obj, days)
        return days, result
    
    elif choice == "2":
        print("Enter the number of WEEKEND days you want to count:")
        days = int(input(": "))
        result = add_weekend_days(date_obj, days)
        return days, result
    
    elif choice == "3":
        print("Enter the number of ALL days you want to count:")
        days = int(input(": "))
        result = add_all_days(date_obj, days)
        return days, result
    
    else:
        print("Invalid choice, returning to main menu.")
        return None, None

def main():
    clear_terminal()
    
    today_str = datetime.today().strftime('%m-%d-%Y')
    print("Welcome to the day counter!\n\nToday is", today_str)
    print("\nTo use today's date press 1\nTo use a custom date press 2\n")
    
    datechoice = input(": ")
    
    if datechoice == "1":
        # Use today's date as a datetime object
        date_obj = datetime.today()
        days, result = Calculate(date_obj)
        
        # If we got a valid result, print it
        if result:
            print(f"\n{days} days from today is {result.strftime('%m-%d-%Y')}")
        
        input("Press Enter to continue...")
        main()  # Re-run main if you want an endless loop
    
    elif datechoice == "2":
        print("Enter the date you want to count from in the format MM-DD-YYYY")
        date_input = input(": ")
        
        try:
            date_obj = datetime.strptime(date_input, '%m-%d-%Y')
        except ValueError:
            print("Invalid date format. Please try again.")
            input("Press Enter to continue...")
            main()
            return
        
        days, result = Calculate(date_obj)
        if result:
            print(f"\n{days} days from {date_input}  is {result.strftime('%m-%d-%Y')}")
        
        input("Press Enter to continue...")
        main()
    
    else:
        print("Invalid input.")
        input("Press Enter to continue...")
        main()

if __name__ == "__main__":
    main()
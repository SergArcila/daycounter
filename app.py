from flask import Flask, render_template, request
from datetime import datetime, timedelta

app = Flask(__name__)

# -------------- Day Counter Functions ------------------ #

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
    Returns a datetime object.
    """
    weekend_days_passed = 0
    current_date = start_date

    # If the start_date itself is a weekend, consider that as day #1
    if current_date.weekday() >= 5:
        weekend_days_passed = 1

    while weekend_days_passed < days_to_add:
        current_date += timedelta(days=1)
        if current_date.weekday() >= 5:  # Saturday or Sunday
            weekend_days_passed += 1
            
    return current_date

def add_all_days(start_date, days_to_add):
    """
    Increment 'start_date' by 'days_to_add' days (including weekends).
    Returns a datetime object.
    """
    days_counted = 1
    current_date = start_date
    
    while days_counted < days_to_add:
        current_date += timedelta(days=1)
        days_counted += 1
    
    return current_date

# -------------- Flask Routes ------------------ #

@app.route("/", methods=["GET"])
def home():
    """
    Render the main page that shows the form.
    """
    return render_template("index.html")

@app.route("/calculate", methods=["POST"])
def calculate():
    """
    Handle the form submission from index.html.
    Parse the user input, run the correct function, 
    and return the result via result.html.
    """
    # Get form data
    date_str = request.form.get("start_date")   # e.g., "03-10-2025"
    day_type = request.form.get("day_type")     # "business", "weekend", or "all"
    days_str = request.form.get("days_count")   # e.g., "15"

    # Convert the inputs
    try:
        days = int(days_str)
    except ValueError:
        # If user didn't provide a valid number, handle it
        return render_template("result.html", 
                               error="Invalid number of days. Please try again.")

    try:
        start_date = datetime.strptime(date_str, "%m-%d-%Y")
    except ValueError:
        return render_template("result.html", 
                               error="Invalid date format. Please use MM-DD-YYYY.")
    
    # Depending on the day_type, pick the right function
    if day_type == "business":
        resulting_date = add_business_days(start_date, days)
        day_label = "business"
    elif day_type == "weekend":
        resulting_date = add_weekend_days(start_date, days)
        day_label = "weekend"
    elif day_type == "all":
        resulting_date = add_all_days(start_date, days)
        day_label = "all"
    else:
        return render_template("result.html", 
                               error="Invalid day type selected.")
    
    # Format result as MM-DD-YYYY
    result_str = resulting_date.strftime("%m-%d-%Y")

    return render_template("result.html", 
                           start_date=date_str, 
                           days=days, 
                           day_label=day_label, 
                           result_date=result_str)

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
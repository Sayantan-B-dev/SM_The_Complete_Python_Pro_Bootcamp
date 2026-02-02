from datetime import datetime, date, timedelta

def calculate_age(dob_str):
    """
    Calculates age details from date of birth in DD/MM/YYYY format.
    """

    # Convert DOB string to date object
    dob = datetime.strptime(dob_str, "%d/%m/%Y").date()

    # Get today's date
    today = date.today()

    # Calculate age in years
    years = today.year - dob.year

    # Adjust if birthday has not happened yet this year
    if (today.month, today.day) < (dob.month, dob.day):
        years -= 1

    # Find last birthday
    last_birthday_year = today.year if (today.month, today.day) >= (dob.month, dob.day) else today.year - 1
    last_birthday = date(last_birthday_year, dob.month, dob.day)

    # Days since last birthday
    days_since_birthday = (today - last_birthday).days

    # Approximate months and days
    months = days_since_birthday // 30
    days = days_since_birthday % 30

    # Total days lived
    total_days = (today - dob).days

    # Output
    print("Date of Birth       :", dob.strftime("%d %B %Y"))
    print("Today's Date        :", today.strftime("%d %B %Y"))
    print("Age                 :", years, "years", months, "months", days, "days")
    print("Total Days Lived    :", total_days)


def milestone_days(dob_str):
    """
    Calculates milestone dates like 1000th and 10000th day from DOB.
    """

    # Convert DOB string to date object
    dob = datetime.strptime(dob_str, "%d/%m/%Y").date()

    # Calculate milestone dates using timedelta
    day_1000 = dob + timedelta(days=1000)
    day_10000 = dob + timedelta(days=10000)

    # Output
    print("1000th Day Date     :", day_1000.strftime("%d %B %Y"))
    print("10000th Day Date    :", day_10000.strftime("%d %B %Y"))


def safe_age_calculator(dob_str):
    try:
        calculate_age(dob_str)
        milestone_days(dob_str)
    except ValueError:
        print("Invalid date format. Use DD/MM/YYYY")


# User input
safe_age_calculator(input("Enter DOB (DD/MM/YYYY): "))

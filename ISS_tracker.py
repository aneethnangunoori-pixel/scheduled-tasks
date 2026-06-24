from datetime import datetime
import smtplib
import time
import requests

MY_EMAIL = "aneethnangunoori@gmail.com"
MY_PASSWORD = "ieqg shby olfh wmcl"
MY_LAT = 51.507351
MY_LONG = -0.127758


def is_iss_overhead():
    try:
        # Switched to a highly reliable alternative ISS API
        response = requests.get(url="https://wheretheiss.at", timeout=5)
        response.raise_for_status()
        data = response.json()

        # Updated key names to match the new API structure
        iss_latitude = float(data["latitude"])
        iss_longitude = float(data["longitude"])

        if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
            return True
    except requests.exceptions.RequestException:
        pass
    return False


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    try:
        response = requests.get("https://api.sunrise-sunset.org/json", params=parameters, timeout=5)
        response.raise_for_status()
        data = response.json()

        sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
        sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

        # CRITICAL FIX: Changed to .utcnow() to match the API's UTC timezone
        time_now = datetime.utcnow().hour

        if time_now >= sunset or time_now <= sunrise:
            return True
    except requests.exceptions.RequestException:
        print("Could not connect to Sunset API. Retrying next minute...")
    return False


# CRITICAL FIX: Moved the sleep to the end of the loop so it checks immediately on startup
while True:
    if is_iss_overhead() and is_night():
        try:
            # CRITICAL FIX: Added explicit port 587 for Gmail
            with smtplib.SMTP("smtp.gmail.com", 587) as connection:
                connection.starttls()
                connection.login(user=MY_EMAIL, password=MY_PASSWORD)
                connection.sendmail(
                    from_addr=MY_EMAIL,
                    to_addrs=MY_EMAIL,
                    msg="Subject:Look Up\n\nThe ISS is above you in the sky."
                )
            print("Email sent successfully!")
        except Exception as e:
            print(f"Failed to send email: {e}")

    time.sleep(60)

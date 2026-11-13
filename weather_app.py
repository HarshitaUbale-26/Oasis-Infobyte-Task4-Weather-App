import requests
import json
import getpass

print("=" * 45)
print("          WEATHER INFORMATION APP")
print("=" * 45)

# Get API Key
api_key = getpass.getpass("Enter your OpenWeather API key: ")

# Get city or Indian PIN code
location = input("Enter city name or PIN code: ").strip()

# Input validation
if not location:
    print("Please enter a city name or PIN code!")

else:
    # OpenWeatherMap API URL
    url = "https://api.openweathermap.org/data/2.5/weather"

    # Check whether input is a 6-digit Indian PIN code
    if location.isdigit() and len(location) == 6:
        params = {
            "zip": location + ",IN",
            "appid": api_key,
            "units": "metric"
        }
    else:
        params = {
            "q": location,
            "appid": api_key,
            "units": "metric"
        }

    try:
        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 200:

            # Parse JSON response
            data = json.loads(response.text)

            # Temperature conversion
            temp_c = data["main"]["temp"]
            temp_f = (temp_c * 9/5) + 32

            print("\n" + "=" * 45)
            print("             WEATHER REPORT")
            print("=" * 45)

            print("City:", data["name"])
            print("Country:", data["sys"]["country"])

            print("\n--- TEMPERATURE DETAILS ---")
            print(f"Temperature: {temp_c:.1f} °C")
            print(f"Temperature: {temp_f:.1f} °F")

            print("\n--- WEATHER DETAILS ---")
            print("Condition:", data["weather"][0]["description"].title())
            print("Humidity:", data["main"]["humidity"], "%")
            print("Wind Speed:", data["wind"]["speed"], "m/s")

            print("\n" + "=" * 45)
            print("          THANK YOU!")
            print("=" * 45)

        elif response.status_code == 404:
            print("City or PIN code not found!")

        elif response.status_code == 401:
            print("Invalid API key or API key is not activated yet.")

        else:
            print("Unable to fetch weather information.")
            print("Error Code:", response.status_code)

    except requests.exceptions.Timeout:
        print("Network timeout! Please try again.")

    except requests.exceptions.ConnectionError:
        print("Internet connection error!")

    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)

    except (ValueError, KeyError, TypeError):
        print("Unable to read weather data. Please try again.")
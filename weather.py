# [2025-12-14 23:53:48 IST] File: weather.py

import requests
import sys

def get_api_key():
    """
    Retrieves the API key. 
    IMPORTANT: Replace the placeholder string below with your actual OpenWeatherMap API key.
    """
    return "YOUR_API_KEY_HERE"

def build_url(city_name, api_key):
    """
    Constructs the API URL with query parameters.
    """
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    # Using 'metric' units for Celsius
    return f"{base_url}?q={city_name}&appid={api_key}&units=metric"

def fetch_weather_data(city_name, api_key):
    """
    Sends the GET request and handles network errors.
    Returns the JSON response if successful, or None if failed.
    """
    url = build_url(city_name, api_key)
    
    try:
        response = requests.get(url)
        
        # Check for HTTP errors
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            print(f"\n[!] Error: City '{city_name}' not found. Please check the spelling.")
        elif response.status_code == 401:
            print("\n[!] Error: Invalid API Key. Please check your configuration.")
        else:
            print(f"\n[!] Error: Unable to fetch data. Status Code: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("\n[!] Error: Network problem. Please check your internet connection.")
    except Exception as e:
        print(f"\n[!] An unexpected error occurred: {e}")
        
    return None

def display_weather_report(data):
    """
    Parses the JSON data and prints the formatted report.
    """
    if not data:
        return

    # Parsing JSON data
    city = data.get("name")
    country = data.get("sys", {}).get("country")
    temp = data.get("main", {}).get("temp")
    humidity = data.get("main", {}).get("humidity")
    condition = data.get("weather", [{}])[0].get("main")
    description = data.get("weather", [{}])[0].get("description")

    # Display Output
    print("\n---- Weather Report ----")
    print(f"City        : {city} ({country})")
    print(f"Temperature : {temp}°C")
    print(f"Humidity    : {humidity}%")
    print(f"Condition   : {condition} ({description})")
    print("------------------------\n")

def main():
    print("--- OpenWeatherMap API Fetcher ---")
    
    api_key = get_api_key()
    
    # Simple check to ensure user replaced the placeholder
    if api_key == "YOUR_API_KEY_HERE":
        print("[!] PLEASE UPDATE THE API KEY IN THE SCRIPT BEFORE RUNNING.")
        return

    while True:
        city = input("Enter city name (or type 'quit' to exit): ").strip()
        
        if city.lower() == 'quit':
            print("Exiting application. Goodbye!")
            break
            
        if not city:
            print("City name cannot be empty.")
            continue

        weather_data = fetch_weather_data(city, api_key)
        
        if weather_data:
            display_weather_report(weather_data)

if __name__ == "__main__":
    main()
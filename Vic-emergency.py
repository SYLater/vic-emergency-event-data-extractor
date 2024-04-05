import requests  # Import the requests library for HTTP requests
import json  # Import the json library for JSON processing
from datetime import datetime  # Import datetime for handling date and time
import re  # Import regular expression library for text matching and manipulation
import html  # Import HTML library for handling HTML entities
from geopy.geocoders import Nominatim  # Import Nominatim from geopy for geocoding
from geopy import distance  # Import distance from geopy for distance calculations

# Set up Nominatim geocoder with a user agent named "tutorial"
app = Nominatim(user_agent="tutorial")

# Define a function to remove HTML tags from a string
def remove_html_tags(raw_html):
    # Use regular expression to replace HTML tags with an empty string
    clean_text = re.sub('<.*?>', '', raw_html)
    # Unescape HTML entities in the text
    return html.unescape(clean_text)

# Define a function to format a timestamp
def format_timestamp(timestamp):
    # Check if the timestamp is a number (int or float)
    if isinstance(timestamp, (int, float)):
        # Convert the timestamp to UTC datetime and format it as a string
        return datetime.utcfromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')
    # If the timestamp is not a number, return it as is
    return timestamp

# Define a function to extract data based on radius and a center point
def extract_data(radius, center_point, json_path):
    # Set the URL and request headers for the API call
    url = "https://emergency.vic.gov.au/public/events-geojson.json"
    params = {"_": "1700872612149"}  # Cache-busting query parameter
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.9",
        "Sec-Ch-Ua": "\"Google Chrome\";v=\"119\", \"Chromium\";v=\"119\", \"Not?A_Brand\";v=\"24\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "X-Requested-With": "XMLHttpRequest"
    }

    # Create a session and send a GET request to the URL
    session = requests.Session()
    response = session.get(url, headers=headers, params=params)

    # Check if the request was successful (HTTP status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        json_response = response.json()
        # Prepare a list to store extracted data
        extracted_data = []

        # Iterate over features in the JSON response
        for feature in json_response['features']:
            # Extract properties and geometry from the feature
            properties = feature.get('properties', {})

            # Geocode the location from properties
            geocoded_location = app.geocode(properties.get('location'))

            # Check if the location was successfully geocoded
            if geocoded_location:
                # Store the lat and lng of the event location
                event_location = [{'lat': geocoded_location.latitude, 'lng': geocoded_location.longitude}]

                # Convert center point and event location to tuples for distance calculation
                center_point_coords = tuple(center_point[0].values())
                event_location_coords = tuple(event_location[0].values())

                # Calculate the distance between center point and event location
                distance_km = distance.distance(center_point_coords, event_location_coords).km

                # Check if the event is within the specified radius
                if distance_km <= radius:

                    event = {}  # Initialize an empty dictionary to store details of the event

                    # Define a list of ID fields that should be skipped during data extraction
                    skip_id_fields = ['sesId', 'sourceId', 'id', 'eventId', 'estaId','cfaId']

                    # Iterate over each key-value pair in the event's properties
                    for key, value in properties.items():
                        # Check if the value is neither None nor False
                        if value is not None and value is not False:
                            # Skip adding the value if it contains the string "Unknown"
                            if "Unknown" in str(value):
                                continue
                            # Skip adding the value if the key is one of the skip_id_fields
                            if any(ele in key for ele in skip_id_fields):
                                continue
                            # Add the key-value pair to the event dictionary
                            event[key] = value

                    # Extract specific fields for special handling
                    web_body = properties.get('webBody', '')
                    text = properties.get('text', '')
                    location = properties.get('location', '')

                    # Clean and add the HTML content from 'webBody' to the event dictionary
                    if web_body:
                        event['WebBody'] = remove_html_tags(web_body)
                    # Clean and add the HTML content from 'text' to the event dictionary
                    if text:
                        event['Text'] = remove_html_tags(text)
                    # Add the geocoded address as the location to the event dictionary
                    if location:
                        event['location'] = geocoded_location.address

                    # Extract 'cap' properties for further processing
                    cap = properties.get('cap', {})
                    string = "Unknown"

                    # Iterate over each key-value pair in the 'cap' dictionary
                    for key, value in cap.items():
                        # Check if the value is neither None nor False
                        if value is not None and value is not False:
                            # Skip adding the value if it contains the string "Unknown"
                            if string in str(value):
                                continue
                            # Add the key-value pair to the event dictionary
                            event[key] = value

                    # Extract 'incidentFeatures' and add to the event dictionary if it exists
                    incident_features = properties.get('incidentFeatures', [])
                    if incident_features:
                        event['IncidentFeatures'] = incident_features

                    # Append the processed event dictionary to the list of extracted data
                    extracted_data.append(event)


        # Save the extracted data to a JSON file
        with open(json_path, 'w', encoding='utf-8') as outfile:
            json.dump(extracted_data, outfile, indent=4, ensure_ascii=False)

        print("Data saved to output.json")
    else:
        # Print an error message if the data retrieval failed
        print(f"Failed to retrieve data, status code: {response.status_code}")

# Set the radius and center point for data extraction
radius = 100  # Radius in kilometers
center_point = [{'lat': -38.106759372327836, 'lng': 144.8611388380783}]
json_path = 'output.json'
# Call the extract_data function with the specified radius and center point
extract_data(radius, center_point, json_path)
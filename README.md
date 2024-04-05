# Emergency Event Data Extractor

This Python script extracts data from the Emergency Victoria GeoJSON API and saves the relevant information to a JSON file. The script filters the data based on a specified radius around a given center point, and processes the response to extract key details about each event.

## Features

- Retrieves emergency event data from the Emergency Victoria GeoJSON API
- Filters the events based on a specified radius around a given center point
- Extracts and processes relevant event details, including:
  - Event properties (e.g., text, web body, location)
  - Geocoded location information
  - Calculated distance from the center point
  - Specific 'cap' and 'incidentFeatures' properties
- Saves the extracted data to a JSON file for further analysis or use

## Requirements

- Python 3.x
- Required libraries:
  - `requests`
  - `json`
  - `datetime`
  - `re`
  - `html`
  - `geopy`

## Usage

1. Clone the repository:
   ```
   git clone https://github.com/SYLater/vic-emergency-event-data-extractor.git
   ```
2. Navigate to the project directory:
   ```
   cd emergency-event-data-extractor
   ```
3. Run the script:
   ```
   python emergency_event_extractor.py
   ```
4. The extracted data will be saved to a file named `output.json` in the specified location.

## Customization

You can customize the script by modifying the following parameters:

- `radius`: The radius in kilometers around the center point to include events.
- `center_point`: The latitude and longitude of the center point for the data extraction.
- `json_path`: The path where the extracted data will be saved as a JSON file.

## Contributing

If you find any issues or have suggestions for improvements, feel free to create a new issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
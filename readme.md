# Information Aggregator

The **Information Aggregator** is a Python application that provides weather information, top news headlines, and historical events for any given city and country. It also visualizes the distribution of news articles across different sources.

## Features
- **Weather Information:** Retrieves current weather data for a specified city.
- **Top News Headlines:** Displays the top 5 news headlines for the selected country and category.
- **Historical Events:** Shows historical events that occurred on this day.
- **Visualization:** Presents a bar chart depicting the distribution of news articles across different sources.

## Requirements
- Python 3.7+
- API Keys for `OpenWeatherMap` and `NewsAPI`

### Dependencies
Install the required packages using pip:

```bash
pip install requests beautifulsoup4 pillow matplotlib
```

### API Keys
- **OpenWeatherMap API Key:** Obtain from [OpenWeatherMap](https://home.openweathermap.org/users/sign_up).
- **NewsAPI Key:** Obtain from [NewsAPI](https://newsapi.org/register).

## How to Run

1. Clone the repository or copy the files to your local machine.

2. Ensure you have Python 3.7+ installed.

3. Install dependencies:

   ```bash
   pip install requests beautifulsoup4 pillow matplotlib
   ```

4. Add your API keys to the script. In the script, replace the placeholders in these lines with your API keys:

   ```python
   WEATHER_API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"
   NEWS_API_KEY = "YOUR_NEWS_API_KEY"
   ```

5. Run the application:

   ```bash
   python aggregator.py
   ```

6. In the GUI, select a country, city, and news category. Click "Get Information" to see the aggregated results.

7. Switch to the "Visualization" tab to view the distribution of news articles across different sources.

## Example Usage
1. Select `Country: us`, `City: New York`, and `News Category: general`.
2. Click **Get Information** to retrieve data.
3. Review the results in the text box and explore the visualization tab.

### Directory Layout
```
information-aggregator/
│
├── aggregator.py            # Main application script
└── README.md                # This README file
```


## License
This project is licensed under the MIT License.

import tkinter as tk
from tkinter import ttk, messagebox
import requests
from bs4 import BeautifulSoup
import unittest
from PIL import Image, ImageTk
import io
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter.font as tkfont


# Constants for API URLs
WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"
NEWS_API_URL = "https://newsapi.org/v2/top-headlines"
WEATHER_API_KEY = "aa775ce9ac68a7830e7411f7af86cd94"
NEWS_API_KEY = "1b5f0455e4cc470a8b8389d35459673f"

COUNTRIES = ["us", "gb", "ca", "au", "in", "de", "fr", "jp", "cn", "ke", "au"]
CITIES = {
    "us": ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"],
    "gb": ["London", "Birmingham", "Manchester", "Liverpool", "Leeds"],
    "ca": ["Toronto", "Vancouver", "Montreal", "Calgary", "Ottawa"],
    "au": ["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide"],
    "in": ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai"],
    "de": ["Berlin", "Munich", "Hamburg", "Cologne", "Frankfurt"],
    "fr": ["Paris", "Marseille", "Lyon", "Toulouse", "Nice"],
    "jp": ["Tokyo", "Osaka", "Nagoya", "Sapporo", "Fukuoka"],
    "cn": ["Beijing", "Shanghai", "Guangzhou", "Shenzhen", "Chengdu"],
    "ke": ["Nairobi", "Mombasa", "Kisumu", "Nakuru", "Eldoret"],
    "au": ["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide"],
}
NEWS_CATEGORIES = ["general", "business", "entertainment", "health", "science", "sports", "technology"]

# Color Palette
COLOR_PALETTE = {
    "primary": "#1976d2",
    "secondary": "#64b5f6",
    "accent": "#ffc107",
    "background": "#f5f5f5",
    "text": "#212121"
}

# Fonts
def load_font(family, size, weight="normal"):
    return tkfont.Font(family=family, size=size, weight=weight)

#FONT_PRIMARY = load_font("Helvetica", 12, "bold")


class Weather:
    def __init__(self, city: str):
        self.city = city

    def get_weather(self) -> dict:
        params = {"q": self.city, "appid": WEATHER_API_KEY, "units": "metric"}
        response = requests.get(WEATHER_API_URL, params=params)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            raise ValueError("Invalid City Name.")
        elif response.status_code == 401:
            raise ValueError("Invalid API Key.")
        else:
            raise ValueError("Failed to retrieve weather data.")

    def parse_weather(self, data: dict) -> str:
        description = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        icon = data["weather"][0]["icon"]
        return f"Weather in {self.city}: {description}, {temperature}°C", icon


class News:
    def __init__(self, country: str = "us", category: str = "general"):
        self.country = country
        self.category = category

    def get_news(self) -> dict:
        params = {"country": self.country, "category": self.category, "apiKey": NEWS_API_KEY}
        response = requests.get(NEWS_API_URL, params=params)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            raise ValueError("Invalid API Key.")
        else:
            raise ValueError("Failed to retrieve news data.")

    def parse_news(self, data: dict) -> str:
        articles = data["articles"][:5]
        headlines = [f"{idx + 1}. {article['title']}" for idx, article in enumerate(articles)]
        return "Top News Headlines:\n" + "\n".join(headlines)

    def get_news_sources_distribution(self, data: dict) -> dict:
        sources = {}
        for article in data["articles"]:
            source_name = article["source"]["name"]
            sources[source_name] = sources.get(source_name, 0) + 1
        return sources


class OnThisDay:
    def __init__(self):
        self.url = "https://en.wikipedia.org/wiki/Main_Page"

    def get_events(self) -> str:
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, "html.parser")
        events = soup.select("#mp-otd ul li")
        return "On This Day:\n" + "\n".join([event.text for event in events[:5]])


class InformationAggregator:
    def __init__(self, city: str, country: str, news_category: str):
        self.weather = Weather(city)
        self.news = News(country, news_category)
        self.on_this_day = OnThisDay()

    def aggregate_info(self) -> dict:
        output = {"weather_info": "", "news_info": "", "on_this_day_info": "", "weather_icon": None, "news_data": None}
        try:
            weather_info, icon = self.weather.parse_weather(self.weather.get_weather())
            output["weather_info"] = weather_info
            output["weather_icon"] = icon
        except ValueError as e:
            output["weather_info"] = f"Weather Error: {str(e)}"

        try:
            news_data = self.news.get_news()
            news_info = self.news.parse_news(news_data)
            output["news_info"] = news_info
            output["news_data"] = news_data
        except ValueError as e:
            output["news_info"] = f"News Error: {str(e)}"

        output["on_this_day_info"] = self.on_this_day.get_events()
        return output


class AggregatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Information Aggregator")
        root.geometry("1000x600")
        root.configure(bg=COLOR_PALETTE["background"])

        # Initialize font after the root window is created
        FONT_PRIMARY = load_font("Helvetica", 12, "bold")

        # Variables
        self.country_var = tk.StringVar(value=COUNTRIES[0])
        self.city_var = tk.StringVar()
        self.news_category_var = tk.StringVar(value=NEWS_CATEGORIES[0])

        # Tabs
        self.tab_control = ttk.Notebook(root)
        self.info_tab = ttk.Frame(self.tab_control)
        self.visualization_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.info_tab, text="Information")
        self.tab_control.add(self.visualization_tab, text="Visualization")
        self.tab_control.pack(expand=1, fill="both")

        # Style Setup
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background=COLOR_PALETTE["background"])
        style.configure("TLabel", background=COLOR_PALETTE["background"], foreground=COLOR_PALETTE["text"])
        style.configure("TCombobox", background=COLOR_PALETTE["secondary"], fieldbackground=COLOR_PALETTE["secondary"], foreground=COLOR_PALETTE["text"])
        style.configure("TButton", background=COLOR_PALETTE["primary"], foreground="#FFFFFF", font=("Helvetica", 10, "bold"))

        # Information Tab
        ttk.Label(self.info_tab, text="Country:").grid(row=0, column=0, sticky="w", pady=5, padx=10)
        self.country_menu = ttk.Combobox(self.info_tab, values=COUNTRIES, textvariable=self.country_var, state="readonly")
        self.country_menu.grid(row=0, column=1, pady=5, padx=10)

        ttk.Label(self.info_tab, text="City:").grid(row=1, column=0, sticky="w", pady=5, padx=10)
        self.city_menu = ttk.Combobox(self.info_tab, textvariable=self.city_var, state="readonly")
        self.city_menu.grid(row=1, column=1, pady=5, padx=10)

        ttk.Label(self.info_tab, text="News Category:").grid(row=2, column=0, sticky="w", pady=5, padx=10)
        self.news_category_menu = ttk.Combobox(self.info_tab, values=NEWS_CATEGORIES, textvariable=self.news_category_var, state="readonly")
        self.news_category_menu.grid(row=2, column=1, pady=5, padx=10)

        self.result_text = tk.Text(self.info_tab, wrap=tk.WORD, width=60, height=25, font=("Helvetica", 10), bg="#FFFFFF")
        
        self.result_text.grid(row=3, column=0, columnspan=2, pady=5, padx=10, sticky="nsew")
        self.result_text.grid_propagate(False)

        self.weather_icon_label = ttk.Label(self.info_tab)
        self.weather_icon_label.grid(row=3, column=2, pady=5, padx=10)

        self.submit_button = ttk.Button(self.info_tab, text="Get Information", command=self.fetch_information)
        self.submit_button.grid(row=4, column=0, columnspan=2, pady=10, padx=10)

        self.progress = ttk.Progressbar(self.info_tab, orient="horizontal", mode="indeterminate")
        self.progress.grid(row=5, column=0, columnspan=2, pady=10, padx=10)

        # Visualization Tab
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.visualization_tab)
        self.canvas.get_tk_widget().pack(expand=True, fill="both")

        # Bind events
        self.country_menu.bind("<<ComboboxSelected>>", self.update_city_menu)
        self.result_text.bind("<Enter>", lambda event: self.show_tooltip(event, "Aggregated information about weather, news, and historical events."))
        self.city_menu.bind("<Enter>", lambda event: self.show_tooltip(event, "Select a city based on the chosen country."))
        self.country_menu.bind("<Enter>", lambda event: self.show_tooltip(event, "Select a country."))
        self.news_category_menu.bind("<Enter>", lambda event: self.show_tooltip(event, "Select the category of news to be fetched."))

        self.update_city_menu()

        # Make the window resizable
        self.info_tab.rowconfigure(3, weight=1)
        self.info_tab.columnconfigure(0, weight=1)
        self.info_tab.columnconfigure(1, weight=1)

    def show_tooltip(self, event, text):
        tooltip = tk.Toplevel()
        tooltip.wm_overrideredirect(True)
        tooltip.geometry(f"+{event.x_root + 10}+{event.y_root + 10}")
        label = tk.Label(tooltip, text=text, background="yellow", relief="solid", borderwidth=1)
        label.pack()
        tooltip.after(1500, tooltip.destroy)

    def update_city_menu(self, event=None):
        country = self.country_var.get()
        self.city_menu.config(values=CITIES.get(country, []))
        self.city_menu.set(CITIES[country][0])

    def fetch_information(self):
        self.progress.start()
        city = self.city_var.get().strip()
        country = self.country_var.get().strip()
        news_category = self.news_category_var.get().strip()
        if not city or not country or not news_category:
            messagebox.showerror("Input Error", "Please select a city, country, and news category.")
            self.progress.stop()
            return

        try:
            aggregator = InformationAggregator(city, country, news_category)
            result = aggregator.aggregate_info()
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"{result['weather_info']}\n\n{result['news_info']}\n\n{result['on_this_day_info']}")
            self.update_weather_icon(result["weather_icon"])
            self.plot_news_sources_distribution(result["news_data"])
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            self.progress.stop()

    def update_weather_icon(self, icon_code):
        if icon_code:
            icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
            response = requests.get(icon_url)
            if response.status_code == 200:
                image_data = response.content
                image = Image.open(io.BytesIO(image_data))
                image = image.resize((80, 80), resample=Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                self.weather_icon_label.config(image=photo)
                self.weather_icon_label.image = photo
            else:
                self.weather_icon_label.config(image='', text="No Icon")
                self.weather_icon_label.image = None
        else:
            self.weather_icon_label.config(image='', text="No Icon")
            self.weather_icon_label.image = None

    def plot_news_sources_distribution(self, news_data):
        """Plot the distribution of news articles across different sources."""
        if news_data:
            news = News()
            sources_distribution = news.get_news_sources_distribution(news_data)
            sources = list(sources_distribution.keys())
            counts = list(sources_distribution.values())

            # Clear the previous plot
            self.ax.clear()

            # Create a bar chart
            self.ax.barh(sources, counts, color=COLOR_PALETTE["primary"])
            self.ax.set_xlabel("Number of Articles")
            self.ax.set_ylabel("News Sources")
            self.ax.set_title("Distribution of News Articles Across Different Sources")

            # Add plot to canvas
            self.canvas.draw()


class TestAggregator(unittest.TestCase):
    def test_weather(self):
        weather = Weather("London")
        data = weather.get_weather()
        self.assertIn("weather", data)
        parsed, _ = weather.parse_weather(data)
        self.assertIn("Weather in London:", parsed)

    def test_news(self):
        news = News("us", "general")
        data = news.get_news()
        self.assertIn("articles", data)
        parsed = news.parse_news(data)
        self.assertIn("Top News Headlines:", parsed)

    def test_on_this_day(self):
        on_this_day = OnThisDay()
        events = on_this_day.get_events()
        self.assertIn("On This Day:", events)

    def test_aggregator(self):
        aggregator = InformationAggregator("London", "us", "general")
        result = aggregator.aggregate_info()
        self.assertIn("Weather in London:", result["weather_info"])
        self.assertIn("Top News Headlines:", result["news_info"])
        self.assertIn("On This Day:", result["on_this_day_info"])


def main():
    root = tk.Tk()
    gui = AggregatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
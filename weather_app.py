import tkinter as tk
from tkinter import ttk, font
import requests
from datetime import datetime, timezone
import threading


# ─────────────────────────────────────────────
#  API KEY  –  paste your OpenWeatherMap key here
API_KEY = "HEHEHEHEHEHEHEHEHEHEHHE"
# ─────────────────────────────────────────────

BASE_URL = "http://api.openweathermap.org/data/2.5/weather"


# ── Weather condition → emoji mapping ────────────────────────────────────────
def get_weather_emoji(weather_id: int, icon_code: str) -> str:
    """Return an emoji that matches the OWM weather condition code."""
    is_night = icon_code.endswith("n")

    if weather_id == 800:
        return "🌙" if is_night else "☀️"
    if weather_id == 801:
        return "🌤️"
    if weather_id == 802:
        return "⛅"
    if weather_id in (803, 804):
        return "☁️"
    if 200 <= weather_id < 300:
        return "⛈️"
    if 300 <= weather_id < 400:
        return "🌦️"
    if 500 <= weather_id < 600:
        if weather_id in (511,):
            return "🌨️"
        return "🌧️"
    if 600 <= weather_id < 700:
        return "❄️"
    if weather_id == 701:
        return "🌫️"
    if weather_id == 721:
        return "🌫️"
    if weather_id == 741:
        return "🌁"
    if weather_id == 762:
        return "🌋"
    if weather_id == 771:
        return "💨"
    if weather_id == 781:
        return "🌪️"
    if 700 <= weather_id < 800:
        return "🌫️"
    return "🌡️"


def format_local_time(unix_ts: int, tz_offset: int) -> str:
    """Convert UTC unix timestamp + timezone offset → human-readable local time."""
    local_dt = datetime.fromtimestamp(unix_ts + tz_offset, tz=timezone.utc)
    return local_dt.strftime("%I:%M %p")


def wind_direction(degrees: float) -> str:
    dirs = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    ix = round(degrees / 45) % 8
    return dirs[ix]


# ── Main Application ─────────────────────────────────────────────────────────
class WeatherApp(tk.Tk):
    # Colour palette
    BG        = "#0d1b2a"
    CARD      = "#1b2d42"
    ACCENT    = "#4fc3f7"
    ACCENT2   = "#81d4fa"
    TEXT      = "#e8f4fd"
    MUTED     = "#90afc5"
    SUCCESS   = "#69f0ae"
    WARNING   = "#ffd740"
    ERROR     = "#ff6b6b"
    DIVIDER   = "#243447"

    def __init__(self):
        super().__init__()
        self.title("🌤 WeatherNow")
        self.geometry("480x680")
        self.resizable(False, False)
        self.configure(bg=self.BG)

        # Center the window
        self.update_idletasks()
        x = (self.winfo_screenwidth()  - 480) // 2
        y = (self.winfo_screenheight() - 680) // 2
        self.geometry(f"480x680+{x}+{y}")

        self._build_ui()

    # ── UI construction ───────────────────────────────────────────────────────
    def _build_ui(self):
        # ── Header bar ──
        header = tk.Frame(self, bg=self.CARD, pady=16)
        header.pack(fill="x")

        tk.Label(
            header,
            text="🌤  WeatherNow",
            bg=self.CARD,
            fg=self.ACCENT,
            font=("Helvetica", 22, "bold"),
        ).pack()
        tk.Label(
            header,
            text="Real-time weather at your fingertips",
            bg=self.CARD,
            fg=self.MUTED,
            font=("Helvetica", 10),
        ).pack()

        # ── Search section ──
        search_frame = tk.Frame(self, bg=self.BG, pady=20)
        search_frame.pack(fill="x", padx=24)

        tk.Label(
            search_frame,
            text="Enter City Name",
            bg=self.BG,
            fg=self.MUTED,
            font=("Helvetica", 10, "bold"),
        ).pack(anchor="w")

        input_row = tk.Frame(search_frame, bg=self.BG)
        input_row.pack(fill="x", pady=(6, 0))

        self.city_var = tk.StringVar()
        self.city_entry = tk.Entry(
            input_row,
            textvariable=self.city_var,
            font=("Helvetica", 14),
            bg=self.CARD,
            fg=self.TEXT,
            insertbackground=self.ACCENT,
            relief="flat",
            bd=0,
            highlightthickness=2,
            highlightbackground=self.DIVIDER,
            highlightcolor=self.ACCENT,
        )
        self.city_entry.pack(side="left", fill="x", expand=True, ipady=10, ipadx=12)
        self.city_entry.bind("<Return>", lambda e: self._fetch_weather_thread())

        self.search_btn = tk.Button(
            input_row,
            text="  Search  ",
            font=("Helvetica", 11, "bold"),
            bg=self.ACCENT,
            fg=self.BG,
            activebackground=self.ACCENT2,
            activeforeground=self.BG,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self._fetch_weather_thread,
        )
        self.search_btn.pack(side="left", padx=(8, 0), ipady=10, ipadx=8)

        # ── Status / error label ──
        self.status_var = tk.StringVar()
        self.status_label = tk.Label(
            self,
            textvariable=self.status_var,
            bg=self.BG,
            fg=self.ERROR,
            font=("Helvetica", 10),
        )
        self.status_label.pack()

        # ── Main weather card ──
        self.card_frame = tk.Frame(self, bg=self.CARD, bd=0, relief="flat")
        self.card_frame.pack(fill="both", expand=True, padx=24, pady=(4, 24))

        # Emoji + Temp row
        top_row = tk.Frame(self.card_frame, bg=self.CARD)
        top_row.pack(fill="x", padx=20, pady=(24, 0))

        self.emoji_label = tk.Label(
            top_row, text="", bg=self.CARD, fg=self.TEXT, font=("Helvetica", 64)
        )
        self.emoji_label.pack(side="left")

        temp_block = tk.Frame(top_row, bg=self.CARD)
        temp_block.pack(side="left", padx=16)

        self.temp_label = tk.Label(
            temp_block, text="", bg=self.CARD, fg=self.TEXT, font=("Helvetica", 48, "bold")
        )
        self.temp_label.pack(anchor="w")

        self.desc_label = tk.Label(
            temp_block, text="", bg=self.CARD, fg=self.ACCENT, font=("Helvetica", 13, "bold")
        )
        self.desc_label.pack(anchor="w")

        self.city_label = tk.Label(
            temp_block, text="", bg=self.CARD, fg=self.MUTED, font=("Helvetica", 11)
        )
        self.city_label.pack(anchor="w")

        # Divider
        tk.Frame(self.card_frame, bg=self.DIVIDER, height=1).pack(fill="x", padx=20, pady=16)

        # ── Detail grid ──
        grid = tk.Frame(self.card_frame, bg=self.CARD)
        grid.pack(fill="x", padx=20)
        grid.columnconfigure((0, 1), weight=1)

        self._detail_widgets = {}
        details = [
            ("feels_like",  "🌡️", "Feels Like",   0, 0),
            ("humidity",    "💧", "Humidity",      0, 1),
            ("wind",        "💨", "Wind Speed",    1, 0),
            ("pressure",    "🔵", "Pressure",      1, 1),
            ("visibility",  "👁️",  "Visibility",    2, 0),
            ("clouds",      "☁️",  "Cloud Cover",   2, 1),
        ]

        for key, icon, label_text, row, col in details:
            cell = tk.Frame(grid, bg=self.DIVIDER, padx=12, pady=10)
            cell.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

            tk.Label(cell, text=f"{icon}  {label_text}", bg=self.DIVIDER,
                     fg=self.MUTED, font=("Helvetica", 9, "bold")).pack(anchor="w")

            val_lbl = tk.Label(cell, text="—", bg=self.DIVIDER,
                               fg=self.TEXT, font=("Helvetica", 14, "bold"))
            val_lbl.pack(anchor="w")
            self._detail_widgets[key] = val_lbl

        # Divider
        tk.Frame(self.card_frame, bg=self.DIVIDER, height=1).pack(fill="x", padx=20, pady=16)

        # ── Sun times ──
        sun_row = tk.Frame(self.card_frame, bg=self.CARD)
        sun_row.pack(fill="x", padx=20, pady=(0, 20))
        sun_row.columnconfigure((0, 1), weight=1)

        self.sunrise_lbl = self._sun_block(sun_row, "🌅 Sunrise", 0)
        self.sunset_lbl  = self._sun_block(sun_row, "🌇 Sunset",  1)

        # ── Placeholder text (shown before first search) ──
        self._placeholder = tk.Label(
            self.card_frame,
            text="🔍  Search for a city to see\nthe current weather",
            bg=self.CARD,
            fg=self.MUTED,
            font=("Helvetica", 13),
            justify="center",
        )
        self._placeholder.place(relx=0.5, rely=0.5, anchor="center")

        self._hide_weather_widgets()

    def _sun_block(self, parent, label_text: str, col: int) -> tk.Label:
        frame = tk.Frame(parent, bg=self.CARD)
        frame.grid(row=0, column=col, sticky="w")
        tk.Label(frame, text=label_text, bg=self.CARD,
                 fg=self.MUTED, font=("Helvetica", 9, "bold")).pack(anchor="w")
        val = tk.Label(frame, text="—", bg=self.CARD,
                       fg=self.TEXT, font=("Helvetica", 13, "bold"))
        val.pack(anchor="w")
        return val

    # ── Show / hide helpers ───────────────────────────────────────────────────
    def _hide_weather_widgets(self):
        self.emoji_label.configure(text="")
        self.temp_label.configure(text="")
        self.desc_label.configure(text="")
        self.city_label.configure(text="")
        for w in self._detail_widgets.values():
            w.configure(text="—")
        self.sunrise_lbl.configure(text="—")
        self.sunset_lbl.configure(text="—")
        self._placeholder.lift()

    def _show_weather_widgets(self):
        self._placeholder.lower()

    # ── Fetch weather ─────────────────────────────────────────────────────────
    def _fetch_weather_thread(self):
        """Run the API call on a background thread to keep UI responsive."""
        city = self.city_var.get().strip()
        if not city:
            self.status_var.set("⚠️  Please enter a city name.")
            return
        self.status_var.set("⏳  Fetching weather…")
        self.search_btn.configure(state="disabled")
        t = threading.Thread(target=self._fetch_weather, args=(city,), daemon=True)
        t.start()

    def _fetch_weather(self, city: str):
        try:
            params = {"q": city, "appid": API_KEY, "units": "metric"}
            resp = requests.get(BASE_URL, params=params, timeout=8)
            data = resp.json()
        except requests.exceptions.ConnectionError:
            self.after(0, self._set_error, "❌  No internet connection.")
            return
        except Exception as exc:
            self.after(0, self._set_error, f"❌  Error: {exc}")
            return

        self.after(0, self._update_ui, data)

    def _set_error(self, msg: str):
        self.status_var.set(msg)
        self.search_btn.configure(state="normal")
        self._hide_weather_widgets()

    def _update_ui(self, data: dict):
        self.search_btn.configure(state="normal")

        cod = data.get("cod")
        if cod != 200:
            msg = data.get("message", "City not found.")
            self._set_error(f"❌  {msg.capitalize()}")
            return

        self.status_var.set("")
        self._show_weather_widgets()

        # ── Extract values ──
        weather_id  = data["weather"][0]["id"]
        icon_code   = data["weather"][0]["icon"]
        description = data["weather"][0]["description"].title()

        temp        = round(data["main"]["temp"])
        feels_like  = round(data["main"]["feels_like"])
        humidity    = data["main"]["humidity"]
        pressure    = data["main"]["pressure"]
        wind_speed  = round(data["wind"]["speed"] * 3.6, 1)
        wind_deg    = data["wind"].get("deg", 0)
        visibility  = data.get("visibility", 0) / 1000      # metres → km
        clouds      = data["clouds"]["all"]
        city_name   = data["name"]
        country     = data["sys"]["country"]
        tz_offset   = data["timezone"]
        sunrise_ts  = data["sys"]["sunrise"]
        sunset_ts   = data["sys"]["sunset"]

        emoji = get_weather_emoji(weather_id, icon_code)

        # ── Push to widgets ──
        self.emoji_label.configure(text=emoji)
        self.temp_label.configure(text=f"{temp}°C")
        self.desc_label.configure(text=description)
        self.city_label.configure(text=f"📍 {city_name}, {country}")

        self._detail_widgets["feels_like"].configure(text=f"{feels_like}°C")
        self._detail_widgets["humidity"].configure(text=f"{humidity}%")
        self._detail_widgets["wind"].configure(
            text=f"{wind_speed} km/h {wind_direction(wind_deg)}"
        )
        self._detail_widgets["pressure"].configure(text=f"{pressure} hPa")
        self._detail_widgets["visibility"].configure(text=f"{visibility:.1f} km")
        self._detail_widgets["clouds"].configure(text=f"{clouds}%")

        self.sunrise_lbl.configure(text=format_local_time(sunrise_ts, tz_offset))
        self.sunset_lbl.configure(text=format_local_time(sunset_ts, tz_offset))


# ── Entry point ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = WeatherApp()
    app.mainloop()

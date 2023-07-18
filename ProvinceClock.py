import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import pytz

def fetch_data(province):
    data = {
        "Ontario": {"capital": "Toronto", "population": 14711827, "timezone": "Canada/Eastern"},
        "Quebec": {"capital": "Quebec City", "population": 8537674, "timezone": "Canada/Eastern"},
        "British Columbia": {"capital": "Victoria", "population": 5110917, "timezone": "Canada/Pacific"},
        "Alberta": {"capital": "Edmonton", "population": 4413146, "timezone": "Canada/Mountain"},
        "Manitoba": {"capital": "Winnipeg", "population": 1377517, "timezone": "Canada/Central"},
        "Saskatchewan": {"capital": "Regina", "population": 1171661, "timezone": "Canada/Saskatchewan"},
        "Newfoundland and Labrador": {"capital": "St. John's", "population": 519716, "timezone": "Canada/Newfoundland"},
        "New Brunswick": {"capital": "Fredericton", "population": 779993, "timezone": "Canada/Atlantic"},
        "Nova Scotia": {"capital": "Halifax", "population": 971395, "timezone": "Canada/Atlantic"},
        "Prince Edward Island": {"capital": "Charlottetown", "population": 158158, "timezone": "Canada/Atlantic"},
        "Yukon": {"capital": "Whitehorse", "population": 41078, "timezone": "Canada/Pacific"},
        "Northwest Territories": {"capital": "Yellowknife", "population": 44904, "timezone": "Canada/Mountain"},
        # Parts of Nunavut are in the Eastern time zone, while others are in the Central time zone. For simplicity, Eastern (for Eastern Canada) was used here.
        "Nunavut": {"capital": "Iqaluit", "population": 39097, "timezone": "Canada/Eastern"},
    }
    return data.get(province)

def show_data():
    province = combo.get()
    data = fetch_data(province)
    if data:
        time_zone = pytz.timezone(data["timezone"])
        dt = datetime.now(time_zone)
        messagebox.showinfo(province, f"Capital: {data['capital']}\n"
                                      f"Population: {data['population']}\n"
                                      f"Current Time: {dt.strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        messagebox.showerror("Error", "Invalid selection.")

root = tk.Tk()

tk.Label(root, text="Select your province in Canada:").pack()
combo = ttk.Combobox(root)
combo['values'] = ["Ontario", "Quebec", "British Columbia", "Alberta", 
                   "Manitoba", "Saskatchewan", "Newfoundland and Labrador",
                   "New Brunswick", "Nova Scotia", "Prince Edward Island", 
                   "Yukon", "Northwest Territories", "Nunavut"]
combo.pack()

tk.Button(root, text="Submit", command=show_data).pack()

root.mainloop()

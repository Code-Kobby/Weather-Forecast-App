import tkinter as tk
from tkinter import messagebox
import requests
import json
import os


class WeatherTaskApp:
    def _init_(self, root):
        self.root = root
        self.root.title("Weather & Task Manager")
        self.root.geometry("500x550")
        self.root.resizable(True , True)

        self.task_file = "tasks.json"
        self.api_key = "10cccd439f5828b256a5cc7319b01dcb"  # Replace with your OpenWeatherMap API key
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"

        self.load_tasks()

        # Weather Section
        self.weather_frame = tk.Frame(self.root, padx=10, pady=10, bg="#87CEEB")
        self.weather_frame.pack(fill="x")

        self.weather_label = tk.Label(
            self.weather_frame,
            text="Weather Forecast",
            font=("Helvetica", 16, "bold"),
            bg="#87CEEB",
        )
        self.weather_label.pack()

        self.city_label = tk.Label(self.weather_frame, text="City:", bg="#87CEEB")
        self.city_label.pack(side="left", padx=5)

        self.city_entry = tk.Entry(self.weather_frame)
        self.city_entry.pack(side="left", padx=5)

        self.get_weather_btn = tk.Button(
            self.weather_frame, text="Get Weather", command=self.get_weather
        )
        self.get_weather_btn.pack(side="left", padx=5)

        self.weather_result = tk.Label(
            self.weather_frame, text="", bg="#87CEEB", font=("Helvetica", 12)
        )
        self.weather_result.pack(pady=5)

        # Task Management Section
        self.task_frame = tk.Frame(self.root, padx=10, pady=10)
        self.task_frame.pack(fill="both", expand=True)

        self.task_label = tk.Label(
            self.task_frame, text="Task Manager", font=("Helvetica", 16, "bold")
        )
        self.task_label.pack()

        self.task_entry = tk.Entry(self.task_frame, width=40)
        self.task_entry.pack(pady=5)

        self.add_task_btn = tk.Button(
            self.task_frame, text="Add Task", command=self.add_task
        )
        self.add_task_btn.pack(pady=5)

        self.task_listbox = tk.Listbox(self.task_frame, width=40, height=15)
        self.task_listbox.pack(pady=5, side="left", fill="both")

        self.scrollbar = tk.Scrollbar(self.task_frame, orient="vertical")
        self.scrollbar.pack(side="right", fill="y")
        self.task_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.task_listbox.yview)

        self.mark_done_btn = tk.Button(
            self.task_frame, text="Mark as Done", command=self.mark_done
        )
        self.mark_done_btn.pack(pady=5)

        self.delete_task_btn = tk.Button(
            self.task_frame, text="Delete Task", command=self.delete_task
        )
        self.delete_task_btn.pack(pady=5)

        self.load_tasks_into_listbox()

    def get_weather(self):
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name!")
            return

        params = {"q": city, "appid": self.api_key, "units": "metric"}

        try:
            response = requests.get(self.base_url, params=params)
            data = response.json()
            if data.get("cod") != 200:
                raise ValueError(data.get("message", "City not found"))
            # Display the weather details
            weather_desc = data["weather"][0]["description"].capitalize()
            temp = data["main"]["temp"]
            self.weather_result.config(
                text=f"City: {data['name']}, Temp: {temp}°C, Weather: {weather_desc}"
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch weather: {e}")

    def add_task(self):
        task = self.task_entry.get().strip()
        if task:
            self.task_listbox.insert(tk.END, task)
            self.task_entry.delete(0, tk.END)
            self.save_tasks()
        else:
            messagebox.showwarning("Input Error", "Please enter a task!")

    def mark_done(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            task = self.task_listbox.get(selected_task_index)
            self.task_listbox.delete(selected_task_index)
            self.task_listbox.insert(tk.END, f"{task} (Done)")
            self.save_tasks()
        else:
            messagebox.showwarning("Selection Error", "Please select a task!")

    def delete_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            self.task_listbox.delete(selected_task_index)
            self.save_tasks()
        else:
            messagebox.showwarning("Selection Error", "Please select a task!")

    def save_tasks(self):
        tasks = self.task_listbox.get(0, tk.END)
        with open(self.task_file, "w") as f:
            json.dump(tasks, f)

    def load_tasks(self):
        if os.path.exists(self.task_file):
            with open(self.task_file, "r") as f:
                self.tasks = json.load(f)
        else:
            self.tasks = []

    def load_tasks_into_listbox(self):
        for task in self.tasks:
            self.task_listbox.insert(tk.END, task)


if _name_ == "_main_":
    root = tk.Tk()
    app = WeatherTaskApp(root)
    root.mainloop()

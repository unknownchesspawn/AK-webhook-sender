import tkinter as tk
from tkinter import messagebox, ttk
import requests
import threading
import time
from PIL import Image, ImageTk
from io import BytesIO

class DiscordWebhookSender:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("AK Webhook Sender")
        self.window.geometry("500x500")  
        self.window.configure(bg="#2E3440")  # background :)

        # Set the window icon
        self.set_window_icon("https://avatars.githubusercontent.com/u/194596336?v=4")

        # Custom font
        self.custom_font = ("Arial", 10)

        # Create main frames
        self.input_frame = tk.Frame(self.window, bg="#2E3440")
        self.input_frame.pack(pady=10, padx=10, fill="x")

        self.button_frame = tk.Frame(self.window, bg="#2E3440")
        self.button_frame.pack(pady=10, padx=10, fill="x")

        self.status_frame = tk.Frame(self.window, bg="#2E3440")
        self.status_frame.pack(pady=10, padx=10, fill="x")

        # Create input fields
        self.webhook_url_label = tk.Label(self.input_frame, text="Webhook URL:", bg="#2E3440", fg="#D8DEE9", font=self.custom_font)
        self.webhook_url_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.webhook_url_entry = tk.Entry(self.input_frame, width=50, bg="#3B4252", fg="#D8DEE9", insertbackground="#D8DEE9", font=self.custom_font)
        self.webhook_url_entry.grid(row=0, column=1, padx=5, pady=5)

        self.message_label = tk.Label(self.input_frame, text="Message:", bg="#2E3440", fg="#D8DEE9", font=self.custom_font)
        self.message_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.message_entry = tk.Text(self.input_frame, height=10, width=50, bg="#3B4252", fg="#D8DEE9", insertbackground="#D8DEE9", font=self.custom_font)
        self.message_entry.grid(row=1, column=1, padx=5, pady=5)

        self.times_to_send_label = tk.Label(self.input_frame, text="Times to send:", bg="#2E3440", fg="#D8DEE9", font=self.custom_font)
        self.times_to_send_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.times_to_send_entry = tk.Entry(self.input_frame, width=10, bg="#3B4252", fg="#D8DEE9", insertbackground="#D8DEE9", font=self.custom_font)
        self.times_to_send_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        self.delay_label = tk.Label(self.input_frame, text="Delay (seconds):", bg="#2E3440", fg="#D8DEE9", font=self.custom_font)
        self.delay_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.delay_entry = tk.Entry(self.input_frame, width=10, bg="#3B4252", fg="#D8DEE9", insertbackground="#D8DEE9", font=self.custom_font)
        self.delay_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        self.delete_hook_var = tk.BooleanVar()
        self.delete_hook_checkbox = tk.Checkbutton(self.input_frame, text="Delete webhook after spam", variable=self.delete_hook_var, bg="#2E3440", fg="#D8DEE9", selectcolor="#3B4252", font=self.custom_font)
        self.delete_hook_checkbox.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        # Create buttons (Send, Cancel, Clear)
        self.send_button = tk.Button(self.button_frame, text="Send", command=self.start_sending, bg="#4C566A", fg="#D8DEE9", activebackground="#5E81AC", activeforeground="#D8DEE9", font=self.custom_font)
        self.send_button.grid(row=0, column=0, padx=5, pady=5)

        self.cancel_button = tk.Button(self.button_frame, text="Cancel", command=self.cancel_sending, bg="#4C566A", fg="#D8DEE9", activebackground="#5E81AC", activeforeground="#D8DEE9", font=self.custom_font)
        self.cancel_button.grid(row=0, column=1, padx=5, pady=5)

        self.clear_button = tk.Button(self.button_frame, text="Clear", command=self.clear_fields, bg="#4C566A", fg="#D8DEE9", activebackground="#5E81AC", activeforeground="#D8DEE9", font=self.custom_font)
        self.clear_button.grid(row=0, column=2, padx=5, pady=5)

        # Create status label and progress bar
        self.status_label = tk.Label(self.status_frame, text="", bg="#2E3440", fg="#D8DEE9", font=self.custom_font)
        self.status_label.pack(pady=5)

        self.progress = ttk.Progressbar(self.status_frame, orient="horizontal", length=450, mode="determinate")
        self.progress.pack(pady=5, fill="x", padx=10)

        self.sending = False

    def set_window_icon(self, icon_url):
        try:
            response = requests.get(icon_url)
            image_data = response.content
            image = Image.open(BytesIO(image_data))
            photo = ImageTk.PhotoImage(image)
            self.window.iconphoto(False, photo)
        except Exception as e:
            print(f"Failed to set window icon: {e}")

    def start_sending(self):
        if not self.sending:
            self.sending = True
            threading.Thread(target=self.send_message).start()

    def cancel_sending(self):
        self.sending = False
        self.status_label.config(text="Sending cancelled")

    def send_message(self):
        webhook_url = self.webhook_url_entry.get()
        message = self.message_entry.get("1.0", "end-1c")
        delete_hook = self.delete_hook_var.get()

        try:
            times_to_send = int(self.times_to_send_entry.get())
            if times_to_send <= 0:
                raise ValueError("Times to send must be a positive integer")
        except ValueError as e:
            self.window.after(0, messagebox.showerror, "Error", str(e))
            self.sending = False
            return

        try:
            delay = float(self.delay_entry.get())
            if delay < 0:
                raise ValueError("Delay must be a non-negative number")
        except ValueError as e:
            self.window.after(0, messagebox.showerror, "Error", str(e))
            self.sending = False
            return

        if not webhook_url or not message:
            self.window.after(0, messagebox.showerror, "Error", "Please fill in both fields")
            self.sending = False
            return

        self.progress["maximum"] = times_to_send
        self.progress["value"] = 0

        for i in range(times_to_send):
            if not self.sending:
                break
            try:
                data = requests.post(webhook_url, json={"content": message})
                if data.status_code == 204:
                    self.window.after(0, self.status_label.config, {"text": f"Message {i+1}/{times_to_send} sent successfully!"})
                else:
                    self.window.after(0, self.status_label.config, {"text": f"Error sending message {i+1}/{times_to_send}: {data.status_code}"})
            except requests.exceptions.RequestException as e:
                self.window.after(0, self.status_label.config, {"text": f"Error sending message {i+1}/{times_to_send}: {str(e)}"})
            self.progress["value"] = i + 1
            self.window.update_idletasks()
            time.sleep(delay)

        if delete_hook and self.sending:
            try:
                requests.delete(webhook_url)
                self.window.after(0, self.status_label.config, {"text": "Webhook deleted"})
            except requests.exceptions.RequestException as e:
                self.window.after(0, self.status_label.config, {"text": f"Error deleting webhook: {str(e)}"})

        self.sending = False

    def clear_fields(self):
        self.webhook_url_entry.delete(0, tk.END)
        self.message_entry.delete("1.0", tk.END)
        self.times_to_send_entry.delete(0, tk.END)
        self.delay_entry.delete(0, tk.END)
        self.status_label.config(text="")
        self.progress["value"] = 0

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = DiscordWebhookSender()
    app.run()

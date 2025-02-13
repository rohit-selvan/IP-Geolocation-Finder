import tkinter as tk
from tkinter import filedialog, messagebox
import requests

class IPGeolocationFinder(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("IP Geolocation Finder")
        self.geometry("600x500")
        self.configure(bg="#e8f4f8")  # Soft pastel background
        self.create_widgets()

    def create_widgets(self):
        # Title
        tk.Label(self, text="IP Geolocation Finder", font=("Verdana", 24, "bold"), bg="#e8f4f8", fg="#2c3e50").pack(pady=20)
        
        # IP Address input
        tk.Label(self, text="Enter an IP Address:", font=("Verdana", 14), bg="#e8f4f8").pack(pady=5)
        self.ip_entry = tk.Entry(self, font=("Verdana", 14), width=30)
        self.ip_entry.pack(pady=10)
        
        # Search button
        tk.Button(self, text="Find Location", command=self.find_location, font=("Verdana", 14), bg="#3498db", fg="white", width=15).pack(pady=10)
        
        # Export button
        tk.Button(self, text="Export to File", command=self.export_to_file, font=("Verdana", 14), bg="#2ecc71", fg="white", width=15).pack(pady=10)
        
        # Result display
        self.result_text = tk.Text(self, font=("Verdana", 12), height=10, width=70, state=tk.DISABLED, wrap=tk.WORD)
        self.result_text.pack(pady=10)

    def find_location(self):
        ip_address = self.ip_entry.get().strip()
        if not ip_address:
            messagebox.showwarning("Input Error", "Please enter an IP address.")
            return
        
        try:
            response = requests.get(f"https://ipinfo.io/{ip_address}/json")
            data = response.json()
            self.display_location(data)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def display_location(self, data):
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete("1.0", tk.END)
        if "error" in data:
            self.result_text.insert(tk.END, "Invalid IP address or data not found.\n")
        else:
            location = data.get("loc", "N/A").split(",")
            map_link = f"https://www.google.com/maps?q={location[0]},{location[1]}" if len(location) > 1 else "N/A"
            result = (
                f"IP Address: {data.get('ip', 'N/A')}\n"
                f"City: {data.get('city', 'N/A')}\n"
                f"Region: {data.get('region', 'N/A')}\n"
                f"Country: {data.get('country', 'N/A')}\n"
                f"Location: Latitude {location[0] if len(location) > 0 else 'N/A'}, Longitude {location[1] if len(location) > 1 else 'N/A'}\n"
                f"ISP: {data.get('org', 'N/A')}\n"
                f"Google Maps Link: {map_link}\n"
            )
            self.result_text.insert(tk.END, result)
        self.result_text.config(state=tk.DISABLED)
    
    def export_to_file(self):
        content = self.result_text.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("No Data", "No data to export. Please search for an IP address first.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")], title="Save File")
        if file_path:
            try:
                with open(file_path, "w") as file:
                    file.write(content)
                messagebox.showinfo("Success", f"Data exported to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while saving: {str(e)}")

if __name__ == "__main__":
    app = IPGeolocationFinder()
    app.mainloop()

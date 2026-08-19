import socket
import threading
import time
import struct
import requests
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
import random
import datetime
import ipaddress
import pytz
import os
import tkinter as tk
from tkinter import messagebox

# Define a simple neural network
class SimpleNet(nn.Module):
    def __init__(self):
        super(SimpleNet, self).__init__()
        self.fc1 = nn.Linear(10, 50)
        self.fc2 = nn.Linear(50, 100)
        self.fc3 = nn.Linear(100, 4096)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = torch.sigmoid(self.fc3(x))
        return x

# Initialize the neural network
model = SimpleNet()

# Dummy training data
X_train = torch.randn(1000, 10)
y_train = torch.randn(1000, 4096)

# Create a DataLoader
train_dataset = TensorDataset(X_train, y_train)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

# Define loss function and optimizer
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training loop
num_epochs = 5
for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0
    for inputs, targets in train_loader:
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
    print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {running_loss/len(train_loader):.4f}')

# Function to perform calculations on GPU using the trained network
def calculate_on_gpu(client_data, client_socket):
    try:
        model.eval()
        with torch.no_grad():
            data = torch.tensor(client_data, dtype=torch.float32)
            result = model(data)
            client_socket.sendall(result.numpy().tobytes())
    except Exception as e:
        print(f"[!] Error processing data on GPU: {e}")

# Function to resolve hostname using Cloudflare DNS
def resolve_hostname(hostname):
    try:
        resolver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        resolver.connect((CLOUDFLARE_DNS, 53))
        resolver.sendall(b'\x1d\x20\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00' + bytes(hostname, 'utf-8') + b'\x00\x00\x01\x00\x01')
        response = resolver.recv(1024)
        resolver.close()
        return socket.inet_ntoa(response[-4:])
    except Exception as e:
        print(f"[!] Error resolving hostname: {e}")
        return None

# Function to get global IP address
def get_global_ip():
    try:
        response = requests.get("https://api.ipify.org?format=text")
        return response.text
    except Exception as e:
        print(f"[!] Error getting global IP: {e}")
        return "127.0.0.1"

# Function to send heartbeat to Cloudflare DNS
def send_heartbeat():
    while True:
        try:
            resolver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            resolver.connect((CLOUDFLARE_DNS, 53))
            resolver.sendall(b'HEARTBEAT')
            resolver.close()
            time.sleep(3600)
        except Exception as e:
            print(f"[!] Error sending heartbeat: {e}")

# Function to handle client connections
def handle_client(client_socket):
    client_socket.settimeout(60)

    while True:
        try:
            client_data = client_socket.recv(4096)
            if not client_data:
                break

            calculate_on_gpu(client_data, client_socket)

            request_line = client_data.split(b'\r\n')[0].decode('utf-8')
            method, url, _ = request_line.split()
            
            if method == "CONNECT":
                host = url.split(':')[0]
                port = int(url.split(':')[1])
            else:
                host = url.split('/')[2]
                port = 80

            resolved_ip = resolve_hostname(host)
            if not resolved_ip:
                break

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as internet_socket:
                internet_socket.connect((resolved_ip, port))
                internet_socket.sendall(client_data)
                while True:
                    internet_data = internet_socket.recv(4096)
                    if not internet_data:
                        break
                    client_socket.sendall(internet_data)
        except socket.timeout:
            print("[*] Connection timed out")
            break
        except Exception as e:
            print(f"[!] Error handling client: {e}")
            break

    client_socket.close()

# Function to calculate subnet broadcasts
def calculate_subnet_broadcasts(global_ip):
    ip = ipaddress.ip_address(global_ip)
    networks = [
        ipaddress.ip_network(f"{ip}/8", strict=False),
        ipaddress.ip_network(f"{ip}/16", strict=False),
        ipaddress.ip_network(f"{ip}/24", strict=False)
    ]
    return [str(network.broadcast_address) for network in networks]

# Function to listen for broadcasts
def listen_for_broadcasts(port, online_ips, gui_update_func, broadcast_level):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind(('', port))
        while True:
            data, addr = sock.recvfrom(1024)
            message = data.decode()
            if f"I have the baton {broadcast_level}" in message and addr[0] not in online_ips:
                online_ips.append(addr[0])
            gui_update_func(addr[0], message, broadcast_level)

# Function to broadcast messages
def broadcast_message(port, message, broadcast_address, interval=5):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        while True:
            sock.sendto(message.encode(), (broadcast_address, port))
            time.sleep(interval)

# Function to manage the baton
def manage_baton(port, online_ips, gui_update_baton_func, broadcast_level, tz):
    while True:
        now = datetime.datetime.now(tz)
        next_midnight = datetime.datetime.combine(now.date() + datetime.timedelta(days=1), datetime.time(0, 0, tzinfo=tz))
        time_to_midnight = (next_midnight - now).total_seconds()
        time.sleep(time_to_midnight)

        if online_ips:
            new_baton_holder = random.choice(online_ips)
            gui_update_baton_func(new_baton_holder, broadcast_level)

            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.sendto(f"You have the baton {broadcast_level}".encode(), (new_baton_holder, port))

            online_ips.clear()

# Function to ping IPs at the same level
def ping_ips_same_level(online_ips, broadcast_level):
    while True:
        time.sleep(1)
        for ip in online_ips:
            for dest_ip in online_ips:
                if ip != dest_ip:
                    try:
                        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                            sock.settimeout(1)
                            sock.sendto("Ping".encode(), (dest_ip, 873))
                            response, _ = sock.recvfrom(1024)
                            print(f"Received response from {dest_ip}: {response.decode()}")
                    except socket.timeout:
                        print(f"No response from {dest_ip}")

# GUI application for managing broadcasts and batons
class BroadcastApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Broadcast and Baton Management")
        self.geometry("600x500")

        self.global_ip = get_global_ip()
        self.subnet_broadcasts = calculate_subnet_broadcasts(self.global_ip)
        self.online_ips_8 = []
        self.online_ips_16 = []
        self.online_ips_24 = []
        self.current_baton_holder_8 = "None"
        self.current_baton_holder_16 = "None"
        self.current_baton_holder_24 = "None"

        self.tz = pytz.utc

        self.create_widgets()
        self.update_global_ip()
        self.update_subnet_broadcasts()

        self.start_threads()

    def create_widgets(self):
        self.global_ip_label = tk.Label(self, text="Global IP: ")
        self.global_ip_label.pack()

        self.baton_holder_label_8 = tk.Label(self, text="Current Baton Holder (/8): ")
        self.baton_holder_label_8.pack()
        
        self.baton_holder_label_16 = tk.Label(self, text="Current Baton Holder (/16): ")
        self.baton_holder_label_16.pack()
        
        self.baton_holder_label_24 = tk.Label(self, text="Current Baton Holder (/24): ")
        self.baton_holder_label_24.pack()

        self.online_ips_label_8 = tk.Label(self, text="Online IPs (/8): ")
        self.online_ips_label_8.pack()

        self.online_ips_listbox_8 = tk.Listbox(self)
        self.online_ips_listbox_8.pack(fill=tk.BOTH, expand=True)

        self.online_ips_label_16 = tk.Label(self, text="Online IPs (/16): ")
        self.online_ips_label_16.pack()

        self.online_ips_listbox_16 = tk.Listbox(self)
        self.online_ips_listbox_16.pack(fill=tk.BOTH, expand=True)

        self.online_ips_label_24 = tk.Label(self, text="Online IPs (/24): ")
        self.online_ips_label_24.pack()

        self.online_ips_listbox_24 = tk.Listbox(self)
        self.online_ips_listbox_24.pack(fill=tk.BOTH, expand=True)

    def update_global_ip(self):
        self.global_ip_label.config(text=f"Global IP: {self.global_ip}")

    def update_subnet_broadcasts(self):
        self.baton_holder_label_8.config(text=f"Current Baton Holder (/8): {self.current_baton_holder_8}")
        self.baton_holder_label_16.config(text=f"Current Baton Holder (/16): {self.current_baton_holder_16}")
        self.baton_holder_label_24.config(text=f"Current Baton Holder (/24): {self.current_baton_holder_24}")

    def update_online_ips_listbox(self, listbox, online_ips):
        listbox.delete(0, tk.END)
        for ip in online_ips:
            listbox.insert(tk.END, ip)

    def update_online_ips(self, ip, message, broadcast_level):
        if broadcast_level == "/8":
            if ip not in self.online_ips_8:
                self.online_ips_8.append(ip)
            self.update_online_ips_listbox(self.online_ips_listbox_8, self.online_ips_8)
        elif broadcast_level == "/16":
            if ip not in self.online_ips_16:
                self.online_ips_16.append(ip)
            self.update_online_ips_listbox(self.online_ips_listbox_16, self.online_ips_16)
        elif broadcast_level == "/24":
            if ip not in self.online_ips_24:
                self.online_ips_24.append(ip)
            self.update_online_ips_listbox(self.online_ips_listbox_24, self.online_ips_24)

    def update_baton_holder(self, baton_holder, broadcast_level):
        if broadcast_level == "/8":
            self.current_baton_holder_8 = baton_holder
        elif broadcast_level == "/16":
            self.current_baton_holder_16 = baton_holder
        elif broadcast_level == "/24":
            self.current_baton_holder_24 = baton_holder
        self.update_subnet_broadcasts()

    def start_threads(self):
        threading.Thread(target=listen_for_broadcasts, args=(873, self.online_ips_8, self.update_online_ips, "/8")).start()
        threading.Thread(target=listen_for_broadcasts, args=(874, self.online_ips_16, self.update_online_ips, "/16")).start()
        threading.Thread(target=listen_for_broadcasts, args=(875, self.online_ips_24, self.update_online_ips, "/24")).start()
        threading.Thread(target=broadcast_message, args=(873, f"I have the baton /8", self.subnet_broadcasts[0])).start()
        threading.Thread(target=broadcast_message, args=(874, f"I have the baton /16", self.subnet_broadcasts[1])).start()
        threading.Thread(target=broadcast_message, args=(875, f"I have the baton /24", self.subnet_broadcasts[2])).start()
        threading.Thread(target=manage_baton, args=(873, self.online_ips_8, self.update_baton_holder, "/8", self.tz)).start()
        threading.Thread(target=manage_baton, args=(874, self.online_ips_16, self.update_baton_holder, "/16", self.tz)).start()
        threading.Thread(target=manage_baton, args=(875, self.online_ips_24, self.update_baton_holder, "/24", self.tz)).start()
        threading.Thread(target=ping_ips_same_level, args=(self.online_ips_8, "/8")).start()
        threading.Thread(target=ping_ips_same_level, args=(self.online_ips_16, "/16")).start()
        threading.Thread(target=ping_ips_same_level, args=(self.online_ips_24, "/24")).start()

# Main function to start the proxy server and GUI application
def main():
    global_ip = get_global_ip()
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Proxy Information", f"Proxy is running on IP: {global_ip}, Port: {FREENET_PROXY_PORT}\nGlobal IP: {global_ip}")

    heartbeat_thread = threading.Thread(target=send_heartbeat)
    heartbeat_thread.start()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((FREENET_PROXY_ADDRESS, FREENET_PROXY_PORT))
    server.listen(5)
    print(f'[*] Listening on {FREENET_PROXY_ADDRESS}:{FREENET_PROXY_PORT}')

    proxy_thread = threading.Thread(target=proxy_server, args=(server,))
    proxy_thread.start()

    app = BroadcastApp()
    app.mainloop()

def proxy_server(server):
    while True:
        client_socket, addr = server.accept()
        print(f'[*] Accepted connection from {addr[0]}:{addr[1]}')
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == '__main__':
    FREENET_PROXY_ADDRESS = '127.0.0.1'
    FREENET_PROXY_PORT = 54356
    CLOUDFLARE_DNS = '1.1.1.1'
    main()

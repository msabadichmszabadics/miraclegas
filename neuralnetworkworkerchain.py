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
from tkinter import Tk, Label, Button, filedialog, Listbox, END, Text
from concurrent.futures import ThreadPoolExecutor, as_completed
import psutil
import uuid
import subprocess
import platform
from scapy.layers.inet import IP, ICMP, traceroute
import json
from pathlib import Path
import multiprocessing as mp
import queue
import dns.resolver
from queue import Queue
import concurrent.futures
import gc
from scapy.all import *
import datetime
import speedtest
# Check if CUDA is available
use_cuda = torch.cuda.is_available()
device = torch.device("cuda" if use_cuda else "cpu")
print(f'Using device: {device}')

# List to store loaded IPs and their filenames
ips_dict = {}
ip_list = {}
#ip = None
online_ips_8 = {}
online_ips_16 = {}
online_ips_24 = {}
ips = {}
ip = {}
results = {}
result = {}
json_string1 = {}
json_string2 = {}
json_string = {}
gc.enable()

#result = None
#results = None

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
train_loader = DataLoader(train_dataset, batch_size=64, shuffle=False)

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

def initiate_tasks(tasks):
    max_workers = 4096
    with ThreadPoolExecutor(max_workers) as executor:
        futures = [executor.submit(task) for task in tasks]
        
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Thread generated an exception: {e}")



def calculate_on_gpu():
    max_workers = 512
    model.eval()
     # Example inputs and tasks
    batch_size = 64
    num_tasks = 1 # Number of tasks to parallelize
    your_task_args = [torch.randn(batch_size, 1, 8, 8) for _ in range(num_tasks)]  # Example batch of 28x28 grayscale images
    
    with torch.no_grad():
        # Using ThreadPoolExecutor for parallel execution of tasks
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_task = {executor.submit(send_heartbeat1): task for task in your_task_args}
            
            for future in concurrent.futures.as_completed(future_to_task):
                try:
                    result = future.result()

                except Exception as e:
                    print(f'Task generated an exception: {e}')
    gc.collect()
    torch.cuda.empty_cache()  # Clear GPU cache after each calculation
    return results.numpy().cpu()
    
def calculate_on_gpu0(ip):
    max_workers = 512
    model.eval()
     # Example inputs and tasks
    batch_size = 64
    num_tasks = 1  # Number of tasks to parallelize
    your_task_args = [torch.randn(batch_size, 1, 8, 8) for _ in range(num_tasks)]  # Example batch of 28x28 grayscale images
    with torch.no_grad():
        # Using ThreadPoolExecutor for parallel execution of tasks
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_task = {executor.submit(scan_ports, ip): task for task in your_task_args}
            
            for future in concurrent.futures.as_completed(future_to_task):
                try:
                    result = future.result()

                except Exception as e:
                    print(f'Task generated an exception: {e}')
    gc.collect()
    torch.cuda.empty_cache()  # Clear GPU cache after each calculation
    return results.numpy().cpu()
        
def calculate_on_gpu1(ip):
    max_workers = 512
    model.eval()
     # Example inputs and tasks
    batch_size = 64
    num_tasks = 1  # Number of tasks to parallelize
    your_task_args = [torch.randn(batch_size, 1, 8, 8) for _ in range(num_tasks)]  # Example batch of 28x28 grayscale images
    with torch.no_grad():
        # Using ThreadPoolExecutor for parallel execution of tasks
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_task = {executor.submit(broadcast_ip, ip): task for task in your_task_args}
            
            for future in concurrent.futures.as_completed(future_to_task):
                try:
                    result = future.result()

                except Exception as e:
                    print(f'Task generated an exception: {e}')
    gc.collect()
    torch.cuda.empty_cache()  # Clear GPU cache after each calculation
    return results.numpy().cpu()

    
def calculate_on_gpu2(ip):
    max_workers = 512
    model.eval()
     # Example inputs and tasks
    batch_size = 64
    num_tasks = 1  # Number of tasks to parallelize
    your_task_args = [torch.randn(batch_size, 1, 8, 8) for _ in range(num_tasks)]  # Example batch of 28x28 grayscale images
    with torch.no_grad():
        # Using ThreadPoolExecutor for parallel execution of tasks
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_task = {executor.submit(query_ip, ip): task for task in your_task_args}
            
            for future in concurrent.futures.as_completed(future_to_task):
                try:
                    result = future.result()

                except Exception as e:
                    print(f'Task generated an exception: {e}')
    gc.collect()
    torch.cuda.empty_cache()  # Clear GPU cache after each calculation
    return results.numpy().cpu()


def calculate_on_gpu3(ip):
    max_workers = 512
    model.eval()
     # Example inputs and tasks
    batch_size = 64
    num_tasks = 1  # Number of tasks to parallelize
    your_task_args = [torch.randn(batch_size, 1, 8, 8) for _ in range(num_tasks)]  # Example batch of 28x28 grayscale images
    with torch.no_grad():
        # Using ThreadPoolExecutor for parallel execution of tasks
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_task = {executor.submit(pingsweep, ip): task for task in your_task_args}
            
            for future in concurrent.futures.as_completed(future_to_task):
                try:
                    result = future.result()
  
                except Exception as e:
                    print(f'Task generated an exception: {e}')
    gc.collect()
    torch.cuda.empty_cache()  # Clear GPU cache after each calculation
    return results.numpy().cpu()
                

        
        
def calculate_on_gpu4(ip):
    max_workers = 512
    model.eval()
     # Example inputs and tasks
    batch_size = 64
    num_tasks = 1  # Number of tasks to parallelize
    your_task_args = [torch.randn(batch_size, 1, 8, 8) for _ in range(num_tasks)]  # Example batch of 28x28 grayscale images
    with torch.no_grad():
        # Using ThreadPoolExecutor for parallel execution of tasks
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_task = {executor.submit(perform_traceroute, ip): task for task in your_task_args}
            
            for future in concurrent.futures.as_completed(future_to_task):
                try:
                    result = future.result()

                except Exception as e:
                    print(f'Task generated an exception: {e}')
    gc.collect()
    torch.cuda.empty_cache()  # Clear GPU cache after each calculation
    return results.numpy().cpu()

        
    
    
def calculate_on_gpu5(ip):
    max_workers = 512
    model.eval()
     # Example inputs and tasks
    batch_size = 64
    num_tasks = 1  # Number of tasks to parallelize
    your_task_args = [torch.randn(batch_size, 1, 8, 8) for _ in range(num_tasks)]  # Example batch of 28x28 grayscale images
    with torch.no_grad():
        # Using ThreadPoolExecutor for parallel execution of tasks
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_task = {executor.submit(get_dns_records, ip): task for task in your_task_args}
            
            for future in concurrent.futures.as_completed(future_to_task):
                try:
                    result = future.result()

                except Exception as e:
                    print(f'Task generated an exception: {e}')
    gc.collect()
    torch.cuda.empty_cache()  # Clear GPU cache after each calculation
    return results.numpy().cpu()


def calculate_on_gpu6(ip):
    max_workers = 512
    model.eval()
     # Example inputs and tasks
    batch_size = 64
    num_tasks = 1  # Number of tasks to parallelize
    your_task_args = [torch.randn(batch_size, 1, 8, 8) for _ in range(num_tasks)]  # Example batch of 8x2 grayscale images
    with torch.no_grad():
        # Using ThreadPoolExecutor for parallel execution of tasks
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_task = {executor.submit(perform_http_requests, ip): task for task in your_task_args}
            
            for future in concurrent.futures.as_completed(future_to_task):
                try:
                    result = future.result()

                except Exception as e:
                    print(f'Task generated an exception: {e}')
    gc.collect()
    torch.cuda.empty_cache()  # Clear GPU cache after each calculation
    return results.numpy().cpu()


# Function to perform calculations on GPU using the trained network
def calculate_on_gpu7(client_data, client_socket):
    try:
        model.eval()
        with torch.no_grad():
            data = torch.tensor(client_data, dtype=torch.float32)
            result = model(data)
            client_socket.sendall(result.numpy().tobytes())
    except Exception as e:
        print(f"[!] Error processing data on GPU: {e}")
        
def test_speed():
    try:
        # Create a Speedtest object
        st = speedtest.Speedtest()

        # Progress notification window
        progress_window = tk.Toplevel()
        progress_label = tk.Label(progress_window, text="Speed test in progress...")
        progress_label.pack()

        # Perform speed test
        st.get_best_server()
        download_speed = st.download() / 1024 / 1024  # Convert to Mbps
        upload_speed = st.upload() / 1024 / 1024  # Convert to Mbps
        ping = st.results.ping

        # Print results
        print("Download Speed: {:.2f} Mbps".format(download_speed))
        print("Upload Speed: {:.2f} Mbps".format(upload_speed))
        print("Ping: {:.2f} ms".format(ping))

        # Update progress label
        progress_label.config(
            text="Speed test completed. Download Speed: {:.2f} Mbps, Upload Speed: {:.2f} Mbps, Ping: {:.2f} ms".format(
                download_speed, upload_speed, ping))

        # Check if ping is greater than 800ms
        if ping > 800:
            messagebox.showerror("Slow Connection", "Your connection is slow (Ping > 800ms).")
            root.destroy()  # Close the tkinter window
        else:
            messagebox.showinfo("Connection Status", "Speed test completed successfully!")

            # Close the progress window after 3 seconds
            progress_window.after(3000, progress_window.destroy)
    except speedtest.ConfigRetrievalError as e:
        messagebox.showerror("Error", "Failed to retrieve Speedtest configuration. Please check your internet connection.")
    except Exception as e:
        messagebox.showerror("Error", "An unexpected error occurred: {}".format(str(e)))
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
def send_heartbeat1():
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

            calculate_on_gpu7(client_data, client_socket)

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



def scan_ports(ip):
    open_ports = []
    ports = {
        "TCP": [80, 443, 25, 110, 143, 22, 21, 389, 636, 23, 3389, 5900],
        "UDP": [53, 161, 162, 123, 514],
        # Add more handshake methods here
    }
    scan_ports_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    for port in ports:
            scan_ports_socket.settimeout(1)
            result = scan_ports_socket.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)
     


def pingsweep(ip):
    pingsweep_results = []

    icmp_request = IP(dst=str(ip)) / ICMP()
    reply = sr1(icmp_request, timeout=1, verbose=False)
 

def perform_traceroute(ip):
    try:
        traceroute_results = []
        buffer_ips = []

        # Perform traceroute
        hops = traceroute(ip, maxttl=255)[0]

        # Store traceroute results and prepare IPs for pingsweep
        for i, hop in enumerate(hops, start=1):
            hop_ip = hop[1].src
            traceroute_results.append({"hop": i, "ip": hop_ip})
            buffer_ips.append(hop_ip)
            
            # If the number of hops exceeds 25, pingsweep every 25th hop
            if len(hops) > 25 and i % 25 == 0:
                perform_traceroute(hop_ip)

       

        # Perform pingsweep on all hops
        pingsweep(buffer_ips)
         
    except Exception as e:
        print(f"Error performing traceroute: {e}")
        
def send_heartbeat(ip):
    handshake_methods = {
        "TCP": [80, 443, 25, 110, 143, 22, 21, 389, 636, 23, 3389, 5900],
        "UDP": [53, 161, 162, 123, 514],
        # Add more handshake methods here
    }

    global_ip = get_global_ip()  # Fetch global IP dynamically

    handshake_results = []
    global handshake_socket
    try:
        for method_name, ports in handshake_methods.items():
            for port in ports:
                try:
                    handshake_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    handshake_socket.settimeout(1)  # Set a timeout of 1 second
                    if result == 0:  # If the connection is successful
                        handshake_socket.sendall(global_ip.encode())
                        # Log successful handshake
                        handshake_results.append({
                            "ip": ip,
                            "method": method_name,
                            "port": port,
                            "status": "Success"
                        })
                        print(f"Heartbeat sent to {ip} using {method_name} ({port})")
                        log_handshake(ip, global_ip)  # Assuming log_handshake is defined elsewhere
                    else:
                        # Print failed handshake
                        handshake_results.append({
                            "ip": ip,
                            "method": method_name,
                            "port": port,
                            "status": "Failed: Connection refused"
                        })
                        print(f"Failed to send heartbeat to {ip} using {method_name} ({port}): Connection refused")
                except Exception as e:
                # Print failed handshake
                    handshake_results.append({
                        "ip": ip,
                        "method": method_name,
                        "port": port,
                        "status": f"Failed: {str(e)}" 
                    })
                    print(f"Failed to send heartbeat to {ip} using {method_name} ({port}): {str(e)}")
    except Exception as e:
        # Print failed handshake
        print(f"Failed to send heartbeat to {ip}: {str(e)}")
     
    # Save handshake results to JSON file
    save_handshake_results(handshake_results)
        


def broadcast_ip(ip):
    broadcast_results = []
    global broadcast_socket1
    global broadcast_socket2
    # Initialize an empty list to store broadcast results
    try:
        # Get the hostname of the local machine
        hostname = socket.gethostname()
        
        # Get the IP address associated with the hostname
        ip_address = socket.gethostbyname(hostname)
        
        global_ip1 = get_global_ip()  # Fetch global IP dynamically
        
        # Predefined ports for broadcasting
        handshake_methods = {
            "TCP": [80, 443, 25, 110, 143, 22, 21, 389, 636, 23, 3389, 5900],
            "UDP": [53, 161, 162, 123, 514],
            # Add more handshake methods here
        }
        
    # Log successful or failed broadcast for each protocol and port
        for protocol, ports in handshake_methods.items():
            for port in ports:
                try:
                    # Construct broadcast message
                    broadcast_message = f"My IP address is {ip_address} on port {port} using {protocol} protocol"
                    broadcast_socket1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    broadcast_socket1.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                    broadcast_socket2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    broadcast_socket2.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                    # Create a UDP socket
                    if protocol == 'UDP':
                        # Broadcast the message on the specified port
                        broadcast_socket1.sendto(broadcast_message.encode(), (global_ip1, port))
                        broadcast_socket1.close()
                    # Create a TCP socket
                    elif protocol == 'TCP':
                        broadcast_socket2.sendto(broadcast_message.encode(), (global_ip1, port))
                        broadcast_socket2.close()
                
                    print(f"Broadcasted IP address successfully on port {port} using {protocol} protocol")

                except Exception as e:
                    print(f"Failed to broadcast IP address on port {port} using {protocol} protocol: {str(e)}")

    except Exception as e:
        print(f"Error broadcasting IP address: {e}")
     

def query_ip(ip):
    query_results = []  # Initialize an empty list to store query results
    global query_socket
    try:
        # Predefined ports for querying
        query_ports = {
            "TCP": [80, 443, 25, 110, 143, 22, 21, 389, 636, 23, 3389, 5900],
            "UDP": [53, 161, 162, 123, 514],
            # Add more handshake methods here
        }
        
        # Log successful or failed query for each protocol and port
        for protocol, ports in query_ports.items():
            for port in ports:
                try:
                    query_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    query_socket.settimeout(1)  # Set timeout for connection attempt
                    # Attempt to connect to the IP address on the specified port
                    result = query_socket.connect_ex((ip, port))

                    query_socket.close()
                
                except Exception as e:
                    print(f"Failed to connect to {ip} on port {port} using {protocol} protocol: {str(e)}")
                    # Log failed query
                    query_results.append({
                        "ip": ip,
                        "port": port,
                        "protocol": protocol,
                        "status": f"Failed: {str(e)}"
                    })
        
    except Exception as e:
        print(f"Error querying IP address: {e}")
              
    
      
    
def get_dns_records(ip):
    records = {}
    record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME', 'SOA']
    # Serialize the dictionary to a JSON string
    json_string1 = json.dumps(ip)

    # Encode the JSON string to bytes
    json_bytes1 = json_string1.encode('utf-8')
    
    domain = get_domain_name(json_bytes1)
    for record_type in record_types:
        try:
            answers = dns.resolver.resolve(domain, record_type)
            records[record_type] = [answer.to_text() for answer in answers]
        except dns.resolver.NoAnswer:
            records[record_type] = []
        except dns.resolver.NXDOMAIN:
            records[record_type] = None
            print(f"The domain '{domain}' does not exist.")
            break
        except Exception as e:
            records[record_type] = None
            print(f"An error occurred while fetching {record_type} records: {e}")

    return records
         


def get_domain_name(ip):
    # Serialize the dictionary to a JSON string
    json_string = json.dumps(ip)

    # Encode the JSON string to bytes
    json_bytes = json_string.encode('utf-8')
    try:
        return socket.gethostbyaddr(json_bytes)
    except Exception as e:
        print(f"Error getting domain name for {ip}: {e}")
        return None
        
def perform_http_requests(ip):
    global_ip = get_global_ip()
    methods = ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"]
    # if not global_ip:
    #    return
   # for ip in ip_list:
   #     domain_name = get_domain_name()
   # if not domain_name:
   #     print(f"Skipping IP {ip} as no domain name found.")
   #     return

    http_results = []
    json_string2 = json.dumps(ip)

    # Encode the JSON string to bytes
    json_bytes2 = json_string2.encode('utf-8')
    domain_name = get_domain_name(json_bytes2)
    url = f"http://{domain_name}"
    for method in methods:
        try:
            response = requests.request(method, url, headers=headers, timeout=1)

        except requests.RequestException as e:
            print(f"Error performing HTTP {method} request to {url}: {e}")  
     

def save_handshake_results(handshake_results):

    try:
        with open(handshake_file_path, 'a') as handshake_file:
            json.dump(handshake_results, handshake_file, indent=4)
            handshake_file.write('\n')

    except Exception as e:
        print(f"Error saving handshake results: {e}")
        
def load_ip_file():
    global ips_dict
    global ip_list
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            new_ips = file.readlines()
        new_ips = [ip.strip() for ip in new_ips if ip.strip()]
        ip_list = new_ips
        if file_path not in ips_dict:
            ips_dict[file_path] = new_ips
            loaded_files_box.insert(tk.END, file_path)
            print(f"Loaded IPs from file {file_path}: {new_ips}")
        else:
            print(f"Ignore file {file_path} as it's already loaded.")
    else:
        print("No file selected.")

def update_global_ip(global_ip_label, global_ip):
    global_ip_label.config(text=f"Global IP: {global_ip}")

def update_subnet_broadcasts(baton_holder_label_8, baton_holder_label_16, baton_holder_label_24, current_baton_holder_8, current_baton_holder_16, current_baton_holder_24):
    baton_holder_label_8.config(text=f"Current Baton Holder (/8): {current_baton_holder_8}")
    baton_holder_label_16.config(text=f"Current Baton Holder (/16): {current_baton_holder_16}")
    baton_holder_label_24.config(text=f"Current Baton Holder (/24): {current_baton_holder_24}")

def update_online_ips_listbox(listbox, online_ips):
    listbox.delete(0, tk.END)
    for ip in online_ips:
        listbox.insert(tk.END, ip)

def update_online_ips(online_ips_8, online_ips_16, online_ips_24, ip, message, broadcast_level):
    if broadcast_level == "/8":
        if ip not in online_ips_8:
            online_ips_8.append(ip)
        update_online_ips_listbox(online_ips_listbox_8, online_ips_8)
    elif broadcast_level == "/16":
        if ip not in online_ips_16:
            online_ips_16.append(ip)
        update_online_ips_listbox(online_ips_listbox_16, online_ips_16)
    elif broadcast_level == "/24":
        if ip not in online_ips_24:
            online_ips_24.append(ip)
        update_online_ips_listbox(online_ips_listbox_24, online_ips_24)

def update_baton_holder(current_baton_holder_8, current_baton_holder_16, current_baton_holder_24, baton_holder, broadcast_level):
    if broadcast_level == "/8":
        current_baton_holder_8 = baton_holder
    elif broadcast_level == "/16":
        current_baton_holder_16 = baton_holder
    elif broadcast_level == "/24":
        current_baton_holder_24 = baton_holder
    update_subnet_broadcasts(current_baton_holder_8, current_baton_holder_16, current_baton_holder_24)

def start_threads(global_ip, online_ips_8, online_ips_16, online_ips_24, subnet_broadcasts, current_baton_holder_8, current_baton_holder_16, current_baton_holder_24, tz):
    threading.Thread(target=listen_for_broadcasts, args=(873, online_ips_8, update_online_ips, "/8")).start()
    threading.Thread(target=listen_for_broadcasts, args=(874, online_ips_16, update_online_ips, "/16")).start()
    threading.Thread(target=listen_for_broadcasts, args=(875, online_ips_24, update_online_ips, "/24")).start()
    threading.Thread(target=broadcast_message, args=(873, f"I have the baton /8", subnet_broadcasts[0])).start()
    threading.Thread(target=broadcast_message, args=(874, f"I have the baton /16", subnet_broadcasts[1])).start()
    threading.Thread(target=broadcast_message, args=(875, f"I have the baton /24", subnet_broadcasts[2])).start()
    threading.Thread(target=manage_baton, args=(873, online_ips_8, update_baton_holder, "/8", tz)).start()
    threading.Thread(target=manage_baton, args=(874, online_ips_16, update_baton_holder, "/16", tz)).start()
    threading.Thread(target=manage_baton, args=(875, online_ips_24, update_baton_holder, "/24", tz)).start()
    threading.Thread(target=ping_ips_same_level, args=(online_ips_8, "/8")).start()
    threading.Thread(target=ping_ips_same_level, args=(online_ips_16, "/16")).start()
    threading.Thread(target=ping_ips_same_level, args=(online_ips_24, "/24")).start()

def initiate_start(ips_dict):
    tasks = []
    for file_path, ips in ips_dict.items():
        for ip in ips:
            tasks.append(lambda ip=ip: calculate_on_gpu6(ip))
            tasks.append(lambda ip=ip: calculate_on_gpu5(ip))
            tasks.append(lambda ip=ip: calculate_on_gpu0(ip))
            tasks.append(lambda ip=ip: calculate_on_gpu(ip))
            tasks.append(lambda ip=ip: calculate_on_gpu2(ip))
            tasks.append(lambda ip=ip: calculate_on_gpu1(ip))
            tasks.append(lambda ip=ip: calculate_on_gpu3(ip))
            tasks.append(lambda ip=ip: calculate_on_gpu4(ip))
    initiate_tasks(tasks)
# Main function to start the proxy server and GUI application

def proxy_server(server):
    while True:
        client_socket, addr = server.accept()
        print(f'[*] Accepted connection from {addr[0]}:{addr[1]}')
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == '__main__':
    FREENET_PROXY_ADDRESS = '127.0.0.1'
    FREENET_PROXY_PORT = 54316
    CLOUDFLARE_DNS = '1.1.1.1'
    test_speed()
    global_ip = get_global_ip()
    subnet_broadcasts = calculate_subnet_broadcasts(global_ip)
    current_baton_holder_8 = "None"
    current_baton_holder_16 = "None"
    current_baton_holder_24 = "None"
    tz = pytz.utc
    messagebox.showinfo("Proxy Information", f"Proxy is running on IP: {global_ip}, Port: {FREENET_PROXY_PORT}\nGlobal IP: {global_ip}")

    heartbeat_thread = threading.Thread(target=send_heartbeat1)
    heartbeat_thread.start()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((FREENET_PROXY_ADDRESS, FREENET_PROXY_PORT))
    server.listen(5)
    print(f'[*] Listening on {FREENET_PROXY_ADDRESS}:{FREENET_PROXY_PORT}')

    proxy_thread = threading.Thread(target=proxy_server, args=(server,))
    proxy_thread.start()
    
        # Start threads
    start_threads(global_ip, online_ips_8, online_ips_16, online_ips_24, subnet_broadcasts, current_baton_holder_8, current_baton_holder_16, current_baton_holder_24, tz)
    
    # Create the root window
    root = tk.Tk()
    root.title("Broadcast and Baton Management")
    root.geometry("600x500")
    
    # Create widgets
    processes_text = Text(root, height=20, width=50)
    processes_text.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

    load_file_button = Button(root, text="Load IPs from File", command=load_ip_file)
    load_file_button.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

    loaded_files_label = Label(root, text="Files Loaded:")
    loaded_files_label.grid(row=2, column=0, sticky='w', padx=10)

    loaded_files_box = Listbox(root, width=40)
    loaded_files_box.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

    online_ips_label_8 = Label(root, text="Online IPs (/8): ")
    online_ips_label_8.grid(row=1, column=2, sticky='e', padx=10)

    online_ips_listbox_8 = Listbox(root)
    online_ips_listbox_8.grid(row=2, column=2, rowspan=4, padx=10, pady=5, sticky="nsew")

    online_ips_label_16 = Label(root, text="Online IPs (/16): ")
    online_ips_label_16.grid(row=1, column=3, sticky='e', padx=10)

    online_ips_listbox_16 = Listbox(root)
    online_ips_listbox_16.grid(row=2, column=3, rowspan=4, padx=10, pady=5, sticky="nsew")

    online_ips_label_24 = Label(root, text="Online IPs (/24): ")
    online_ips_label_24.grid(row=1, column=4, sticky='e', padx=10)

    online_ips_listbox_24 = Listbox(root)
    online_ips_listbox_24.grid(row=2, column=4, rowspan=4, padx=10, pady=5, sticky="nsew")

    global_ip_label = Label(root, text="Global IP: ")
    global_ip_label.grid(row=5, column=0, sticky='w', padx=10, pady=5)

    baton_holder_label_8 = Label(root, text="Current Baton Holder (/8): ")
    baton_holder_label_8.grid(row=6, column=0, sticky='w', padx=10, pady=5)

    baton_holder_label_16 = Label(root, text="Current Baton Holder (/16): ")
    baton_holder_label_16.grid(row=7, column=0, sticky='w', padx=10, pady=5)

    baton_holder_label_24 = Label(root, text="Current Baton Holder (/24): ")
    baton_holder_label_24.grid(row=8, column=0, sticky='w', padx=10, pady=5)

    start_traceroute_button = Button(root, text="Start", command=lambda: initiate_start(ips_dict))
    start_traceroute_button.grid(row=9, column=0, columnspan=2, padx=10, pady=5)



    root.mainloop()
    
    

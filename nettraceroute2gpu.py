import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from tkinter import Tk, Label, Button, filedialog, Listbox, END, Text
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed
import psutil
import gc
import socket
import os
import uuid
import subprocess
import platform
from traceroute import Traceroute
from scapy.layers.inet import IP, ICMP, traceroute
from scapy.all import srp, Ether, IP, ICMP
import json
from scapy.layers.inet import traceroute
from pathlib import Path
# Preallocate 8 GB of RAM
fixed_memory = np.zeros((8 * 1024 * 1024 * 1024 // np.dtype(np.uint8).itemsize,), dtype=np.uint8)  # 8 GB

# Check if CUDA is available
use_cuda = torch.cuda.is_available()
device = torch.device("cuda" if use_cuda else "cpu")
print(f'Using device: {device}')
gc.enable()

# Get the user's Documents folder
documents_folder = Path(os.path.expanduser('~')) / 'Documents'

# Create a folder for measurements inside Documents
measurements_folder = documents_folder / 'measurements'
measurements_folder.mkdir(parents=True, exist_ok=True)

# Define the file path for handshake results
handshake_file_path = measurements_folder / 'handshake_results.json'
portscan_file_path = measurements_folder/ 'portscan_results.json'
pingsweep_file_path = measurements_folder/ 'pingsweep_results.json'
traceroute_file_path = measurements_folder/ 'traceroute_results.json'

class SimpleNet(nn.Module):
    def __init__(self):
        super(SimpleNet, self).__init__()
        self.fc1 = nn.Linear(10, 50)
        self.fc2 = nn.Linear(50, 100)
        self.fc3 = nn.Linear(100, 100)  # Output size to match the payload length

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = torch.sigmoid(self.fc3(x))  # Using sigmoid to get output between 0 and 1
        return x

# Initialize the neural network
model = SimpleNet().to(device)

# Dummy training data
X_train = torch.randn(1000, 10).to(device)
y_train = torch.randn(1000, 100).to(device)

# Create a DataLoader
train_dataset = TensorDataset(X_train, y_train)
train_loader = DataLoader(train_dataset, batch_size=16, shuffle=False)

# Define loss function and optimizer
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training loop (shortened for demonstration purposes)
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


def scan_ports(ip, ports=[80, 443, 22, 21, 25, 8080]):
    open_ports = []

    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            result = sock.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)

    # Save results to JSON file
    save_results_to_json0(ip, open_ports)

def pingsweep(ip_range):
    pingsweep_results = []

    for ip in ip_range:
        # Craft the ICMP echo request packet
        icmp_request = IP(dst=str(ip)) / ICMP()

        # Send the ICMP echo request and receive response
        reply = sr1(icmp_request, timeout=1, verbose=False)

        # Check if the host is reachable (received ICMP echo reply)
        if reply and reply.haslayer(ICMP) and reply.getlayer(ICMP).type == 0:
            pingsweep_results.append({"ip": str(ip), "status": "reachable"})
        else:
            pingsweep_results.append({"ip": str(ip), "status": "unreachable"})

    # Save results to JSON file
    save_results_to_json1(pingsweep_results)

def perform_traceroute(ip):
    try:
        traceroute_results = []

        # Perform traceroute
        hops = traceroute(ip)

        # Store traceroute results
        for hop in hops:
            traceroute_results.append({"ip": hop[1].src})

        


    except Exception as e:
        print(f"Error saving traceroute results: {e}")

    # Append traceroute results to JSON file
        save_results_to_json2(traceroute_results)

def send_heartbeat(ip):
    handshake_methods = {
        "TCP": [80, 443, 25, 110, 143, 22, 21, 389, 636, 23, 3389, 5900],
        "UDP": [53, 161, 162, 123, 514],
        # Add more handshake methods here
    }

    global_ip = get_global_ip()  # Fetch global IP dynamically

    handshake_results = []

    try:
        for method_name, ports in handshake_methods.items():
            for port in ports:
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as handshake_socket:
                        handshake_socket.settimeout(1)  # Set a timeout of 1 second
                        result = handshake_socket.connect_ex((ip, port))
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
        
        
def save_results_to_json0(ip, open_ports):

    try:
        with open(portscan_file_path, 'a') as portscan_file:
            json.dump({"ip": ip, "open_ports": open_ports}, portscan_file, indent=4)
            portscan_file.write('\n')


    except Exception as e:
        print(f"Error saving portscan results: {e}")



def save_results_to_json1(pingsweep_results):
    try:
        with open(pingsweep_file_path, 'a') as pingsweep_file:
            json.dump({"results": pingsweep_results}, pingsweep_file, indent=4)
            pingsweep_file.write('\n')

    except Exception as e:
        print(f"Error saving handshake results: {e}") 
        

def save_results_to_json2(traceroute_results):
    try:
        with open(traceroute_file_path, 'a') as traceroute_file:
            json.dump({"results": traceroute_results}, traceroute_file, indent=4)
            traceroute_file.write('\n')

    except Exception as e:
        print(f"Error saving handshake results: {e}")    
             

def save_handshake_results(handshake_results):

    try:
        with open(handshake_file_path, 'a') as handshake_file:
            json.dump(handshake_results, handshake_file, indent=4)
            handshake_file.write('\n')

    except Exception as e:
        print(f"Error saving handshake results: {e}")

def get_global_ip():
    try:
        response = requests.get("https://api.ipify.org?format=text")
        return response.text.strip()  # Remove any leading or trailing whitespace
    except Exception as e:
        print(f"Error getting global IP: {e}")
        return "127.0.0.1"

# List to store loaded IPs and their filenames
ips_dict = {}

def load_ip_file():
    global ips_dict
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            new_ips = file.readlines()
        new_ips = [ip.strip() for ip in new_ips if ip.strip()]
        if file_path not in ips_dict:
            ips_dict[file_path] = new_ips
            loaded_files_box.insert(END, file_path)
            print(f"Loaded IPs from file {file_path}: {new_ips}")
        else:
            print(f"Ignore file {file_path} as it's already loaded.")
    else:
        print("No file selected.")

def initiate_tasks(tasks):
    max_workers = psutil.cpu_count()  # Use maximum CPU cores
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for task in tasks:
            futures.append(executor.submit(task))
        
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Thread generated an exception: {e}")

def initiate_start():
    tasks = []
    for file_path, ips in ips_dict.items():
        for ip in ips:
            tasks.append(lambda ip=ip: perform_traceroute(ip))
            tasks.append(lambda ip=ip: pingsweep(ip))
            tasks.append(lambda ip=ip: scan_ports(ip))
            tasks.append(lambda ip=ip: send_heartbeat(ip))
    initiate_tasks(tasks)
                
root = Tk()
root.title("networkmap")

# Label to display CPU/GPU usage
device_label_text = "Using GPU" if use_cuda else "Using CPU"
device_label = Label(root, text=device_label_text)
device_label.grid(row=5, columnspan=2)

# Define the Text widget to display processes
processes_text = Text(root, height=20, width=50)
processes_text.grid(row=6, columnspan=2)

load_file_button = Button(root, text="Load IPs from File", command=load_ip_file)
load_file_button.grid(row=3, columnspan=2)

loaded_files_label = Label(root, text="Files Loaded:")
loaded_files_label.grid(row=4, column=0)
loaded_files_box = Listbox(root, width=40)
loaded_files_box.grid(row=4, column=1)

start_traceroute_button = Button(root, text="Start", command=initiate_start)
start_traceroute_button.grid(row=22, columnspan=2)



root.mainloop()


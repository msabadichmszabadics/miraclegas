import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from tkinter import Tk, Label, Button, filedialog, Listbox, END, Text
import numpy as np
import os
import socket
import json
import multiprocessing as mp
from scapy.all import sr1, IP, ICMP

# Check if CUDA is available
use_cuda = torch.cuda.is_available()
device = torch.device("cuda" if use_cuda else "cpu")
print(f'Using device: {device}')

# Initialize queues for task and result
task_queue = mp.Queue()
result_queue = mp.Queue()

# Dictionary to store loaded IPs and their filenames
ips_dict = {}

# Get the user's Documents folder
documents_folder = os.path.join(os.path.expanduser('~'), 'Documents')

# Create a folder for measurements inside Documents
measurements_folder = os.path.join(documents_folder, 'measurements')
os.makedirs(measurements_folder, exist_ok=True)

# Define file paths for saving results
handshake_file_path = os.path.join(measurements_folder, 'handshake_results.json')
portscan_file_path = os.path.join(measurements_folder, 'portscan_results.json')
pingsweep_file_path = os.path.join(measurements_folder, 'pingsweep_results.json')
traceroute_file_path = os.path.join(measurements_folder, 'traceroute_results.json')
broadcast_file_path = os.path.join(measurements_folder, 'broadcast_results.json')
query_file_path = os.path.join(measurements_folder, 'query_results.json')
user_selected_file_path = None

# Define your neural network
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
train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)

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

# Function to load IPs from a file
def load_ip_file():
    global ips_dict
    global user_selected_file_path
    
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    user_selected_file_path = file_path
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

# Function to scan ports
def scan_ports(ip, ports=[80, 443, 22, 21, 25, 8080]):
    open_ports = []

    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            result = sock.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)

    # Save results to JSON file
    save_results_to_json(portscan_file_path, {"ip": ip, "open_ports": open_ports})

# Function to perform pingsweep
def pingsweep(ip):
    pingsweep_results = []
    icmp_request = IP(dst=ip) / ICMP()

    reply = sr1(icmp_request, timeout=1, verbose=False)

    if reply and reply.haslayer(ICMP) and reply.getlayer(ICMP).type == 0:
        pingsweep_results.append({"ip": ip, "status": "reachable"})
    else:
        pingsweep_results.append({"ip": ip, "status": "unreachable"})

    # Save results to JSON file
    save_results_to_json(pingsweep_file_path, {"results": pingsweep_results})

# Function to perform traceroute
def perform_traceroute(ip):
    try:
        traceroute_results = []

        hops = sr1(IP(dst=ip, ttl=(1, 64)) / ICMP(), verbose=0, timeout=2)

        if hops:
            for i, sent_pkt in enumerate(hops.res):
                try:
                    if sent_pkt[0][1].type == 11:
                        traceroute_results.append({"ip": sent_pkt[1].src})
                except:
                    pass
        else:
            traceroute_results.append({"ip": "No response"})

    except Exception as e:
        print(f"Error saving traceroute results: {e}")

    # Append traceroute results to JSON file
    save_results_to_json(traceroute_file_path, {"results": traceroute_results})

# Function to send heartbeat
def send_heartbeat(ip):
    handshake_methods = {
        "TCP": [80, 443, 25, 110, 143, 22, 21, 389, 636, 23, 3389, 5900],
        "UDP": [53, 161, 162, 123, 514],
    }

    global_ip = get_global_ip()

    handshake_results = []

    for method_name, ports in handshake_methods.items():
        for port in ports:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as handshake_socket:
                    handshake_socket.settimeout(1)
                    result = handshake_socket.connect_ex((ip, port))
                    if result == 0:
                        handshake_socket.sendall(global_ip.encode())
                        handshake_results.append({
                            "ip": ip,
                            "method": method_name,
                            "port": port,
                            "status": "Success"
                        })
                        print(f"Heartbeat sent to {ip} using {method_name} ({port})")
                    else:
                        handshake_results.append({
                            "ip": ip,
                            "method": method_name,
                            "port": port,
                            "status": "Failed: Connection                        refused"
                        })
                        print(f"Failed to send heartbeat to {ip} using {method_name} ({port}): Connection refused")
            except Exception as e:
                handshake_results.append({
                    "ip": ip,
                    "method": method_name,
                    "port": port,
                    "status": f"Failed: {str(e)}"
                })
                print(f"Failed to send heartbeat to {ip} using {method_name} ({port}): {str(e)}")

    # Save handshake results to JSON file
    save_results_to_json(handshake_file_path, handshake_results)

# Function to broadcast IP address
def broadcast_ip():
    broadcast_results = []

    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        global_ip = get_global_ip()
        
        handshake_methods = {
            "TCP": [80, 443, 25, 110, 143, 22, 21, 389, 636, 23, 3389, 5900],
            "UDP": [53, 161, 162, 123, 514],
        }
        
        for protocol, ports in handshake_methods.items():
            for port in ports:
                try:
                    if protocol == 'UDP':
                        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                    elif protocol == 'TCP':
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.bind(('', 0))
                    
                    broadcast_message = f"My IP address is {ip_address} on port {port} using {protocol} protocol"
                    sock.sendto(broadcast_message.encode(), (global_ip, port))
                    sock.close()
                    
                    broadcast_results.append({
                        "ip": ip_address,
                        "port": port,
                        "protocol": protocol,
                        "status": "Success"
                    })
                    print(f"Broadcasted IP address successfully on port {port} using {protocol} protocol")
                except Exception as e:
                    print(f"Failed to broadcast IP address on port {port} using {protocol} protocol: {str(e)}")
                    broadcast_results.append({
                        "ip": ip_address,
                        "port": port,
                        "protocol": protocol,
                        "status": f"Failed: {str(e)}"
                    })
        
    except Exception as e:
        print(f"Error broadcasting IP address: {e}")
        
    save_results_to_json(broadcast_file_path, broadcast_results)

# Function to query IP address
def query_ip():
    query_results = []

    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        
        query_ports = {
            "TCP": [80, 443, 25, 110, 143, 22, 21, 389, 636, 23, 3389, 5900],
            "UDP": [53, 161, 162, 123, 514],
        }
        
        for protocol, ports in query_ports.items():
            for port in ports:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    result = sock.connect_ex((ip_address, port))
                    
                    if result == 0:
                        print(f"Connection established to {ip_address} on port {port} using {protocol} protocol")
                        query_results.append({
                            "ip": ip_address,
                            "port": port,
                            "protocol": protocol,
                            "status": "Success"
                        })
                    else:
                        print(f"Failed to connect to {ip_address} on port {port} using {protocol} protocol: Connection refused")
                        query_results.append({
                            "ip": ip_address,
                            "port": port,
                            "protocol": protocol,
                            "status": "Failed: Connection refused"
                        })
                    
                    sock.close()
                    
                except Exception as e:
                    print(f"Failed to connect to {ip_address} on port {port} using {protocol} protocol: {str(e)}")
                    query_results.append({
                        "ip": ip_address,
                        "port": port,
                        "protocol": protocol,
                        "status": f"Failed: {str(e)}"
                    })
        
    except Exception as e:
        print(f"Error querying IP address: {e}")
        
    save_results_to_json(query_file_path, query_results)

# Function to save results to JSON file
def save_results_to_json(file_path, data):
    try:
        with open(file_path, 'a') as f:
            json.dump(data, f, indent=4)
            f.write('\n')
    except Exception as e:
        print(f"Error saving results to {file_path}: {e}")

# Function to get global IP address
def get_global_ip():
    try:
        response = requests.get("https://api.ipify.org?format=text")
        return response.text.strip()
    except Exception as e:
        print(f"Error getting global IP: {e}")
        return "127.0.0.1"

# Main function to distribute and coordinate tasks
def distribute_tasks():
    global ips_dict
    tasks = []

    for file_path, ips in ips_dict.items():
        for ip in ips:
            tasks.append(perform_traceroute)
            tasks.append(pingsweep)
            tasks.append(scan_ports)
            tasks.append(send_heartbeat)
            tasks.append(query_ip)
            tasks.append(broadcast_ip)

    # Put tasks into the queue
    for task in tasks:
        task_queue.put(task)

    # Start GPU worker
    gpu_process = mp.Process(target=gpu_worker, args=(task_queue, result_queue))
    gpu_process.start()
    gpu_process.join()

    # Retrieve and print results
    results = []
    while not result_queue.empty():
        results.append(result_queue.get())
    print("Results:")
    for result in results:
        print(result)

# GPU worker function
def gpu_worker(task_queue, result_queue):
    while True:
        try:
            task = task_queue.get(timeout=1)
            if task is None:
                break  # If None is received, it indicates the end of tasks
            result = task()  # Execute the task
            result_queue.put(result)
        except queue.Empty:
            continue  # If the queue is empty, continue waiting for tasks
        except Exception as e:
            result_queue.put(f"Exception: {e}")

# Function to initiate GPU tasks
def initiate_gpu_tasks():
    distribute_tasks()

# GUI setup
root = Tk()
root.title("Network Map")

# Label to display CPU/GPU usage
device_label_text = "Using GPU" if use_cuda else "Using CPU"
device_label = Label(root, text=device_label_text)
device_label.grid(row=5, columnspan=2)

# Text widget to display processes
processes_text = Text(root, height=20, width=50)
processes_text.grid(row=6, columnspan=2)

# Button to load IPs from file
load_file_button = Button(root, text="Load IPs from File", command=load_ip_file)
load_file_button.grid(row=3, columnspan=2)

# Listbox to display loaded files
loaded_files_label = Label(root, text="Files Loaded:")
loaded_files_label.grid(row=4, column=0)
loaded_files_box = Listbox(root, width=40)
loaded_files_box.grid(row=4, column=1)

# Button to start tasks
start_tasks_button = Button(root, text="Start", command=initiate_gpu_tasks)
start_tasks_button.grid(row=22, columnspan=2)

root.mainloop()


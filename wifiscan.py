import subprocess
from datetime import datetime

def scan_and_log():
    # Get current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Perform WiFi scan using netsh command on Windows
    try:
        output = subprocess.check_output(['netsh', 'wlan', 'show', 'network', 'mode=Bssid'])
        output = output.decode('utf-8').split('\n')
        
        # Log the scan details into a text file
        with open('wifi_scan_log.txt', 'a') as log_file:
            log_file.write(f"Scan Time: {timestamp}\n")
            log_file.write("---------------------------------------------------\n")
            for line in output:
                if "SSID" in line:
                    ssid = line.split(":")[1].strip()
                    log_file.write(f"SSID: {ssid}\n")
                elif "BSSID" in line:
                    bssid = line.split(":")[1].strip()
                    log_file.write(f"BSSID: {bssid}\n")
                elif "Signal" in line:
                    signal = line.split(":")[1].strip()
                    log_file.write(f"Signal Strength: {signal}\n")
                elif "Channel" in line:
                    channel = line.split(":")[1].strip()
                    log_file.write(f"Channel: {channel}\n")
                elif "Authentication" in line:
                    auth = line.split(":")[1].strip()
                    log_file.write(f"Authentication: {auth}\n")
                elif "Encryption" in line:
                    encryption = line.split(":")[1].strip()
                    log_file.write(f"Encryption: {encryption}\n")
                    log_file.write("---------------------------------------------------\n")
            log_file.write("\n")
    except subprocess.CalledProcessError:
        print("Error occurred while scanning WiFi networks.")

if __name__ == "__main__":
    scan_and_log()

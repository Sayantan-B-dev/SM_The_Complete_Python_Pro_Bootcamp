# Automate Your Lights When Phone Is Within Home Radius

## Project Overview
Automatically turns on your smart lights when your phone connects to your home Wi-Fi network, and turns them off when you leave.

## How It Works
- Periodically pings your phone's IP address to check network presence
- Detects when phone connects/disconnects from home network
- Sends API calls to smart lights (Philips Hue, TP-Link Kasa, etc.)
- Automates lighting based on your presence

## Files
- main.py: Main automation script
- config.py: Network and light configuration
- requirements.txt: Python dependencies
- README.md: Setup instructions

## Setup Instructions
1. Install requirements: pip install -r requirements.txt
2. Configure your phone's IP and light API in config.py
3. Set static IP for phone via DHCP reservation
4. Run main.py as a background service

## Features
- Presence detection via ping/ARP scanning
- Multi-brand smart light support
- Configurable check intervals
- Manual override options

## Challenges Addressed
- Dynamic IP changes (solved via DHCP reservation)
- Ping blocking on phones
- Different smart light APIs
- False triggers from brief disconnections

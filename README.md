# PyPot
Modular honeypot designed in Python to track exploitation attempts and scanning

# Project Goal
Having run an AWS instance for a couple of years I have watched a lot of traffic heading towards my servers.
To better understand the attacks targeting my servers, I decided to create a honeypot to track and log all traffic.

# Usage
To run just enter: "sudo python honeypot.py"
Honeypot will run in the background and save all logged information into the SQLITE3 Database db.db

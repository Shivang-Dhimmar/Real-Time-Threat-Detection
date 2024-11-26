
# Real-Time Malware Detection Software

## Project Overview
This repository manages the source code of Software Lab Project aimed at detecting security threats to the system at runtime.

## Procedure

1. **System State Monitoring**
   - Utilize Linux kernel metadata to assess the current state of system resources.

2. **Malicious Files Identification**
   - Detect files that match malwares signatures.
   - Provide users with a list of identified malicious files.

4. **Real-Time Resource Utilization**
   - Generate real-time plots of system resource utilization.
   - Monitor key metrics to visualize system performance

## Features
- Real-time monitoring of system resources.
- Detection and analysis of potentially malicious files.
- User notification of identified malicious files.
- Visual representation of system metrics for better insight.

## Installation Guide
1. **Install ClamAV Daemon And Signature Database**
   - sudo apt install clamav
   - sudo apt install clamav-daemon
   - sudo apt install clamav-freshclam
   - sudo freshclam

2. **Enable clamav-daemon.service If Not Yet**
   - sudo systemctl enable clamav-daemon.service

3. **Add permission to clamav-daemon using linux user groups**
   - sudo usermod -aG <user_name> clamav
   - sudo usermod -aG clamav  <user_name>

4. **Install Dependenies for python**
   - pip install pip pyClamd
   - pip install PyQt5


# Recon Automation Tool
This is a simple Python-based automation script for basic bug bounty reconnaissance.  
It helps in gathering subdomains, checking live hosts, running permutations, scanning vulnerabilities, and doing basic port scanning.

## What it does
- Finds subdomains using Subfinder  
- Checks live domains using HTTPX  
- Generates permutations using AlterX  
- Runs vulnerability scan using Nuclei  
- Performs port scan using Nmap  
- Generates a simple final report  

## Requirements
Make sure you have these tools installed:
- subfinder  
- httpx  
- alterx  
- nuclei  
- nmap  
Also, Python 3 is required.

## How to run
bash:
python3 recon.py example.com

Replace example.com with your target domain.

## Output
All results are saved in a folder like:

recon_example.com_YYYYMMDD_HHMMSS

Inside it you will find:

- subdomains.txt
- live_hosts.txt
- permutations.txt
- perm_live_hosts.txt
- nuclei_results.txt
- nmap_results.txt
- REPORT file


## Note
This tool is made for learning and bug bounty practice.
Always make sure you have permission before testing any target.

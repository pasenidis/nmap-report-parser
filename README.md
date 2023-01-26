# nmap-report-parser

by Edward Pasenidis

## Purpose
> Context: SSH users granted to external engineers are usually lacking `write` permission so you cannot output XML on Nmap

Quickly generating reports from classic Nmap output. No dependencies.

## How to use
1. Put your output into a file
2. Run the script, no dependencies required
```py
python3 main.py -f report.txt
```

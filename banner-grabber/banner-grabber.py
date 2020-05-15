import socket,sys,argparse,multiprocessing,subprocess,time
from datetime import datetime

def scan(ip,port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        res = s.connect_ex((ip,port))
        if res == 0:
            if port == 80:
                rsp = "HEAD / HTTP/1.1\r\nhost: " + ip + "\r\n\r\n"
                s.send(rsp.encode())
            banner = s.recv(4096)
            msg = "Port " + str(port) + " is open\n"
            msg += "-----------------------------\n" + banner.strip().decode()
            print(msg + "\n-------------------------\n")
        s.close()
    except socket.timeout:
        banner = "No banner msg"
        if port == 53:
            banner = subprocess.getoutput("nslookup -type=any -class=chaos version.bind "+ip)
        msg = "Port " + str(port) + " is open\n"
        msg += "-----------------------------\n" + banner.strip()
        print(msg + "\n-------------------------\n")
        s.close()

def main(args):
    try:
        start = datetime.now()
        print ("==================================================")
        print ("Scanning " + args.ip + " Ports: " + str(args.sport) + " - " + str(args.eport))
        print ("==================================================\n")

        for port in range(args.sport,args.eport):
            p =multiprocessing.Process(target = scan, args=(args.ip,port))
            p.start()
            time.sleep(args.throttle)
        time.sleep(3)

        stop = datetime.now()
        print ("==================================================")
        print ("Scan Duration: " + str(stop - start))
        print ("==================================================")
    except Exception as err:
        print("Error", err)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("ip", action="store", type=str, help="Host name")
    parser.add_argument("sport", action="store", type=int, nargs="?", default=1,
    const =1,help = "Starting port range")
    parser.add_argument("eport", action="store", type=int, nargs="?", default=1023,
    const = 1023, help = "Ending port range")
    parser.add_argument("-t","--throttle", action="store",type = float, nargs="?",
    default=0.25, const=0.25, help="Time interval")

    if len(sys.argv[1:]) == 0:
        parser.print_help()
        parser.exit()

    args = parser.parse_args()
    main(args)
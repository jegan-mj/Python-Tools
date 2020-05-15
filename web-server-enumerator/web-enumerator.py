import sys, argparse, multiprocessing, requests, time
from datetime import datetime

def request(url):
    try:
        agent = {
            "User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36")
        }
        rsp =requests.get(url)
        print(rsp,url)
        if rsp.status_code != 404:
            print("[+] Status " + str(rsp.status_code) + ": " + url)
    except Exception as err:
        print(err)

def scan(url,word,ext):
    turl = "http://" + url + word.rstrip()
    print("turl",turl)
    request(turl)
    if ext:
        request(turl+ext)

def main(args):
    start = datetime.now()
    print ("==================================================")
    print ("Started @ " + str(start))
    print ("==================================================")
    url = args.url
    if url.endswith("/") == False: url += "/"
    with open(args.wordlist) as fle:
        for word in fle:
            if word.startswith("#") == False:
                p = multiprocessing.Process(target = scan, args = (url,word,args.extension))
                p.start()
            time.sleep(2)
    stop = datetime.now()
    print ("==================================================")
    print ("Scan Duration: " + str(stop - start))
    print ("Completed @ " + str(stop))
    print ("==================================================")   

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("url", action="store", help="starting url")
    parser.add_argument("wordlist", action="store", help="list of paths/files")
    parser.add_argument("-e", "--extension", action="store", help="file extension")

    if len(sys.argv[2:]) == 0:
        parser.print_help() 
        parser.exit()

    args = parser.parse_args()
    main(args)
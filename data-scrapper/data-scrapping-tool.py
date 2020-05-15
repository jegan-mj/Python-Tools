import argparse, requests, re, sys

class RegEx:
    def __init__(self,pattern,desc):
        self.pattern = pattern
        self.desc = desc

regEmail = RegEx(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", "Emails")
regPhone = RegEx(r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b", "Phone Numbers")
regIP = RegEx(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", "IP Addresses")
regWord = RegEx(r"[a-zA-Z]+", "Words")

def scrapeURL(url,reg):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
        src = requests.get(url.strip(),headers=headers)
        print(src)
        for rg in reg:
            print("Scrapping " + rg.desc + " from " + url + ": \n")
            res = set(re.findall(rg.pattern,src.text, re.I))
            for data in res:
                print(data)
        
    except Exception as err:
        print(err)
    
def scrapeFile(fle,reg):
    try:
        with open(fle) as f:
            for url in f:
                scrapeURL(url,reg)

    except Exception as err:
        print(err)

def main(args):

    reg = []
    isFile = True

    if args.input.lower().startswith("http"):
        isFile = False

    if args.scrape.lower() == "e":
        reg = [regEmail]
    elif args.scrape.lower() == "p":
        reg = [regPhone]
    elif args.scrape.lower() == "ip":
        reg = [regIP]
    elif args.scrape.lower() == "a":
        reg = [regEmail, regPhone, regIP, regWord]
    elif args.scrape.lower() == "w":
        reg = [regWord]


    if(isFile):
        scrapeFile(args.input,reg)
    else:
        scrapeURL(args.input,reg)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("input", action = "store", type = str, help = "Enter the URL or file path")
    parser.add_argument("scrape", action="store", type = str, nargs="?", default="a", help="e from emails; p for phone numbers; i for ip address; w for words; a for all")

    if len(sys.argv[2:])==0:
        parser.print_help()
        parser.exit()

    args = parser.parse_args()
    main(args)
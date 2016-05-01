#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
from datetime import datetime


def parse_txs():
    print("Get transactions ids...")
    accounts = {"0xd079c22e9c63341bf839a8634e8892c430d724cf",
                "0xae506bb28ed79b29c6968ab527d1efdc5f399331"}
    txs = set()
    page = 0
    stop = False
    with open("txs.txt", "r") as f:
        old_txs = set(map(lambda x: x.strip(), f.readlines()))
    while 1:
        print("page: {}".format(page))
        r = requests.get('https://etherscan.io/txs?a=0xAE506bb28Ed79b29c6968Ab527d1eFdc5f399331&p={}'.format(page))
        soup = BeautifulSoup(r.text, 'lxml')
        addrs = soup.find_all("span", {"class": "address-tag"})
        if len(addrs) == 0:
            break
        for addr in addrs:
            if addr.text in accounts:
                continue
            if addr.text in old_txs:
                stop = True
                break
            txs.add(addr.text)
        if stop:
            break
        page += 1
    print("Get {} new transactions ids".format(len(txs)))
    with open("txs.txt", "a") as f:
        [f.write(tx + "\n") for tx in txs]
    with open("data.txt", "a") as f:
        for i, tx in enumerate(txs):
            print(i)
            tx = tx.strip()
            r = requests.get('https://etherscan.io/tx/{}'.format(tx))
            soup = BeautifulSoup(r.text, 'lxml')
            data = soup.find("textarea", {"class": "form-control"})
            f.write(data.text + "\n") if data is not None else print(tx)
    print("Get transactions data... OK")


def parse_data():
    print("Get variables from data...")
    with open("data.txt", "r") as f:
        s = f.readlines()
        print(len(s))
    with open("transactions.txt", "w") as f:
        for tx in s:
            tx = tx.strip()[10:]
            txid = tx[:32]
            am = tx[64:128]
            time = tx[129:]
            f.write("{} {} {}\n".format(txid, int("0x" + am, 0) / 10 ** 8, datetime.fromtimestamp(int("0x" + time, 0))))
    print("Get variables from data... OK")


def sort_data():
    with open("transactions.txt", "r") as f:
        s = f.readlines()
    s = list(map(lambda x: x.split(), s))
    s = sorted(s, key=lambda x: (x[2], x[3]))
    with open("info.txt", "w") as f:
        [f.write(x[0] + 4 * " " + x[1] + (14 - len(x[1])) * " " + x[2] + (14 - len(x[2])) * " " + \
                 x[3] + "\n") for x in s]


def sort_by_amount():
    with open("transactions.txt", "r") as f:
        s = f.readlines()
    s = list(map(lambda x: x.split(), s))
    s = sorted(s, key=lambda x: float(x[1]), reverse=True)
    with open("top.txt", "w") as f:
        [f.write(x[0] + 4 * " " + x[1] + (14 - len(x[1])) * " " + x[2] + (14 - len(x[2])) * " " + \
                 x[3] + "\n") for x in s[:10]]
        f.write(str(sum([float(x[1]) for x in s[10:]])))


def group_by_day():
    with open("transactions.txt", "r") as f:
        s = f.readlines()
    s = list(map(lambda x: x.split(), s))
    s = sorted(s, key=lambda x: (x[2], x[3]))
    days_info = []
    cur_date = s[0][2]
    day_tx = []
    for tx in s:
        if tx[2] == cur_date:
            day_tx.append(tx)
        else:
            days_info.append(day_tx)
            cur_date = tx[2]
            day_tx = []
    days_info.append(day_tx)
    with open("info_by_day.txt", "w") as f:
        f.write("Date\t\t\tAmount\n")
        for x in days_info:
            f.write(x[0][2] + "\t\t" + str(sum(float(el[1]) for el in x)) + "\n")


if __name__ == "__main__":
    parse_txs()
    parse_data()
    sort_by_amount()
    group_by_day()

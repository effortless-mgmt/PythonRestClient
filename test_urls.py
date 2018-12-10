import time
import requests

def check_up(url, name):
    try:
        req = requests.get(url + "/api/user")
    except:
        print(name, "failed", sep="\t")
        return
    
    if (req.status_code == 200):
        print(name, req.status_code, req.json(), sep="\t")
    else:
        print(name, req.status_code, sep="\t")

t1 = ("https://api.effortless.dk", "prod.ssl")
t2 = ("http://staging.effortless.dk", "stag.nossl")
t3 = ("https://staging.effortless.dk", "stag.ssl")
t4 = ("http://staging.effortless.dk:5000", "stag.5000")
tests = [t1, t2, t3, t4]

print("Testing following urls:")
for t in tests:
    print(t[1], t[0], sep="\t")

print()

def test():
    for t in tests:
        check_up(t[0], t[1])

def loop():
    while True:
        test()
        time.sleep(2)
        print("\n====================\n")

#loop()
test()


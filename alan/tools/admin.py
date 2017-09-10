# @author ksdme
# tool to act as a AlanServer Client
# and configure the moderator settings
import requests
from sys import argv

# requires the AlanServer url
host, argv = argv[-1], argv[:-1]

# if its in admin mode
if "--admin" in argv:

    print "[+] Select one of the below: "
    print "[1] Clear Session"
    print "[2] Set Login State"
    print "[3] Set Quiz State"
    print "[4] End Quiz\n"

    optn = int(raw_input("[+] Enter Selection: "))
    pawd = raw_input("[+] Enter Admin Passwd:")

    # catches all of the uri failure
    try:
        if optn == 1:
            roll = int(raw_input("[+] Session holder's Roll: "))

            reponse = requests.get(
                "http://{}/state/clear/{}?w={}".format(
                    host, roll, pawd))

            print "[+] Successful!", reponse.content, "\n"

        elif optn == 2:
            state = int(raw_input("[+] Enter State: ")) > 0

            reponse = requests.get(
                "http://{}/state/login/{}?w={}".format(
                    host, int(state), pawd))

            print "[+] Successful!", reponse.content, "\n"

        elif optn == 3:
            state = int(raw_input("[+] Enter State: ")) > 0

            reponse = requests.get(
                "http://{}/state/quiz/{}?w={}".format(
                    host, int(state), pawd))

            print "[+] Successful!", reponse.content, "\n"

        elif optn == 4:
            reponse = requests.get(
                "http://{}/quiz/end?w={}".format(host, pawd))

            print "[+] Successful!", reponse.content, "\n"
    
    except requests.ConnectionError:
        print "usage: admin.py <command> <AlanServer host:port>"

#Made by Cristian Di Bartolomeo
#Only scan with permission!
#------------------------------

#Imports
import socket
import os

#Text art: Speed - patorjk.com
print('''
________________     _____________       ______         
___  __ \__  __ \    ___    |__  /__________  /_______ _
__  /_/ /_  /_/ /    __  /| |_  /___  __ \_  __ \  __ `/
_  ____/_  _, _/     _  ___ |  / __  /_/ /  / / / /_/ / 
/_/     /_/ |_|______/_/  |_/_/  _  .___//_/ /_/\__,_/  
              _/_____/           /_/                    
''')

#Methods
#Testing IP
def TryError(ip, port):
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.settimeout(2)
    try:
        soc.connect_ex((ip, port))
    except socket.gaierror:
        print("GaiError exception raised.")
        return 1
    return 0

#Ping Sweep
def PingSweep(ip):
    upHost = []
    for x in range(1, 256):
        resp = os.system("ping -c 1 " +ip+"."+str(x) +" | find \"TTL=\"")
        if resp == 0:
            print(ip+"."+str(x)+" is up.")
            upHost.append(ip+"."+str(x)+" is up.")
    return upHost

#Loop
while True:
        #File Checking
        rInt = 0
        check = True
        while check == True:
                if os.path.isfile("results"+str(rInt)+".txt"):
                        rInt += 1
                else:
                        data = open("results"+str(rInt)+".txt", "w")
                        check = False

        opt = -1

        #Mode Selection
        while True:
                print("Which mode would you like to select?\n1 - Port Specific\n2 - Port Range\n3 - Ping Sweep")
                try:
                    opt = int(input())
                except ValueError:
                    print("ValueError excepted. Integer expected.")
                if opt == 1 or opt == 2:
                    break
        #Option 3
                elif opt == 3:
                    pingIP = input("Please insert the first three IP digits. ie: 192.168.2\n")
                    upHost = []
                    upHost = PingSweep(pingIP)
                    leng = len(upHost)
                    for x in range(0, leng):
                        data.write(upHost[x]+"\n")
                    data.close()
                else:
                    print("Please use a valid input.")

        #Option 1
        if opt == 1:
                port = 0
                portlist = []
                ip = input("Enter IP: ")
                print("Input any number < 1 or > 65535 to end the loop.")
                while True:
                        port = int(input("Enter a port: "))
                        if port < 1 or port > 65535:
                                break
                        else:
                                portlist.append(port)
                portlist.sort()
                con = int(input("Enable closed port message? Y - 1, N - 2: "))

                #Scan Loop
                leng = len(portlist)
                x = 0
                data.write("Portrange Port Scanner by Cristian Di Bartolomeo {RESULTS}\n")
                data.write("Analysis for: " +ip+ " at ports: |")
                while True:
                        if(x >= leng):
                                break
                        else:
                                data.write(" "+str(portlist[x])+" |")
                        x += 1
                data.write("\n\n")
                y = 0
                error = TryError(ip, portlist[0])
                if error == 1:
                    data.write("!==GAIERROR EXCEPTION RAISED==!")
                    data.close()
                    break
                while True:
                        if(y < leng):
                                soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                soc.settimeout(2)
                                if soc.connect_ex((ip, portlist[y])):
                                        if con == 1:
                                                print("Port ", str(portlist[y]), " is closed.")
                                                data.write("Port " +str(portlist[y])+ " is closed.\n")
                                else:
                                        print("Port ", str(portlist[y]), " is open.")
                                        data.write("Port " +str(portlist[y])+ " is open.\n")
                                        soc.shutdown(socket.SHUT_RDWR)
                                        soc.close()
                                y += 1
                        else:
                                break
        
        #Option 2
        if opt == 2:
                ip = input("Enter IP: ")
                i1 = input("Enter the port to start at: ")
                i2 = input("Enter the port to end at: ")
                con = int(input("Enable Closed port message? Y - 1, N - 2: "))
                val = int(i1)

                #Scan Loop
                data.write("Portrange Port Scanner by Cristian Di Bartolomeo {RESULTS}\n")
                data.write("Analysis for: " +ip+ " at ports " +i1+ " - " +i2+ "\n\n")
                error = TryError(ip, int(i1))
                if error == 1:
                    data.write("!==GAIERROR EXCEPTION RAISED==!")
                    data.close()
                    break
                for num in range(int(i1), int(i2)+1):
                        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        soc.settimeout(2)
                        if soc.connect_ex((ip, val)):
                                if con == 1:
                                        print ("Port ", str(val), " is closed.")
                                        data.write("Port " + str(val) + " is closed.\n")
                        else:
                                print ("Port ", str(val), " is open.")
                                data.write("Port " + str(val) + " is open.\n")
                                soc.shutdown(socket.SHUT_RDWR)
                                soc.close()
                        val += 1
        data.close()
        while True:
                print("Would you like to run Portrange again?\nY/N ")
                cho = str(input())
                if cho == "Y" or cho == "y":
                        print("\nRestarting...\n")
                        break
                elif cho == "N" or cho == "n":
                        break
                else:
                    print("Please use a valid input.")
        if cho == "N" or cho == "n":
                break

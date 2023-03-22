from flask import Flask, render_template, jsonify, request
import ipPublique
import ping3
from netscan import scan_hosts
import subprocess
from speedtest import download_upload_speed
from localip import *
import requests
import random
import os
import json
import threading
import time
from typing import Union

VERSION = "1.0.0"
LOCALIP = get_ip_address("wlan0")

class Semabox_config:
    name: str
    version: str
    ip: str

    def __init__(self):
        self.Load()                                                             # on charge les données (si elles existent, sinon on les crée)

    def Save(self):
        with open("semaboxe-data.json", "w") as f:
            json.dump(self.ToDict(), f)                                         # on sauvegarde les données
        
    def Load(self):
        if not os.path.exists("semaboxe-data.json"):                            # si le fichier n'existe pas on le crée
            self.name = "Semaboxe-" + str(random.randint(0, 1000))                  # on génère un nom aléatoire
            self.version = VERSION                                                  # on met la version actuelle
            self.ip = LOCALIP                                                  # on met l'ip par défaut
            self.Save()                                                             # on crée un nouveau fichier avec les valeurs par défaut
        with open("semaboxe-data.json", "r") as f:                              # on ouvre le fichier
            data = json.load(f)                                                 # on charge les données
        
        self.name = data["name"]                                                # on charge le nom
        self.version = data["version"]                                          # on charge la version
        self.ip = data["ip"]                                                    # on charge l'ip


    def ToDict(self) -> dict:
        return {
            "name": self.name,
            "version": self.version,
            "ip": self.ip
        }
    

semabox_config: Semabox_config = Semabox_config()                               # on crée une instance de la classe Semabox_config

global speedTestHistory
speedTestHistory: list = []                                                     # dictionaire stockant les 5 dernières valeurs débit montant et descendant



#r = requests.post('http://semalynx.local:5000/api/manage-semabox/add', json=semabox_config.ToDict())  
hostname = "1.1.1.1"
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', ipPublique=ipPublique.public_ip , hostname=hostname)


@app.route('/ping', methods=['GET'])
def ping():
    try:
        latency = round(ping3.ping(hostname, unit='ms'),2)
        return jsonify(latency)
    except Exception as e:
        return str(e)

@app.route('/netmap', methods=['GET'])
def netmap():
    try:
        netmap = scan_hosts(get_net_cidr("wlan0"))
    except Exception as e:
        print("error :",e)
        netmap = []
    return jsonify(netmap)

# @app.route('/netmap', methods=['GET'])
# def netmap():
#     try:
#         nm = nmap.PortScanner()
#         netmap = {}
#         nm.scan(hosts='192.168.1.0/24', arguments='-sS -T4 -p1-100')
#         for host in nm.all_hosts():
#             netmap[host] = nm[host]['tcp']
#         return jsonify(netmap)
#     except Exception as e:
#         return str(e)

@app.route('/getspeedtest', methods=['GET'])
def getspeedtest():
    try:
        return jsonify(speedTestHistory)
    except Exception as e:
        return str(e)

@app.route('/reboot', methods=['GET'])
def reboot():
    try:
        #subprocess.call(['sudo', 'reboot'])
        subprocess.call(['echo', 'pas le reboot'])
        return jsonify("reboot")
    except Exception as e:
        return str(e)

@app.route('/health', methods=['GET'])
def health():
    return jsonify('OK')



def SpeedtestLoop():
    global speedTestHistory
    while True:
        speedTestHistory.append(download_upload_speed())
        if len(speedTestHistory) > 5:
            speedTestHistory.pop(0)
        time.sleep(300)


if __name__ == '__main__':
    threading.Thread(target=SpeedtestLoop).start()
    app.run(debug=True,host='0.0.0.0', port=9999)



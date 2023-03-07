from flask import Flask, render_template, jsonify, request
import ipPublique
import ping3
import netscan
import subprocess
# dictionaire stockant les 5 dernières valeurs débit montant et descendant 
speedtest = [
    {
        "download": 150,
        "upload": 20
    },
    {
        "download": 43,
        "upload": 36
    },
    {
        "download": 152,
        "upload": 14
    },
    {
        "download": 18,
        "upload": 39
    },
    {
        "download": 45,
        "upload": 11
    }
]

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
        netmap = netscan.hosts
        return jsonify(netmap)
    except Exception as e:
        return str(e)

@app.route('/getspeedtest', methods=['GET'])
def getspeedtest():
    try:
        return jsonify(speedtest)
    except Exception as e:
        return str(e)

@app.route('/reboot', methods=['POST'])
def reboot():
    try:
        subprocess.call(['sudo', 'reboot'])
        return jsonify("reboot")
    except Exception as e:
        return str(e)
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=9999)
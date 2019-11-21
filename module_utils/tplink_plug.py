"""TP Link generic functions used by tplink_plug_* Ansible modules."""
import json
import socket
from struct import pack

def encrypt(string):
	key = 171
	result = pack('>I', len(string))
	for i in string:
		a = key ^ ord(i)
		key = a
		result += chr(a)
	return result

def decrypt(string):
	key = 171
	result = ""
	for i in string:
		a = key ^ ord(i)
		key = ord(i)
		result += chr(a)
	return result

def tplink_plug_get_metrics(ip, port):
    cmd = '{"emeter":{"get_realtime":{}}}'
    data = request(ip, port, cmd)
    return data

def tplink_plug_get_state(ip, port):
    data = tplink_plug_get_sysinfo(ip, port)
    return data['relay_state']

def tplink_plug_get_sysinfo(ip, port):
    cmd = '{"system":{"get_sysinfo":{}}}'
    data = request(ip, port, cmd)
    return data['system']['get_sysinfo']

def tplink_plug_set_state(ip, port, state):
    cmd = '{"system":{"set_relay_state":{"state":' + str(state) + '}}}'
    request(ip, port, cmd)
    
def request(ip, port, cmd):
    try:
        sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_tcp.connect(('192.168.0.7', 9999))
        sock_tcp.send(encrypt(cmd))
        data = sock_tcp.recv(2048)
        sock_tcp.close()
        return json.loads(decrypt(data[4:]))
    except socket.error:
        quit("Cound not connect to host " + ip + ":" + str(port))
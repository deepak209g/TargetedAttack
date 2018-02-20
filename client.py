import btpeer as btp
import btfiler as btf
import os
import threading
import socket
import json
import requests
import traceback


central_server = 'http://172.31.111.1:5000'
cluster_peers = list()
lock = threading.Lock()
port = 5000
#
# def get_peers():
#     host = ''  # Bind to all interfaces
#     port = 5000
#     broadcastaddr = get_broadcast_addr()
#     broadcastaddr = "172.31.255.255"
#     addr = (broadcastaddr, port)
#
#     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#     s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # broadcasr
#
#     data = 'hello from sender'
#
#     s.bind(('', port))  # socket binding to any host
#     s.sendto(data, addr)
#     s.close
#
#
# def get_broadcast_addr():
#     myip = socket.gethostbyname(socket.gethostname())
#     print 'My IP', myip
#
#     # XX: assumes /24 address
#     broadip = socket.inet_ntoa(socket.inet_aton(myip)[:2] + b'\xff\xff')
#     print 'LAN broadcast', broadip
#
#     return broadip
def setup_server(client):
    client.mainloop()


def refresh_peers_list(client, port):
    response = requests.get(central_server)
    print (json.loads(response.text)['top5'])

    for ip in json.loads(response.text)['top5']:
        peerid = str(ip) + ":" + str(port)
        if peerid not in client.getpeerids():
            client.addpeer(peerid=peerid, host=str(ip), port=port)

    client.removepeer(central_server.split('/')[-1])
    

def send_message(client, peerid, msg_json):
    one_reply = client.sendtopeer(peerid=peerid, msgtype="FPUT", msgdata=json.dumps(msg_json))
    # print (one_reply)
    msg_data = one_reply[0][1]
    tmp_cluster = json.loads(msg_data)[unicode("cluster")]
    with lock:
        for peerid in tmp_cluster:
            if peerid not in cluster_peers:
                cluster_peers.append(peerid)
                print(cluster_peers)

def message_generator(message=None):
    try:
        # print("Give file_path or Enter 'stop' to shutdown the process")
        global client

        if not message:
            filepath = raw_input()
            # if filepath == 'stop':
            #     break

            client.addlocalfile(filepath)
            message = client.files[filepath]
        # client.addlocalfile(os.path.join('client1', '1.txt'))
        msg_json = {
            'msg_data': message,
            'peerid_list': [client.myid],
            'hops': 0,
            'cluster': [client.myid]
        }
        client.addpeer(peerid="192.168.1.6:5002", host="192.168.1.6", port=5002)
        print (json.dumps(msg_json))

        if len(client.getpeerids()) <= 1:
            refresh_peers_list(client, port)

        global cluster_peers
        cluster_peers = []
        threads = list()
        for peerid in client.getpeerids():
            # client.sendtopeer(peerid=peerid, msgtype="FPUT", msgdata=json.dumps(msg_json))
            threads.append(threading.Thread(target=send_message, args=(client, peerid, msg_json,)))
            threads[-1].start()
            print ("send data to {}".format(peerid))
            # client.connectandsend(host=peerid.split(':')[0], port=peerid.split(':')[1], msgtype='FPUT',
            #                   msgdata=json.dumps(msg_json), pid=client.myid, waitreply=True)
        for thread in threads:
            thread.join()
        print("number of similar messages {0}".format(len(cluster_peers)))
    except Exception as exp:
        if client.debug == True:
            traceback.print_exc()


def main():
    # instantiate a server
    port = 5000
    global client
    client = btf.FilerPeer(10, port)
    client.debug = True

    t1 = threading.Thread(target=setup_server, args=(client, ))
    t1.start()

    refresh_peers_list(client, port)

    # get_peers()
    # stop = False
    # while stop is False:
    message_generator("Spam")

if __name__ == "__main__":
    main()
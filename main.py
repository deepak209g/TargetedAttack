import btpeer as btp
import btfiler as btf
import threading
import socket

server = btf.FilerPeer(10, 5000)
server.debug = True


# server.buildpeers('172.31.110.112', 5002)
server.mainloop()
print("after")
print socket.gethostbyname(socket.gethostname())
import numpy as np
import matplotlib.pyplot as plt
import socket

def recwall(sock,n):
    data=bytearray()
    while (len(data)<n):
        packet=sock.recv(n-len(data))
        if not packet:
            return
        data.extend(packet)
    return data

def neigbours4(y,x):
    return (y,x-1),(y-1,x),(y,x+1),(y+1,x)

def neigboursX(y,x):
    return (y-1,x-1),(y-1,x+1),(y+1,x-1),(y+1,x+1)

def neigbours8(y,x):
    return neigbours4(y,x) + neigboursX(y,x)

def w(arr,y,x):
    for i in neigbours8(y,x):
        if arr[i[0],i[1]]>=arr[y,x]:
            return False
    return True

def serch(arr):
    l=[]
    for y in range(1,arr.shape[0]-1):
        for x in range(1,arr.shape[1]-1):
            if w(arr,y,x):
                l.append((y,x))
    return(l)


host='84.237.21.36'    
port=5152

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((host,port))
    for _ in range(10):
        sock.send(b'get')
        bts=recwall(sock,40002)

        img=np.frombuffer(bts[2:],dtype='uint8').reshape(bts[0],bts[1])
        pos=serch(img)
        pos1=np.array(pos[0])
        pos2=np.array(pos[1])

        res=round(((pos1[0]-pos2[0])**2+(pos1[1]-pos2[1])**2)**0.5,1)
        sock.send(f'{res}'.encode())
        print(sock.recv(20))

        sock.send(b'beat')
        beat=sock.recv(20)
        print(beat)
        print()


        # plt.subplot(121)
        # plt.imshow(img)
        # plt.show()
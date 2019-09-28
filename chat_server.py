import socket
import threading


def client_chat(sock_conn):
    try:
        while True:
            msg_len = sock_conn.recv(15)
            if not msg_len:
                break

            msg_len = int(msg_len.decode().rstrip())
            recv_size = 0
            msg_data = b""
            while recv_size < msg_len:
                tmp = msg_data = sock_conn.recv(msg_len - recv_size)
                if not tmp:
                    break
                msg_data += tmp
                recv_size += len(tmp)
            else:
                #发送给其他所有在线的客户端
                for sock_tmp, tmp_addr in client_socks:
                    if sock_tmp is not sock_conn:
                        try:
                            sock_tmp.send(msg_len)
                            sock_tmp.send(msg_data)
                        except:
                            client_socks.remove((sock_tmp, tmp_addr)) 
                            sock_tmp.close()             
                continue
            break

    finally:
        client_socks.remove((sock_conn, client_addr))
        sock_conn.close()


sock = socket.socket()
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("0.0.0.0", 9999))
sock.listen(5)

client_socks = []

while True:
    sock_conn, client_addr = sock.accept()
    client_socks.append((sock_conn, client_addr))
    threading.Thread(target=client_chat, args=(sock_conn, )).start()







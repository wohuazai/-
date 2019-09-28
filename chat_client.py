import tkinter as tk
import socket, threading
import tkinter.messagebox


def on_send_msg():
    ni_name = "上帝"
    chat_msg = chat_msg_box.get(1.0, "end")
    if chat_msg == "\n":
        return

    chat_data = ni_name + ":" + chat_msg
    chat_data = chat_data.encode()
    data_len = "{:<15}".format(len(chat_data)).encode()
    try:
        sock.send(data_len + chat_data)
    except:
        # sock.close()
        tk.messagebox.showerror("发送消息失败，请检查区网络连接！ ")
    else:
        chat_msg_box.delete(1.0, "end")
        chat_record_box.configure(state=tk.NORMAL)
        chat_record_box.insert("end", chat_data.decode() + "\n")
        chat_record_box.configure(state=tk.DISABLED)

        
def recv_chat_msg():
    global sock

    while True:
        try:
            while True:
                msg_len = sock.recv(15)
                if not msg_len:
                    break

                msg_len = int(msg_len.decode().rstrip())
                recv_size = 0
                msg_data = b""
                while recv_size < msg_len:
                    tmp = msg_data = sock.recv(msg_len - recv_size)
                    if not tmp:
                        break
                    msg_data += tmp
                    recv_size += len(tmp)
                else:
                    chat_msg_box.delete(1.0, "end")
                    chat_record_box.configure(state=tk.NORMAL)
                    chat_record_box.insert("end", chat_data.decode() + "\n")
                    chat_record_box.configure(state=tk.DISABLED)
                                
                    continue
                break

        finally:
            sock.close()
            sock = socket.socket()
            sock.connect(("itmojun.com",9999))
    


sock = socket.socket()
sock.connect(("itmojun.com",9999))


tki = tk.Tk()

tki.title("P1901班专属聊天室")
tki.minsize(600, 500)

chat_record_box = tk.Text(tki)
chat_record_box.configure(state=tk.DISABLED)
chat_record_box.pack(padx=10, pady=10)

chat_msg_box = tk.Text(tki)
chat_msg_box.configure(width=60, height=5)
chat_msg_box.pack(side=tk.LEFT,padx=10, pady=5)

chat_msg_bin = tk.Button(tki, text="发 送", command=on_send_msg)
chat_msg_bin.pack(side=tk.RIGHT, padx=10, pady=10, ipadx=15,ipady=15)

threading.Thread(target=recv_chat_msg).start()

tki.mainloop()

sock.close()


import socket
import threading
import customtkinter, tkinter.scrolledtext

host = socket.gethostbyname(socket.gethostname())
port = 5050


class Client:
    def __init__(self, host, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))

        msg = customtkinter.CTk()

        msg.withdraw()

        self.nickname = customtkinter.CTkInputDialog( title="Join", text="Enter a Nickname:").get_input()

        self.gui_done = False
        self.running = True

        gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)

        gui_thread.start()
        receive_thread.start()

    def gui_loop(self):
        self.window = customtkinter.CTk()
        self.window.configure(padx=50, pady=50, background="gray")

        self.chat_label = customtkinter.CTkLabel(master=self.window, text="Chat", bg_color="gray")
        self.chat_label.configure(text_font=("Arial", 12))
        self.chat_label.pack(padx=20, pady=10)

        self.text_area = tkinter.scrolledtext.ScrolledText(master=self.window)
        self.text_area.pack(padx=20, pady=10)
        self.text_area.config(state="disabled")

        self.message_label = customtkinter.CTkLabel(master=self.window, text="Message", bg_color="gray")
        self.message_label.configure(text_font=("Arial", 12))
        self.message_label.pack(padx=20, pady=10)

        self.input_area = tkinter.Text(master=self.window, height=3)
        self.input_area.pack(padx=20, pady=10)

        self.send_button = customtkinter.CTkButton(master=self.window, text="Send", command=self.write)
        self.send_button.pack(padx=20, pady=10)

        self.gui_done = True
        self.window.protocol("WM_DELETE_WINDOW", self.stop)
        self.window.mainloop()

    def receive(self):

        while self.running:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if message == "NICK":
                    self.client.send(self.nickname.encode('utf-8'))
                else:
                    if self.gui_done:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end', message)
                        self.text_area.yview('end')
                        self.text_area.config(state='disable')
            except ConnectionAbortedError:
                break
            except:

                print("Error")
                self.client.close()
                break

    def write(self):
        message = f"{self.nickname}: {self.input_area.get('1.0', 'end')}\n"
        self.client.send(message.encode('utf-8'))
        self.input_area.delete('1.0', 'end')

    def stop(self):
        self.running = False
        self.window.destroy()
        self.client.close()
        exit(0)


client = Client(host=host, port=port)

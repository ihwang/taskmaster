import socket
import sys
import yaml

utf = "utf-8"

def run_client(host='127.0.0.1', port=7788):
    with socket.socket() as sock:
        sock.connect((host, port))
        with open(sys.argv[1], "rt") as stream:
            raw_yaml = yaml.safe_load(stream)

        data = yaml.dump(raw_yaml)
        print(data)
        sock.sendall(data.encode(utf))

        res = sock.recv(1024)
        data = res.decode()
        print(data)
        

     #   print(data["program"])

if __name__ == '__main__':
    run_client()
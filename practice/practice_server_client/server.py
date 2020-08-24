import socket
import yaml

utf = "utf-8"

def run_server(host='127.0.0.1', port=7788):
    BUF_SIZE = 1024
    with socket.socket() as sock:
        sock.bind((host, port))
        sock.listen()
        conn, addr = sock.accept()
        data = conn.recv(BUF_SIZE)
        print(data)

        print(data.decode(utf))
        conn.sendall(data)

        data = data.decode()
        new_yaml = yaml.safe_load(data)
        print(new_yaml)

if __name__ == '__main__':
    run_server()

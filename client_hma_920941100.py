import socket
import json


PROXY_HOST = "127.0.0.1"
PROXY_PORT = 8080

SERVER_IP = "127.0.0.1"
SERVER_PORT = 7000


def send_request(proxy_socket, server_ip, server_port, message):
    request = {
        "server_ip": server_ip,
        "server_port": server_port,
        "message": message
    }

    data = json.dumps(request)

    proxy_socket.sendall(data.encode())

    response = proxy_socket.recv(1024)

    return response.decode()


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_socket:
        proxy_socket.connect((PROXY_HOST, PROXY_PORT))

        response = send_request(
            proxy_socket,
            SERVER_IP,
            SERVER_PORT,
            "ping"
        )
        print(response)

        for _ in range(5):
            response = send_request(
                proxy_socket,
                SERVER_IP,
                SERVER_PORT,
                "ping"
            )
            print(response)

        response = send_request(
            proxy_socket,
            "192.168.1.1",
            SERVER_PORT,
            "ping"
        )
        print(response)

        response = send_request(
            proxy_socket,
            SERVER_IP,
            SERVER_PORT,
            "ping"
        )
        print(response)


if __name__ == "__main__":
    main()
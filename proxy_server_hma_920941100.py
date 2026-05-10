import socket
import threading
import json


HOST = "127.0.0.1"
PORT = 8080

BLOCKLIST = {"192.168.1.1"}


def forward_to_server(server_ip, server_port, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.connect((server_ip, server_port))

        server_socket.sendall(message.encode())

        response = server_socket.recv(1024)

        return response.decode()


def handle_request(request):
    try:
        server_ip = request["server_ip"]
        server_port = int(request["server_port"])
        message = request["message"]

        if server_ip in BLOCKLIST:
            return "Error"

        response = forward_to_server(server_ip, server_port, message)

        return response

    except Exception:
        return "Error"


def handle_client(client_socket):
    decoder = json.JSONDecoder()
    buffer = ""

    try:
        while True:
            data = client_socket.recv(4096)

            if not data:
                break

            buffer += data.decode()

            while buffer.strip():
                buffer = buffer.lstrip()

                try:
                    request, index = decoder.raw_decode(buffer)
                except json.JSONDecodeError:
                    break

                buffer = buffer[index:]

                response = handle_request(request)

                client_socket.sendall(response.encode())

    finally:
        client_socket.close()


def main():
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    proxy_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    proxy_socket.bind((HOST, PORT))

    proxy_socket.listen()

    while True:
        client_socket, client_address = proxy_socket.accept()

        thread = threading.Thread(
            target=handle_client,
            args=(client_socket,),
            daemon=True
        )
        thread.start()


if __name__ == "__main__":
    main()
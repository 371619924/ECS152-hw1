import socket
import threading


HOST = "127.0.0.1"
PORT = 7000


def handle_client(client_socket):
    try:
        while True:
            data = client_socket.recv(1024)

            if not data:
                break

            message = data.decode().strip()

            if message == "ping":
                client_socket.sendall(b"pong")
            else:
                client_socket.sendall(b"Error")
    finally:
        client_socket.close()


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((HOST, PORT))

    server_socket.listen()

    while True:
        client_socket, client_address = server_socket.accept()

        thread = threading.Thread(
            target=handle_client,
            args=(client_socket,),
            daemon=True
        )
        thread.start()


if __name__ == "__main__":
    main()
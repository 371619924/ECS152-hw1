import socket
import time


HOST = "127.0.0.1"
PORT = 6000
END_SIGNAL = b"__END__"


def main():
    # Create a UDP socket.
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind the server to 127.0.0.1:6000.
    server_socket.bind((HOST, PORT))

    total_bytes = 0
    start_time = None
    client_addr = None

    while True:
        # Receive one UDP datagram.
        data, addr = server_socket.recvfrom(65535)

        # Save the client address .
        client_addr = addr

        # The special ending message should not be counted.
        if data == END_SIGNAL:
            break

        # Start timing when the first real data packet arrives.
        if start_time is None:
            start_time = time.time()

        # Add this datagram's size to the total.
        total_bytes += len(data)

    end_time = time.time()

    # Avoid division by zero in case no data was received.
    if start_time is None:
        throughput = 0.0
    else:
        elapsed_time = end_time - start_time
        throughput = total_bytes / elapsed_time / 1024

    
    print(f"Bytes received: {total_bytes}", flush=True)

    # Required UDP response to the client.
    response = f"Throughput: {throughput:.2f} KB/s"
    if client_addr is not None:
        server_socket.sendto(response.encode(), client_addr)

    server_socket.close()


if __name__ == "__main__":
    main()
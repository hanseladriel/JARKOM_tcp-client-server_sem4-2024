import socket
import sys

def send_request(host, port, resource):
    # Buat socket TCP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect ke server
    server_address = (host, port)
    client_socket.connect(server_address)

    try:
        # Buat request HTTP
        request = f"GET {resource} HTTP/1.1\r\nHost: {host}:{port}\r\n\r\n"
        request = request.encode()

        # Kirim request ke server
        client_socket.sendall(request)

        # Terima respons dari server
        response = b""
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            response += data

        # Cetak respons
        print(response.decode())

    finally:
        # Bersihkan socket
        client_socket.close()

if __name__ == "__main__":
    # Dapatkan command-line arguments
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} server_host server_port filename")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])
    resource = f"/{sys.argv[3]}"

    # Kirim request ke server
    send_request(host, port, resource)
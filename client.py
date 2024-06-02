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
    host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8080
    resource = sys.argv[3] if len(sys.argv) > 3 else "/"
    
    if not resource.startswith("/"):
        resource = "/" + resource
    
    # Kirim request ke server
    send_request(host, port, resource)
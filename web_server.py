import socket
import os
import threading

def parse_request(client_socket):
    # Baca data request dari client socket
    request_data = client_socket.recv(1024)

    # Pisahkan data request menjadi baris
    request_lines = request_data.decode().split("\r\n")

    # Parsing baris request
    request_line = request_lines[0]
    request_parts = request_line.split()
    method = request_parts[0]
    resource = request_parts[1]
    http_version = request_parts[2]

    # Parsing headers
    headers = {}
    for line in request_lines[1:]:
        if line:
            key, value = line.split(": ")
            headers[key] = value

    # Kembalikan data request yang telah di-parsing
    return {
        "method": method,
        "resource": resource,
        "http_version": http_version,
        "headers": headers,
    }

def handle_client(client_socket, client_address):
    try:
        print(f"Connection from {client_address}")

        # Parsing request HTTP
        request_data = parse_request(client_socket)
        print(f"Request: {request_data}")

        # Dapatkan resource yang diminta
        requested_resource = request_data["resource"]

        # Konstruksi jalur file
        file_path = os.path.join(".", requested_resource[1:])  # Hapus '/' di awal

        # Periksa apakah file ada
        if os.path.isfile(file_path):
            # Baca isi file
            with open(file_path, "rb") as file:
                file_data = file.read()

            # Konstruksi respons HTTP
            response_headers = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
            response_data = response_headers.encode() + file_data

        else:
            # File tidak ditemukan
            response_data = "HTTP/1.1 404 Not Found\r\n\r\n".encode()

        # Kirim respons ke client
        client_socket.sendall(response_data)

    finally:
        client_socket.close()

def start_server(host, port):
    # Buat socket TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind socket ke alamat server
    server_address = (host, port)
    server_socket.bind(server_address)

    # Listen untuk koneksi masuk
    server_socket.listen(5)

    print(f"Server sedang mendengarkan pada {host}:{port}")

    try:
        while True:
            # Tunggu koneksi client
            print("Menunggu koneksi...")
            client_socket, client_address = server_socket.accept()

            # Mulai thread baru untuk menangani koneksi client
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()

    except KeyboardInterrupt:
        print("\nServer dihentikan.")
        server_socket.close()

if __name__ == "__main__":
    # Dapatkan host dan port server
    host = socket.gethostname()
    port = 8000

    # Mulai server
    start_server(host, port)
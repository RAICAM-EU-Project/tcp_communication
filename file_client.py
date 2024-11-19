import socket

def receive_file(server_ip, server_port=12344, save_dir="."):
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server
        client_socket.connect((server_ip, server_port))
        print(f"Connected to server at {server_ip}:{server_port}")

        # Receive metadata
        metadata = client_socket.recv(1024).decode()
        if metadata.startswith("ERROR"):
            print(f"Server error: {metadata}")
            return

        file_name, file_size = metadata.split(":")
        file_size = int(file_size)
        print(f"Receiving file: {file_name} ({file_size} bytes)")

        # Send acknowledgment
        client_socket.sendall(b"READY")

        # Receive file data in chunks
        received_size = 0
        with open(f"{save_dir}/{file_name}", 'wb') as f:
            while received_size < file_size:
                chunk = client_socket.recv(1024)
                if not chunk:
                    break
                f.write(chunk)
                received_size += len(chunk)
                print(f"Progress: {received_size}/{file_size} bytes", end="\r")

        print(f"\nFile {file_name} received successfully.")
    finally:
        client_socket.close()

if __name__ == "__main__":
    # SERVER_IP = "192.168.2.64"  # Replace with Computer 1's IP
    SERVER_IP = "127.0.0.1" 
    receive_file(SERVER_IP)

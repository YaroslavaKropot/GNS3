#!/usr/bin/env python3
import socket
import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 server.py <IP>")
        sys.exit(1)
    
    ip = sys.argv[1]
    port = 5000
    
    try:
        socket.inet_pton(socket.AF_INET, ip)
        family = socket.AF_INET
        ip_type = "IPv4"
    except socket.error:
        try:
            socket.inet_pton(socket.AF_INET6, ip)
            family = socket.AF_INET6
            ip_type = "IPv6"
        except socket.error:
            print(f"Error: '{ip}' is not a valid IPv4 or IPv6 address")
            sys.exit(1)
    
    sock = socket.socket(family, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        sock.bind((ip, port))
    except Exception as e:
        print(f"Bind error: {e}")
        sys.exit(1)
    
    sock.listen(5)
    print(f"Server listening on {ip} ({ip_type}), port {port}")
    
    while True:
        client, addr = sock.accept()
        client_ip = addr[0]
        client_port = addr[1]
        print(f"From [{client_ip}:{client_port}] connected")
        
        data = client.recv(1024).decode()
        print(f"From [{client_ip}:{client_port}] received message: {data}")
        
        if data.lower() == "close":
            print("Closing server...")
            client.close()
            break
        
        response = data.upper()
        client.send(response.encode())
        print("Reply sent")
        client.close()
    
    sock.close()

if __name__ == "__main__":
    main()
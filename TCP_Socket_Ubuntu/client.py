#!/usr/bin/env python3
import socket
import sys

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 client.py <IP> <message>")
        sys.exit(1)
    
    ip = sys.argv[1]
    msg = sys.argv[2]
    port = 5000
    
    try:
        socket.inet_pton(socket.AF_INET, ip)
        family = socket.AF_INET
    except socket.error:
        try:
            socket.inet_pton(socket.AF_INET6, ip)
            family = socket.AF_INET6
        except socket.error:
            print(f"Error: '{ip}' is not a valid IPv4 or IPv6 address")
            sys.exit(1)
    
    sock = socket.socket(family, socket.SOCK_STREAM)
    
    try:
        sock.connect((ip, port))
    except Exception as e:
        print(f"Connection failed: {e}")
        sys.exit(1)
    
    print(f"sending message: {msg}")
    sock.send(msg.encode())
    
    reply = sock.recv(1024).decode()
    print(f"reply from server: {reply}")
    
    sock.close()

if __name__ == "__main__":
    main()
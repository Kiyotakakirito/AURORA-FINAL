import socket

host = "db.malrtperngdlvelxvjvp.supabase.co"
print(f"Testing DNS for: {host}")
try:
    results = socket.getaddrinfo(host, 5432, socket.AF_UNSPEC, socket.SOCK_STREAM)
    print(f"Resolved {len(results)} addresses:")
    for r in results:
        print(f"  family={r[0]}, addr={r[4]}")
except Exception as e:
    print(f"DNS FAILED: {e}")

# Also test port connectivity
import socket as s
print("\nTesting TCP port 5432 to db host...")
try:
    sock = s.create_connection((host, 5432), timeout=8)
    print("Port 5432 OPEN")
    sock.close()
except Exception as e:
    print(f"Port 5432 BLOCKED/FAILED: {e}")

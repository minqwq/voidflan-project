import socket

class network_ip:
    def get_public_ips():
        # 获取IPv4
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(('8.8.8.8', 80))
                ipv4 = s.getsockname()[0]
        except Exception as e:
            print(f"IPv4: {e}")

        # 获取IPv6
        try:
            with socket.socket(socket.AF_INET6, socket.SOCK_DGRAM) as s:
                s.connect(('2001:4860:4860::8888', 80))
                ipv6 = s.getsockname()[0]
        except Exception as e:
            print(f"IPv6: {e}")

        print(f"IPv4: {ipv4}")
        print(f"IPv6: {ipv6}")

    def get_local_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("114.114.114.114", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip

import socket
import time
from ping3 import ping, verbose_ping


class NetTracer:
    def __init__(self, hosts, ports=None, interval=5):
        """
        :param hosts: List of hosts to monitor
        :param ports: List of ports to check on each host, defaults to None
        :param interval: Interval between checks in seconds, defaults to 5 seconds
        """
        self.hosts = hosts
        self.ports = ports if ports else []
        self.interval = interval

    def ping_host(self, host):
        """
        Ping a host and return the latency or failure
        :param host: Hostname or IP to ping
        :return: Round trip time in ms or 'Request timed out' if unreachable
        """
        try:
            response_time = ping(host, timeout=2)
            if response_time:
                return f"Ping to {host}: {response_time * 1000:.2f} ms"
            else:
                return f"Ping to {host} failed: Request timed out"
        except Exception as e:
            return f"Ping to {host} failed: {e}"

    def check_port(self, host, port):
        """
        Check if a specific port is open on the host
        :param host: Hostname or IP
        :param port: Port number to check
        :return: Status message
        """
        try:
            with socket.create_connection((host, port), timeout=3):
                return f"Port {port} on {host} is OPEN"
        except (socket.timeout, ConnectionRefusedError):
            return f"Port {port} on {host} is CLOSED"
        except Exception as e:
            return f"Port check error on {host}:{port} - {e}"

    def monitor(self):
        """
        Start the monitoring process for hosts and ports
        """
        while True:
            for host in self.hosts:
                print(self.ping_host(host))

                for port in self.ports:
                    print(self.check_port(host, port))

            print("\nWaiting for the next round...\n")
            time.sleep(self.interval)


if __name__ == "__main__":
    # Define the hosts and ports you want to monitor
    hosts_to_monitor = ['8.8.8.8', 'example.com']  # IPs or hostnames
    ports_to_monitor = [80, 443]  # Common HTTP(S) ports

    # Create an instance of the NetTracer
    tracer = NetTracer(hosts=hosts_to_monitor, ports=ports_to_monitor, interval=10)

    # Start monitoring
    tracer.monitor()

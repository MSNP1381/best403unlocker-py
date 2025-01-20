import configparser
import platform
import subprocess
import sys
from typing import List
from urllib.parse import urlparse
import dns.resolver
import requests
from rich.progress import Progress
import shutil
import ipaddress
import os
import logging
import ctypes
from rich.prompt import Prompt
from rich.table import Table


logger =logging.getLogger(__name__)
# logger.addHandler(handler)
# Configure logging


def test_url_with_custom_dns(url, dns_server, results,progress:Progress):
    def resolve_dns_with_custom_server(hostname, dns_server):
        resolver = dns.resolver.Resolver()
        resolver.nameservers = [dns_server]
        # parsed_url = urlparse(url)
        # hostname = parsed_url.hostname
        try:
            answer = resolver.resolve(hostname)
            logger.info(f"Resolved {hostname} to {answer[0].address} with {dns_server}")
            return answer[0].address
        except Exception:
            logger.warning(f"DNS resolution error with {dns_server}")
            return None

    progress.console.print(f"Testing with DNS server: {dns_server}")
    ip_address = resolve_dns_with_custom_server(url, dns_server)
    if ip_address:
        try:
            headers = {
                "Host": urlparse(url).hostname,
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
            }

            proxies = {"http": None, "https": None, "ftp": None}
            response = requests.get(
                f"http://{ip_address}", timeout=2, proxies=proxies, headers=headers
            )
            progress.console.print(f"Status Code: {response.status_code}")
            if response.status_code >= 200 and response.status_code < 300:
                logger.info(f"HTTP request successful with {dns_server}")
                results[dns_server] = response.elapsed.total_seconds()
                progress.console.print(
                    f"*****\n\n\t\t OK {round(response.elapsed.total_seconds(),2)}\n\n*****"
                )
            # else:
            #     logger.warning(f"HTTP request failed. Status code: {response.status_code}")
        except requests.RequestException as e:
            logger.warning(f"HTTP request error: {e}")
    else:
        logger.warning("Failed to resolve DNS.")


def read_config():
    config_path = os.path.expanduser("~/.unlock403/best403unlocker.conf")
    config_dir = os.path.dirname(config_path)
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    if not os.path.exists(config_path):
        response = requests.get(
            "https://raw.githubusercontent.com/MSNP1381/best403unlocker-py/refs/heads/main/best403unlocker.conf"
        )
        with open(config_path, "w") as configfile:
            configfile.write(response.text)
    config = configparser.ConfigParser()
    config.read(config_path)
    dns_servers = config.get("dns", "dns").replace('"', "").split()
    return dns_servers


def write_dns_config(dns_servers):
    config_path = os.path.expanduser("~/.unlock403/best403unlocker.conf")
    config_dir = os.path.dirname(config_path)
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    config = configparser.ConfigParser()
    config["dns"] = {"dns": " ".join(dns_servers)}
    with open(config_path, "w") as configfile:
        config.write(configfile)


def sort_dict(results: dict):
    values = sorted(results.items(), key=lambda item: item[1])
    return [i[0] for i in values]


def set_dns(dns_servers: List[str],progress:Progress):
    os_type = platform.system().lower()

    def validate_dns_servers(dns_servers):
        valid_dns_servers = []
        for i in dns_servers:
            try:
                ipaddress.ip_address(i)
                valid_dns_servers.append(i)
            except ValueError:
                logger.debug(f"Invalid DNS server IP: {i}")
                exit()
        return valid_dns_servers
    dns_servers = validate_dns_servers(dns_servers)
    if os_type == "windows":
        set_dns_windows(dns_servers,progress)
    elif os_type == "darwin":
        set_dns_mac(dns_servers)
    elif os_type == "linux":
        set_dns_linux(dns_servers)
    else:
        logger.debug(f"Unsupported OS: {os_type}")


def set_dns_windows(dns_servers,progress:Progress):
    if not dns_servers:
        return
    columns, _ = shutil.get_terminal_size()
    padding = "*" * columns

    windows_logo = """
             _.-;;-._
      '-..-'|   ||   |
      '-..-'|_.-;;-._|
      '-..-'|   ||   |
jgs   '-..-'|_.-''-._|"""
    print(padding)
    print(windows_logo)
    print("Windows detected")
    print("windows doesn't support changing DNS servers, change it manually")
    print("")
    if len(dns_servers) >= 1:
        print(padding)
        print(dns_servers[0])
    if len(dns_servers) > 1:
        print(dns_servers[1])
        print("")

        print(padding)
    print("")
    #list windows network interface names then select which interface intractivly using rich library
    def list_windows_interfaces():
        command = 'netsh interface show interface'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        interfaces = []
        if result.returncode == 0:
            lines = result.stdout.splitlines()
            for line in lines[3:]:
                parts = line.split()
                if len(parts) >= 4:
                    interfaces.append(parts[-1])
        return interfaces

    interfaces = list_windows_interfaces()

    if not interfaces:
        logger.warning("No network interfaces found.")
        return

    table = Table(title="Network Interfaces")
    table.add_column("Index", justify="right", style="cyan", no_wrap=True)
    table.add_column("Interface Name", style="magenta")

    for idx, interface in enumerate(interfaces):
        table.add_row(str(idx), interface)

    progress.console.print(table)

    interface_index = Prompt.ask("Select the interface index", choices=[str(i) for i in range(len(interfaces))])
    interface_name = interfaces[int(interface_index)]
    progress.console.print(f"Selected interface: {interface_name}")
    
    primary_dns = dns_servers[0] if len(dns_servers) > 0 else None
    secondary_dns = dns_servers[1] if len(dns_servers) > 1 else None

    if primary_dns:
        command = f'netsh interface ip set dns name="{interface_name}" source=static addr={primary_dns}'
        subprocess.run(["powershell", "-Command", f'Start-Process powershell -ArgumentList \'{command}\' -Verb RunAs'], shell=True)
        logger.info(f"Primary DNS set to {primary_dns}")

        if secondary_dns:
            command = f'netsh interface ip add dns name="{interface_name}" addr={secondary_dns} index=2'
            subprocess.run(["powershell", "-Command", f'Start-Process powershell -ArgumentList \'{command}\' -Verb RunAs'], shell=True)
            logger.info(f"Secondary DNS set to {secondary_dns}")
    else:
        logger.warning("Administrator privileges are required to change DNS settings on Windows.")


def set_dns_mac(dns_servers):
    network_service = "Wi-Fi"  # Change this to your network service name if different
    dns_string = ",".join(dns_servers)
    command = f"networksetup -setdnsservers {network_service} {dns_string}"
    subprocess.run(command, shell=True)


def set_dns_linux(dns_servers):
    print("Linux detected")
    resolv_conf = "/etc/resolv.conf"
    # select first two dns servers
    dns_servers = dns_servers[:2]
    command = f"echo '{chr(10).join([f'nameserver {dns}' for dns in dns_servers])}' | sudo tee {resolv_conf} > /dev/null"
    subprocess.run(command, shell=True)


def scan_dns_servers(url, dns_servers):
    with Progress() as progress:
        
        results = {i: 1000 for i in dns_servers}
        for dns_server in progress.track(dns_servers, description="Testing DNS servers"):
            test_url_with_custom_dns(url, dns_server, results,progress)
        return results,progress

def check_if_sudo_or_admin():
    if os.name == 'nt':
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except Exception:
            return False
    else:
        return os.geteuid() == 0
def change_permission_to_sudo_or_admin():
    if os.name == 'nt':
        # Windows-specific code to check for admin privileges
        try:
            is_admin = os.getuid() == 0
        except AttributeError:
            is_admin = subprocess.run(["powershell", "-Command", "Test-ProcessAdminRights"], capture_output=True, text=True).stdout.strip() == "True"
    else:
        # Unix-specific code to check for sudo privileges
        is_admin = os.geteuid() == 0

    if not is_admin:
        if os.name == 'nt':
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

def main():

    # results,_=scan_dns_servers('https://developers.google.com',read_config())
    # sorted_dns_servers = sort_dict(results)
    # final_result=[]
    # for dns_, time in sorted(results.items(), key=lambda x: x[1]):
    #     if time==1000:
    #         pass
    #         # print(f"{dns_}: no response")
    #     else:
    #         final_result.append(dns_)
    #         print(f"{dns_}: {round(time, 2)} seconds")
    with Progress() as progress:
        set_dns(['87.107.153.60'],progress)
    # os_type = platform.system().lower()


if __name__ == "__main__":
    main()

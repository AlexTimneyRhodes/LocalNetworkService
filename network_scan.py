import asyncio
import ipaddress
from tqdm import tqdm
import aiohttp
from bs4 import BeautifulSoup

COMMON_PORTS = [22, 80, 443, 8080, 9090, 8001, 7878, 8989, ]

# semaphore = asyncio.Semaphore(255)  # Adjust this number based on performance

async def scan_port(ip, port, session):
    # async with semaphore:
        try:
            reader, writer = await asyncio.wait_for(asyncio.open_connection(ip, port), timeout=1)
            writer.close()
            await writer.wait_closed()
            return port, await get_service_name(ip, port, session)
        except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
            return None

async def get_service_name(ip, port, session):
    try:
        async with session.get(f"http://{ip}:{port}", timeout=2) as response:
            if response.status == 200:
                soup = BeautifulSoup(await response.text(), 'html.parser')
                title = soup.title.string if soup.title else 'Unknown Service'
                return title.strip()
    except Exception as e:
        print(f"[DEBUG] Error getting service name for {ip}:{port}: {str(e)}")
    return 'Unknown Service'

async def scan_host(ip, session):
    tasks = [scan_port(str(ip), port, session) for port in COMMON_PORTS]
    results = await asyncio.gather(*tasks)
    open_ports = [result for result in results if result]
    return str(ip), open_ports

async def scan_network(network):
    all_ips = list(ipaddress.IPv4Network(network))
    active_hosts = {}

    print(f"[INFO] Starting scan of network: {network}")
    print(f"[DEBUG] Total IPs to scan: {len(all_ips)}")

    async with aiohttp.ClientSession() as session:
        tasks = [scan_host(ip, session) for ip in all_ips]
        for future in tqdm(asyncio.as_completed(tasks), total=len(tasks), desc="Scanning hosts", ncols=80):
            ip, open_ports = await future
            if open_ports:
                active_hosts[ip] = open_ports
                print(f"[INFO] Found active host: {ip} with open ports: {open_ports}")

    print(f"[INFO] Scan complete. Total active hosts found: {len(active_hosts)}")
    return active_hosts

# Example usage
async def main():
    network = '192.168.1.0/24'  # Adjust this to match your network range
    active_hosts = await scan_network(network)

    print("[INFO] Scan complete.")
    print(f'Active hosts and their open ports: {active_hosts}')

# Check if running in an existing event loop environment
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError as e:
        # This handles running in an environment like Jupyter notebooks or certain IDEs
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())

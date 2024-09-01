from app import app
from hypercorn.config import Config
from hypercorn.asyncio import serve
import asyncio
import logging

from network_scan import scan_network

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

async def run_scan():
    network = '192.168.1.0/24'  # Adjust this to match your network
    print("[INFO] Starting network scan...")
    results = await scan_network(network)
    print("[INFO] Scan complete. Results:")
    print(results)

async def main():
    config = Config()
    config.bind = ["0.0.0.0:5000"]
    
    # Run the scan before starting the server
    await run_scan()
    
    # Start the server
    await serve(app, config)

if __name__ == "__main__":
    asyncio.run(main())

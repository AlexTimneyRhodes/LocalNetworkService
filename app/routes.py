from flask import render_template
from app import app
from network_scan import scan_network
import asyncio

# Example network
network = '192.168.1.0/26'

@app.route('/')
async def home():
    host_ports = await scan_network(network)
    return render_template('index.html', host_ports=host_ports)
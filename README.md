
# Local Web Service

This project is a Flask-based web application that scans your local network for active hosts and open ports, displaying the results in a web interface.

## Features

- Asynchronous network scanning using Python's asyncio.
- Web interface to display active hosts and their open ports.
- Supports scanning custom network ranges.
- Built-in progress bar to monitor the scanning process.

## Requirements

Ensure you have the following dependencies installed:

```
Flask[async]==2.0.1
Werkzeug==2.0.3
tqdm==4.64.0
requests==2.26.0
beautifulsoup4==4.10.0
aiohttp==3.10.5
hypercorn==0.14.3
```

You can install them using pip:

```bash
pip install -r requirements.txt
```

## Project Structure

```
project-directory/
│
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── templates/
│   │   └── index.html
│
├── network_scan.py
├── requirements.txt
└── run.py
```

- `app/`: Contains the Flask application files.
  - `__init__.py`: Initializes the Flask app.
  - `routes.py`: Defines the routes for the web application.
  - `templates/`: Contains the HTML template for displaying scan results.
- `network_scan.py`: Handles the asynchronous network scanning logic.
- `requirements.txt`: Lists all the dependencies required for the project.
- `run.py`: The entry point for running the application with Hypercorn.

## Running the Application

1. **Clone the repository**:

    ```bash
    git clone https://your-repo-link.git
    cd project-directory
    ```

2. **Install the dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

3. **Run the application**:

    ```bash
    python run.py
    ```

    This will start the network scan and launch the web server.

4. **Access the Web Interface**:

    Open your web browser and go to `http://localhost:5000` to view the scan results.

## Running the Application on Boot (Fedora Linux)

1. **Create a Systemd Service File**:

    Create a service file `/etc/systemd/system/localwebservice.service` with the following content:

    ```ini
    [Unit]
    Description=Local Web Service
    After=network.target

    [Service]
    User=your_username
    Group=your_username
    WorkingDirectory=/home/your_username/Desktop/LocalWebService
    ExecStart=/usr/bin/python3 /home/your_username/Desktop/LocalWebService/run.py
    Restart=always
    RestartSec=10
    Environment="PATH=/home/your_username/.local/bin:/usr/bin"

    [Install]
    WantedBy=multi-user.target
    ```

2. **Reload systemd and enable the service**:

    ```bash
    sudo systemctl daemon-reload
    sudo systemctl enable localwebservice.service
    ```

3. **Start the service**: 

    ```bash
    sudo systemctl start localwebservice.service
    ```

4. **Check the status**:

    ```bash
    sudo systemctl status localwebservice.service
    ```

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

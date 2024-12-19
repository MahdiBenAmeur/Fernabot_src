# Fernabot_src
# FernaBot

Welcome to the official repository for FernaBot's ongoing development. This repository contains the essential code and configurations for the FernaBot project, a Facebook Messenger bot designed to assist users with real-time information and interactions.

## Key Files

- **main.py**: This file contains the server setup for FernaBot. Launching this file will start the server, enabling it to accept requests from the Facebook Messenger API.
- **interface.py**: This provides a GUI interface that allows users to add data to the database by simply dropping Excel sheets into the application.

## Requirements

- **MySQL**: Ensure MySQL is installed and running on your machine.
- **Configuration**: Update `config.json` with the necessary database credentials and tokens from the Facebook Messenger API.
- **Python Version**: The code is compatible with Python 3.10.
- **Dependencies**: Install all required packages using the provided `requirements.txt` file by running:

```bash
pip install -r requirements.txt

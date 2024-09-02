## IMPORTANT NOTE
This repository is intended for my personal notes and portfolio purposes on LinkedIn. I do not expect any contributions from others. Thank you for understanding!

# POC Whoosh Indonesia Schedule API

This repository contains a Proof of Concept (POC) for checking the schedule of Whoosh, the Indonesian bullet train. Once the schedule is available, the application sends notifications via REST API to LINE messenger and stores the data in SQLite.

## Features

- **Check Whoosh Schedule**: Automatically fetches the latest schedule for the Indonesian bullet train.
- **Send Notifications**: Sends schedule notifications to LINE messenger using REST API.
- **Data Storage**: Stores schedule data in a local SQLite database.

## Getting Started

### Prerequisites

- Python 3.x
- SQLite
- LINE Messaging API credentials

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/ariogunawan/POC-Whoosh-Indonesia-Schedule-API.git
    cd POC-Whoosh-Indonesia-Schedule-API
    ```

2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

### Configuration

1. Set up your LINE Messaging API credentials:
    - Create a `.env` file in the root directory.
    - Add your LINE Messaging API credentials to the `.env` file:
        ```
        LINE_CHANNEL_ACCESS_TOKEN=your_channel_access_token
        LINE_CHANNEL_SECRET=your_channel_secret
        ```

### Usage

1. Run the application:
    ```bash
    python main.py
    ```

2. The application will:
    - Check the Whoosh schedule.
    - Send notifications to LINE messenger.
    - Store the schedule data in SQLite.

## Project Structure

- `main.py`: The main script to run the application.
- `whoosh_api.py`: Contains functions to fetch the Whoosh schedule.
- `line_notify.py`: Contains functions to send notifications to LINE messenger.
- `database.py`: Contains functions to interact with the SQLite database.
- `requirements.txt`: List of required Python packages.
- `.env.example`: Example environment file for LINE Messaging API credentials.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [LINE Messaging API](https://developers.line.biz/en/services/messaging-api/)
- [SQLite](https://www.sqlite.org/index.html)

## IMPORTANT NOTE
This repository is intended for my personal notes and portfolio purposes on LinkedIn. I do not expect any contributions from others. Thank you for understanding!

For Linux deployment - Don't forget to CHOWN -R ubuntu:ubuntu _the_current_folder_

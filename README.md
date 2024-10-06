
# Interface 

This project provides an interface to interact with machines via a web-based application. It allows users to control and monitor various machine operations, manage media files, and configure process settings using a user-friendly interface.

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Installation](#installation)
4. [Setting Up Virtual Environment (myenv)](#setting-up-virtual-environment-myenv)
5. [Running Daphne for ASGI](#running-daphne-for-asgi)
6. [Technologies Used](#technologies-used)
7. [Contributing](#contributing)
8. [License](#license)
9. [Contact](#contact)

## Introduction

The **Interface With Machine** project is designed to provide an efficient interface for interacting with various machine operations, allowing media management, process control, and real-time data visualization. This system can handle multiple media files (PDFs, videos) for the machine stations and provides sliders for media presentation.

## Features

- Control machine media (PDF and video) via an interface.
- Manage machine stations and associated media.
- Configure settings for media sliders and process information.
- Real-time data interaction and monitoring.
- Manage Fixture Cleaning Records (Create, Update, Delete, View)
- Manage Rejection Sheets
- Track Soldering Bit Records
- Daily, Weekly, and Monthly Maintenance Checklists
- Startup Checksheet Management
- P-Chart Data Management and Visualization
- Screen Content Display and Updates
- Support for PDF and Media Files
- Control Dashboard for Monitoring Key Metrics

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ft-prince/InterfaceWithMachine.git
   cd InterfaceWithMachine
   ```

2. Set up and activate the virtual environment (`myenv`):

   ```bash
   python -m venv myenv
   ```

   - **Windows:**
     ```bash
     myenv\Scripts\activate
     ```

   - **Linux/MacOS:**
     ```bash
     source myenv/bin/activate
     ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run database migrations:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser to access the admin interface:
   ```bash
   python manage.py createsuperuser
   ```


This will ensure that all dependencies are installed in an isolated environment, and your system's global Python packages remain unaffected.

## Running Daphne for ASGI

To run the project using `daphne`, follow these steps:

1. Open your terminal and navigate to the project root.

2. Use the following command to run `daphne` with the specified host and port:

   ```bash
   daphne -b 127.0.0.1 -p 8000 sopdisplay_core.asgi:application
   ```

This will launch the interface on your local machine, making it accessible at `http://127.0.0.1:8000`.

## Technologies Used

- **Django** - Python Web Framework
- **Daphne** - ASGI Server
- **Python** - Backend Development
- **HTML/CSS/JavaScript** - Frontend Technologies
- **SQLite** - Default Database (can be replaced with other DBs like PostgreSQL)

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request to help improve this project.

## License

This project is licensed under the Renata License.

## Contact

For any inquiries, feel free to reach out at:

- **Email:** [Reanataiot.com]
- **GitHub:** [ft-prince](https://github.com/ft-prince)

### Admin and User Access

- **Admin Access:**
  - Username: `prince`
  - Password: `123456`
  - Admin username: `admin`
  - Admin password: `interface123`

- **Normal User Access:**
  - Username: `user2`
  - Password: `interface123`

---


![image](https://github.com/user-attachments/assets/df8b4062-2130-4a83-a306-1bfe54e47ea4)

![image](https://github.com/user-attachments/assets/fca78cd7-c367-4c78-80e7-317e88e200b1)

![image](https://github.com/user-attachments/assets/38cb1571-004e-401e-8134-68164bd89082)


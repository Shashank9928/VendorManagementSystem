# Vendor Management System with Performance Metrics

This repository contains the Django backend for Vendor Management System with Performance Metrics, which includes a comprehensive Vendor Management System. Below you will find instructions to navigate the documentation and set up the project locally.

## Quick Start

Before diving into the detailed documentation, ensure you have Python installed on your machine. Clone the repository using:

```bash
git clone https://github.com/Shashank9928/VendorManagementSystem.git
cd VendorManagementSystem
```

## Documentation

The documentation is split into two main parts:

1. **Setup Documentation**: Detailed instructions for setting up the application locally can be found in the [SETUP_DOCS](./SETUP_DOCS.md). This includes instructions on environment setup, dependencies, and database configurations.

2. **API Documentation**: Comprehensive details about the API endpoints, including how to authenticate and use the APIs, are available in the [API_DOCS](./API_DOCS.md). This section is essential for developers looking to integrate or interact with the API.

## Features

Briefly list the key features of your application. For example:

- Vendor Profile Management
- Purchase Order Tracking
- Performance Metrics Analysis

## Running the Application

Quick steps to get the application running:

1. Activate the virtual environment:
   - Windows: `.\ve\Scripts\activate`
   - macOS/Linux: `ve venv/bin/activate`

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
   
4. Creating a Superuser
	- To access the Django admin panel and authenticate API requests, create a superuser:
	 ```bash
		python  manage.py  createsuperuser
	```

	- Follow the prompts to set the username, email, and password.

4. Start the development server:
   ```bash
   python manage.py runserver
   ```

Visit `http://127.0.0.1:8000/` in your browser to view the application.

## Running Tests

To run automated tests and ensure your setup is correct:

```bash
python manage.py test
```
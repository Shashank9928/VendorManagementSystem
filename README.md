# Vendor Management System with Performance Metrics

This repository contains the Django backend for Vendor Management System with Performance Metrics, which includes a comprehensive Vendor Management System. Below you will find instructions to navigate the documentation and set up the project locally.

## Quick Start

Before diving into the detailed documentation, ensure you have Python installed on your machine. Clone the repository using:

```bash



git  clone  https://github.com/Shashank9928/VendorManagementSystem.git



cd  VendorManagementSystem



```

## Documentation

The documentation is split into two main parts:

1.  **Setup Documentation**: Detailed instructions for setting up the application locally can be found in the [SETUP_DOCS](./SETUP_DOCS.md). This includes instructions on environment setup, dependencies, and database configurations.

2.  **API Documentation**: Comprehensive details about the API endpoints, including how to authenticate and use the APIs, are available in the [API_DOCS](./API_DOCS.md). This section is essential for developers looking to integrate or interact with the API.

## Features

Briefly list the key features of the application:

- Vendor Profile Management

- Purchase Order Tracking

- Performance Metrics Analysis

# Application Setup

To provide comprehensive documentation on setting up Django application, running it, and executing test cases, follow the structured guide below. This documentation will cover initial repository setup, environment configuration, dependency installation, application startup, and how to run tests.

### Setting Up the Repository and Environment

#### 1. Cloning the Repository

First, clone the repository to your local machine using git. Open a terminal and run the following command:

```bash



git  clone  https://github.com/Shashank9928/VendorManagementSystem.git



cd  VendorManagementSystem



```

#### 2. Setting Up a Virtual Environment

It's recommended to use a virtual environment for Python projects to manage dependencies separately from your global Python installation. If you haven't installed `virtualenv` yet, you can install it using pip:

```bash



pip  install  virtualenv



```

Create a new virtual environment in the project directory:

```bash



python  -m  venv  ve



```

Activate the virtual environment:

- On Windows:

```bash



.\ve\Scripts\activate



```

- On macOS and Linux:

```bash



source  ve/bin/activate



```

#### 3. Installing Dependencies

With the virtual environment activated, install the project dependencies:

```bash



pip  install  -r  requirements.txt



```

### Configuring the Application

#### 1. Setting Up the Database

If your Django project uses a database that requires initial setup (like PostgreSQL or MySQL), configure it accordingly. For SQLite (the default), no additional setup is required.

#### 2. Migrations

Run the following commands to perform database migrations:

```bash



python  manage.py  makemigrations



python  manage.py  migrate



```

#### 3. Creating a Superuser

To access the Django admin panel and authenticate API requests, create a superuser:

```bash



python  manage.py  createsuperuser



```

Follow the prompts to set the username, email, and password.

### Running the Application

Start the Django development server with the following command:

```bash



python  manage.py  runserver



```

The server will start, typically accessible via `http://127.0.0.1:8000/`.

### Running Test Cases

To ensure the application works as expected, you should run your test suite:

```bash



python  manage.py  test



```

This command will execute all tests defined in your application and provide a summary of the results.

### Accessing the Admin Panel

You can access the Django admin panel by navigating to `http://127.0.0.1:8000/admin` in your web browser. Log in using the superuser credentials you created earlier to manage your application’s data.

**Default Server Url**: [http://127.0.0.1:8000](http://127.0.0.1:8000/)

# API-DOCUMENTATION

## Authentication

### Overview

All API requests, with the exception of the login endpoint, require authentication. Our system utilizes token-based authentication to secure access and ensure that operations are performed by authenticated users.

### Creating a Superuser

Before authenticating, you must have a superuser account. If you haven't already set up a superuser, you can create one using the following command:

bash: `python manage.py createsuperuser`

Follow the prompts to set the username, email, and password for the superuser.

### Using a Pre-configured Superuser

If you are using the provided database (`db.sqlite3` from this repository), a superuser with the following credentials is already set up:

- **Username:** vendor

- **Password:** 1234

You can use these credentials to test and interact with the API without setting up a new superuser.

Include the token in the HTTP header as follows:

`Authorization: Token <YOUR_TOKEN>`

Replace `<YOUR_TOKEN>` with the token you received from the login response.

### 1. **LoginAPIView**

**Endpoint:** `/api/login/`

**Method:** POST

**Permissions:** Allow any user (authenticated or not)

**Description:**

Allows users to authenticate using a username and password to receive a token for subsequent requests.

**Request Parameters:**

- `username` (string): The user's username.

- `password` (string): The user's password.

**Responses:**

- **200 OK**: Successful authentication.

- **Body**: `{ "token": "<TOKEN>" }`

- **400 Bad Request**: Missing username or password.

- **Body**: `{ "error": "Both username and password are required." }`

- **401 Unauthorized**: Invalid username or password.

- **Body**: `{ "error": "Invalid Credentials" }`

- **405 Method Not Allowed**: If any method other than POST is used.

- **Body**: `{ "error": "<METHOD> method not allowed." }`

### 2. **VendorListCreateAPIView**

**Endpoint:** `/api/vendors/`

**Methods:** GET, POST

**Headers:**

- `Authorization: Token <YOUR_TOKEN>`

**Permissions:**

- Authenticated Users

**Description:**

- GET: Retrieves a list of all vendors.

- POST: Creates a new vendor.

**GET Responses:**

- **200 OK**: Successfully retrieved list.

- **Body**: List of vendor objects.

**POST Parameters:**

- Data required for creating a vendor (name, contact_details, address, vendor_code).

- `name` (string): Name Of Vendor

- `contact_details` (string): Contact info of vendor

- `address` (string): Addres details of vendor

- `vendor_code` (string): Vendor Code Alphaneumaric

**POST Responses:**

- **201 Created**: Vendor successfully created.

- **Body**: Newly created vendor object.

- **400 Bad Request**: Data validation failed.

- **Body**: Error messages.

### 3. **VendorDetailAPIView**

**Endpoint:** `/api/vendors/{vendor_id}/`

**Methods:** GET, PUT, DELETE

**Headers:** - `Authorization: Token <YOUR_TOKEN>`

**Permissions:**

- Authenticated Users

**Description:**

Handles operations on a single vendor identified by `vendor_id`.

**GET Responses:**

- **200 OK**: Vendor found and retrieved.

- **Body**: Vendor object.

- **404 Not Found**: Vendor does not exist.

- **Body**: `{ "error": "Vendor not found" }`

**PUT Parameters:**

- Fields that can be updated (name, contact_details, address, vendor_code).

- `name` (string): Name Of Vendor

- `contact_details` (string): Contact info of vendor

- `address` (string): Addres details of vendor

- `vendor_code` (string): Vendor Code Alphaneumaric

**PUT Responses:**

- **200 OK**: Vendor successfully updated.

- **Body**: Updated vendor object.

- **400 Bad Request**: Validation error.

- **Body**: Error messages.

- **404 Not Found**: Vendor does not exist.

- **Body**: `{ "error": "Vendor not found" }`

**DELETE Responses:**

- **204 No Content**: Vendor successfully deleted.

- **404 Not Found**: Vendor does not exist.

- **Body**: `{ "error": "Vendor not found" }`

### 4. **PurchaseOrderListCreateAPIView**

**Endpoint:** `/api/purchase_orders/`

**Methods:** GET, POST

**Headers:**

- `Authorization: Token <YOUR_TOKEN>`

**Permissions:**

- Authenticated Users

**Description:**

- GET: Retrieves a list of purchase orders, optionally filtered by `vendor_id`.

- POST: Creates a new purchase order.

**GET Parameters:**

- `vendor_id` (optional, query parameter): Filter purchase orders by vendor.

**GET Responses:**

- **200 OK**: List of purchase orders.

- **Body**: List of purchase order objects.

**POST Parameters:**

- Required data for creating a purchase order (vendor, po_number, order_date, delivery_date, items, quantity, status).

- `po_number` (string): Purchase Oder Number

- `vendor` (string): Vendor Id

- `order_date` (Timestamp): (2024-04-30T14:30:00Z)

- `issue_date` (Timestamp): (**Optional**)(2024-04-30T14:30:00Z)

- `delivery_date` (Timestamp): (2024-04-30T14:30:00Z)

- `items` (json): List id items with qty

      "items": {
      	"iten01": 89
        }

- `quantity` (int): quantity of tems

- `status` (string): (**Optional Default: pending**), pending, completed, canceled

- `acknowledgment_date` (Timestamp): (**Optional**)(2024-04-30T14:30:00Z)

**POST Responses:**

- **201 Created**: Purchase order successfully created.

- **Body**: Newly created purchase order object.

- **400 Bad Request**: Validation error.

- **Body**: Error messages.

### 5. **PurchaseOrderDetailAPIView**

**Endpoint:** `/api/purchase_orders/{po_id}/`

**Methods:** GET, PUT, DELETE

**Headers:**

- `Authorization: Token <YOUR_TOKEN>`

**Permissions:**

- Authenticated Users

**Description:**

Handles operations on a single purchase order identified by `po_id`.

**GET Responses:**

- **200 OK**: Purchase order found and retrieved.

- **Body**: Purchase order object.

- **404 Not Found**: Purchase order does not exist.

- **Body**: `{ "error": "Purchase order not found" }`

**PUT Parameters:**

- Fields that can be updated (delivery_date, items, quantity, status, etc.).

- `po_number` (string): Purchase Oder Number

- `vendor` (string): Vendor Id

- `order_date` (Timestamp): (2024-04-30T14:30:00Z)

- `issue_date` (Timestamp): (**Optional**)(2024-04-30T14:30:00Z)

- `delivery_date` (Timestamp): (2024-04-30T14:30:00Z)

- `items` (json): List id items with qty

      "items": {
      	"iten01": 89
        }

- `quantity` (int): quantity of tems

- `status` (string): (**Optional Default: pending**), pending, completed, canceled

- `acknowledgment_date` (Timestamp): (**Optional**)(2024-04-30T14:30:00Z)

**PUT Responses:**

- **200 OK**: Purchase order successfully updated.

- **Body**: Updated purchase order object.

- **400 Bad Request**: Validation error.

- **Body**: Error messages.

- **404 Not Found**: Purchase order does not exist.

- **Body**: `{ "error": "Purchase order not found" }`

**DELETE Responses:**

- **204 No Content**: Purchase order successfully deleted.

- **404 Not Found**: Purchase order does not exist.

- **Body**: `{ "error": "Purchase order not found" }`

### 6. **VendorPerformanceAPIView**

**Endpoint:** `/api/vendors/{vendor_id}/performance/`

**Methods:** GET

**Headers:**

- `Authorization: Token <YOUR_TOKEN>`

**Permissions:**

- Authenticated Users

**Description:**

Retrieves the performance metrics for a specific vendor for the current day.

**GET Responses:**

- **200 OK**: Performance data available and returned.

- **Body**: Performance metrics.

- **404 Not Found**: Either vendor not found or no data available for today.

- **Body**: `{ "error": "No performance data available for today." }` or vendor not found message.

### 7. **PurchaseOrderAcknowledgeAPIView**

**Endpoint:** `/api/purchase_orders/{po_id}/acknowledge/`

**Methods:** POST

**Headers:**

- `Authorization: Token <YOUR_TOKEN>`

**Permissions:**

- Authenticated Users

**Description:**

Acknowledges a purchase order by setting the acknowledgment date to now, if not already set.

**POST Responses:**

- **200 OK**: Purchase order acknowledged.

- **Body**: `{ "message": "Purchase order acknowledged successfully." }`

- **400 Bad Request**: Purchase order already acknowledged.

- **Body**: `{ "error": "Purchase order already acknowledged." }`

- **404 Not Found**: Purchase order does not exist.

- **Body**: `{ "error": "Purchase order not found" }`

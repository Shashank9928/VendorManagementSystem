
### Application Setup

To provide comprehensive documentation on setting up your Django application, running it, and executing test cases, follow the structured guide below. This documentation will cover initial repository setup, environment configuration, dependency installation, application startup, and how to run tests.

### Setting Up the Repository and Environment

#### 1. Cloning the Repository
First, clone the repository to your local machine using git. Open a terminal and run the following command:
```bash
git clone <https://github.com/Shashank9928/VendorManagementSystem.git>
cd <VendorManagementSystem>
```

#### 2. Setting Up a Virtual Environment
It's recommended to use a virtual environment for Python projects to manage dependencies separately from your global Python installation. If you haven't installed `virtualenv` yet, you can install it using pip:
```bash
pip install virtualenv
```
Create a new virtual environment in the project directory:
```bash
python -m venv ve
```
Activate the virtual environment:

- On Windows:
  ```bash
  .\ve\Scripts\activate
  ```
- On macOS and Linux:
  ```bash
  source ve/bin/activate
  ```

#### 3. Installing Dependencies
With the virtual environment activated, install the project dependencies:
```bash
pip install -r requirements.txt
```

### Configuring the Application

#### 1. Setting Up the Database
If your Django project uses a database that requires initial setup (like PostgreSQL or MySQL), configure it accordingly. For SQLite (the default), no additional setup is required.

#### 2. Migrations
Run the following commands to perform database migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

#### 3. Creating a Superuser
To access the Django admin panel and authenticate API requests, create a superuser:
```bash
python manage.py createsuperuser
```
Follow the prompts to set the username, email, and password.

### Running the Application

Start the Django development server with the following command:
```bash
python manage.py runserver
```
The server will start, typically accessible via `http://127.0.0.1:8000/`.

### Running Test Cases

To ensure the application works as expected, you should run your test suite:
```bash
python manage.py test
```
This command will execute all tests defined in your application and provide a summary of the results.

### Accessing the Admin Panel

You can access the Django admin panel by navigating to `http://127.0.0.1:8000/admin` in your web browser. Log in using the superuser credentials you created earlier to manage your application’s data.
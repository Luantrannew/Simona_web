# Django Order Management System

This is a Django-based Order Management System that manages customers, products, orders, and order lines. The project includes functionality to import data from a CSV file into the database and display lists of customers, products, and order lines on web pages.

## Features

- Import customer, product, order, and order line data from a CSV file.
- Display lists of customers, products, and order lines.
- Ensure data consistency by linking orders and order lines to existing customers and products.

## Requirements

- Python 3.11.4
- Django 5.0.6
- Pandas

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/your-repo-name.git
    ```

2. Navigate to the project directory:
    ```bash
    cd your-repo-name
    ```

3. Create a virtual environment:
    ```bash
    python -m venv env
    ```

4. Activate the virtual environment:
    - On Windows:
        ```bash
        .\env\Scripts\activate
        ```
    - On macOS and Linux:
        ```bash
        source env/bin/activate
        ```

5. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

6. Apply migrations:
    ```bash
    python manage.py migrate
    ```

## Usage

1. Run the development server:
    ```bash
    python manage.py runserver
    ```

2. Open your web browser and go to `http://127.0.0.1:8000` to access the application.

## Importing Data

To import data from a CSV file, ensure your CSV file is properly formatted with the necessary columns for customers, products, orders, and order lines.

Update the path to your CSV file in the `data` variable in the views where data import is handled.



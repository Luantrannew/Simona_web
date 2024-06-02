# Django Order Management System

This is a Django-based Order Management System that manages customers, products, orders, and order lines. The project includes functionality to import data from a CSV file and save it into a PostgreSQL database.
![image](https://github.com/Luantrannew/Simona_web/assets/62492632/967e83d4-cbf7-4e50-a22a-cdca08e3d8f0)

## Features

- Import customer, product, order, and order line data from a CSV file.
- Save the imported data into a PostgreSQL database.
- Display lists of customers, products, and order lines.

## Requirements

- Python 3.11.4
- Django==2.2
- Django==5.0.6
- pandas==2.2.2

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Luantrannew/Simona_web
    ```

2. Navigate to the project directory:
    ```bash
    cd simona
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
    python manage.py makemigrations
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



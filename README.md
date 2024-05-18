# Django Order Management System

This is a Django-based Order Management System that manages customers, products, orders, and order lines. The project includes functionality to import data from a CSV file and save it into a PostgreSQL database.


![image](https://github.com/Luantrannew/Simona_web/assets/62492632/a2d8b62d-aea8-4d34-acc7-6e90e44b4172)
![image](https://github.com/Luantrannew/Simona_web/assets/62492632/5e8ae6c9-f856-43f9-908d-c3f2ac7551ae)
![image](https://github.com/Luantrannew/Simona_web/assets/62492632/df2a8e56-2be1-44c1-9177-052a964ac9b9)


## Features

- Import customer, product, order, and order line data from a CSV file.
- Save the imported data into a PostgreSQL database.
- Display lists of customers, products, and order lines.

## Requirements

- Python 3.11.4
- Django 5.0.6
- Pandas

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Luantrannew/Simona_web
    ```

2. Navigate to the project directory:
    ```bash
    cd Simona_web
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



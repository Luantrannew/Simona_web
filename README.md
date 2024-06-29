# Django Order Management System

This is a Django-based Order Management System that manages customers, products, orders, and order lines. The project includes functionality to import data from a CSV file and save it into a PostgreSQL database.

## Features

- Save the imported data into a PostgreSQL database.
- Display lists of customers, products, and order lines.

## Screenshots

![Dashboard](https://github.com/Luantrannew/Simona_web/assets/62492632/27107d9c-13be-4f8d-8693-007245ed7104)
*Dashboard*

![Customers List](https://github.com/Luantrannew/Simona_web/assets/62492632/7c6d7685-2c3b-42b3-b4d6-d99ccbc6e560)
*Modal*

![Order Lines](https://github.com/Luantrannew/Simona_web/assets/62492632/151abb15-07b2-4668-bd0e-98c0e215e335)
*Order*

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

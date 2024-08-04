# Django Project

Welcome to the Django Project! This document will guide you through the steps required to set up and run the project locally on your machine.
![image](https://github.com/user-attachments/assets/81296d46-a08d-4ba7-8c84-e755f5332861)


## Prerequisites

Ensure you have the following installed:

- [Python](https://www.python.org/downloads/) (3.8+ recommended)
- [pip](https://pip.pypa.io/en/stable/) (Python package installer)
- [virtualenv](https://virtualenv.pypa.io/en/latest/) (optional, but recommended)

## Getting Started

Follow these steps to set up and run the project:

1. **Clone the Repository**

    ```bash
    git clone [[https://github.com/yourusername/yourproject.git]()](https://github.com/PitRella/SPA_Comments.git)
    cd SPA_Comments
    ```

2. **Set Up a Virtual Environment**

    Create and activate a virtual environment:

    ```bash
    # Create virtual environment
    python -m venv venv

    # Activate virtual environment
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Configure the Database**

    This project uses MySQL. Ensure you have MySQL installed and configured. Update your `settings.py` file with your database credentials.

5. **Apply Migrations**

    Create and apply database migrations:

    ```bash
    python manage.py makemigrations
    python manage.py makemigrations comments
    python manage.py migrate
    ```

6. **Run the Server**

    ```bash
    python manage.py runserver
    ```

Your Django project should now be up and running at `http://127.0.0.1:8000/`.

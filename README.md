# Django Project

Welcome to the Django Project! This document will guide you through the steps required to set up and run the project locally on your machine.

## Prerequisites

Ensure you have the following installed:

- [Python](https://www.python.org/downloads/) (3.8+ recommended)
- [pip](https://pip.pypa.io/en/stable/) (Python package installer)
- [virtualenv](https://virtualenv.pypa.io/en/latest/) (optional, but recommended)

## Getting Started

Follow these steps to set up and run the project:

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/yourproject.git
cd yourproject


2. Set Up a Virtual Environment

Create and activate a virtual environment
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
3. Install Dependencies
pip install -r requirements.txt
4. Configure the Database
In my project i used mysql

5. Apply Migrations

Create and apply database migrations:

bash

python manage.py makemigrations
python manage.py migrate

python manage.py runserver

# Split Wisely Project

This project is a clone of the popular expense-splitting application, Splitwise. It's built using Django and HTMX, providing a dynamic and interactive user experience with minimal JavaScript.

## Features

* **Group Expense Management:**
    * Create and manage groups.
    * Add expenses to groups.
    * Split expenses equally or with custom amounts among group members.
* **User Authentication:**
    * User registration and login.
* **Dynamic UI with HTMX:**
    * Loading indicators during form submissions.
    * Real-time updates without full page reloads.
* **Efficient Database Operations:**
    * Use of `bulk_create` for efficient creation of multiple `Split` instances.
    * Use of `prefetch_related` and `select_related` to minimize database queries.
* **Admin Interface:**
    * Customized Django admin interface for managing expenses and users.

## Project Structure
```
split-wisely/
├── splitwise/           # Django project settings
│   ├── pycache/
│   ├── init.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── static/              # Static files (CSS)
│   ├── auth.css
│   └── global.css
├── templates/           # Django templates
│   └── users/           # User-related templates
│       ├── pycache/
│       ├── migrations/
│       └── templates/
│           ├── init.py
│           ├── admin.py
│           ├── apps.py
│           ├── models.py
│           ├── urls.py
│           └── views.py
├── .gitignore
├── db.sqlite3
├── manage.py
└── requirements.txt
```

## Technologies Used

* **Django:** Python web framework.
* **HTMX:** Library for accessing AJAX, CSS Transitions, WebSockets and Server Sent Events directly in HTML, using attributes.
* **Python:** Programming language.
* **HTML/CSS:** Front-end technologies.
* **JavaScript:** For enhanced interactivity.

## Setup

1.  **Clone the repository:**

    ```bash
    git clone git@github.com:RubeshChandar/split-wisely.git
    cd split-wisely
    ```

2.  **Create a virtual environment:**

    ```bash
    python -m venv .venv
    ```

3.  **Activate the virtual environment:**

    * On Windows:

        ```bash
        .venv\Scripts\activate
        ```

    * On macOS and Linux:

        ```bash
        source .venv/bin/activate
        ```

4.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

5.  **Apply migrations:**

    ```bash
    python manage.py migrate
    ```

6.  **Create a superuser:**

    ```bash
    python manage.py createsuperuser
    ```

7.  **Run the development server:**

    ```bash
    python manage.py runserver
    ```

8.  **Access the application:**

    * Open your web browser and go to `http://127.0.0.1:8000/`.

## Usage

* Register or log in to the application.
* Create groups and add members.
* Add expenses to groups, specifying the amount and how it should be split.
* View group expenses and balances.

## JavaScript Functionality

* Distributes expense amounts equally among selected users.
* Disables amount input fields when corresponding checkboxes are unchecked.
* Handles loading indicators during form submissions using HTMX.

## Contributing

Contributions are welcome! Please feel free to submit a pull request.


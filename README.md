# Video to PDF File Converter Application

## Description
This application converts video files into PDF documents, capturing audio and convert audio text to PDF. 
The application includes user authentication and permissions, allowing authenticated users to upload larger video files.

## Features
- Convert videos to PDF.
- Authenticated users can upload videos up to 100MB.
- Non-authenticated users can upload videos up to 10MB.
- User authentication and authorization.
- Seed command to run migrations, migrate the database, and create a superuser.

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/Prakash22Suthar/video_processor.git
    cd video_processor
    ```

2. **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the seed command to set up the database:**
    ```bash
    python manage.py seed
    ```

## Usage

1. **Start the development server:**
    ```bash
    python manage.py runserver
    ```

2. **Access the application:**
    Open your web browser and go to `http://127.0.0.1:8000`.

## Seed Command

The `seed` command will run the migrations, migrate the database, and create a superuser for accessing the Django admin.

Add the following command to your `management/commands/` directory in your Django app:

## Video Size Validation

Video file size validation is handled as follows:
- **Authenticated users:** Maximum video size of 100MB.
- **Non-authenticated users:** Maximum video size of 10MB.

Ensure you have implemented the necessary logic in your Django views to handle these validations.

## Contributing

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/fooBar`).
3. Commit your changes (`git commit -am 'Add some fooBar'`).
4. Push to the branch (`git push origin feature/fooBar`).
5. Create a new Pull Request.


---

Feel free to customize the above information according to your specific project details.

## Getting Started

1. **Clone the Repository**: Clone this repository to your local machine

2. **Install Requirements**: Navigate to the project directory and install the required packages using:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run Migrations**: Apply the database migrations to set up the initial database schema:

   ```bash
   python manage.py makemigrations && python manage.py migrate
   ```

4. **Create Dummy Data**: To quickly set up some initial data for testing, run the following commands:

   ```bash
   python manage.py create_accounts
   python manage.py create_hackathons
   ```

## Usage

1. Start the development server:
   ```bash
   python manage.py runserver
   ```

2. Access the API documentation:
   Open your web browser and navigate to [http://localhost:8000/api-docs/](http://localhost:8000/api-docs/) to access the API documentation.

3. Log in as an organiser:
   Use the following credentials to log in as an organiser:
   - Email: organiser@email.com
   - Password: easypassword
# MedTime
--
Your Health, On Time
--

MedTime is a drug scheduling and reminder application designed to help users manage their medication regimens effectively. Inspired by personal experiences of forgetting medication, this app allows users to input their drug schedules and receive timely reminders.

## Features

- **User Authentication**: Secure registration and login using JWT authentication.
- **Medication Scheduling**: Users can create and manage medication schedules, including dose details.
- **Dashboard Overview**: A user-friendly dashboard displaying ongoing medication, progress stats, and next dose reminders.
- **Notifications**: Future implementation of reminder notifications via email and push notifications.
- **Caregiver Support**: Upcoming features to allow caregivers to schedule prescriptions for their patients.
- **Data Visualization**: Visual representation of medication stats for better user insights.

## Technology Stack

- **Frontend**: 
  - React
  - Vite
  - CoreUI React Admin Dashboard Template
  - Material UI
  - SASS

- **Backend**: 
  - Python
  - Django
  - SQLite (intended for Postgres in future releases)

- **Authentication**: JWT with email OTP for secure user registration.

## Installation
- Clone the repo: `git clone `

### Frontend

1. Navigate to the frontend directory:
   ```bash
   cd MedTime-frontend
   ```

2. Install dependencies:
   ```bash
   $ npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

### Backend
1. Navigate to the backend directory:
   ```bash
   cd MedTime



2. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:

On Windows:
   ```bash
   venv\Scripts\activate
   ```

On macOS/Linux:
   ```bash
   source venv/bin/activate
   ```

4. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

5. Start the Django development server:

   ```bash
   python manage.py runserver
   ```

6. Connect to API to http://127.0.0.1:8000/ to use the backend API.

7. NOTE: Authentication Headers is needed for some protected endpoints


## Contributing
Contributions are welcome! Please feel free to submit issues or pull requests.

## License
This project is licensed under the MIT License - see the LICENSE file for details.


## Acknowledgements

Shoutout to CoreUI and the open-source community for their invaluable contributions. The CoreUI React template significantly accelerated development, and the landing page template by [Mona95](https://github.com/Mona95/React-Landingpage) provided a solid foundation for the app’s design.

# DriveX

A Flask-based ride booking web application inspired by modern ride-sharing platforms. DriveX allows users to register, log in, browse available cars by pickup point, calculate trip distance and fare, book rides, complete payments, and review wallet and activity history. Employees can manage the available car inventory from a dedicated dashboard.

## Overview

DriveX is a multi-role transportation booking platform built with **Flask**, **MongoDB**, **HTML/CSS**, and **JavaScript**. The project combines a traditional server-rendered web app with map-based trip selection using **Leaflet**, **OpenStreetMap**, and **Leaflet Routing Machine**.

The application currently supports three roles:

- **User** – register, log in, choose rides, pay for bookings, and view wallet/activity history
- **Employee** – log in and manage cars assigned to pickup points
- **Admin** – register and log in support exists in the current codebase

## Features

### User features
- User registration and login
- Role-based authentication using session management
- Ride search flow with pickup and dropoff locations
- Interactive map UI using Leaflet
- Car listing based on available pickup points
- Distance-based fare calculation
- Ride booking and payment flow
- Wallet history tracking
- Activity history tracking

### Employee features
- Employee registration and login
- Employee dashboard
- Add new cars with:
  - VIN number
  - model
  - capacity
  - color
  - description
  - image
  - plate number
  - price
  - pickup point
- Delete cars
- View all available cars
- Search cars dynamically

### System features
- MongoDB Atlas integration
- Unique indexes for email, IDs, and car VIN
- Default pickup point initialization on startup
- Session-based booking persistence
- OpenStreetMap geocoding and location suggestions
- Haversine-based backend distance calculation API

## Tech Stack

**Backend**
- Python
- Flask
- PyMongo
- Werkzeug
- python-dotenv
- requests

**Frontend**
- HTML5
- CSS3
- JavaScript
- Jinja2 templates

**Maps and Location**
- Leaflet
- Leaflet Routing Machine
- OpenStreetMap / Nominatim API

**Database**
- MongoDB Atlas

## Project Structure

```bash
DriveX/
├── app.py
├── requirements.txt
├── .env.example
├── drivex.sql
├── procfile
├── instance/
│   └── local.db
├── static/
│   ├── home.css
│   ├── register.css
│   ├── route.css
│   ├── payment.css
│   ├── user_dashboard.css
│   ├── employee_dashboard.css
│   ├── employee_dashboard.js
│   └── image/
├── templates/
│   ├── home.html
│   ├── register.html
│   ├── login.html
│   ├── user_dashboard.html
│   ├── route.html
│   ├── payment.html
│   ├── wallet.html
│   ├── activity.html
│   └── employee_dashboard.html
└── README.md
```

## How It Works

### 1. Registration and login
Users can create accounts as a **user**, **employee**, or **admin**. Passwords are hashed before storing them in MongoDB.

### 2. Ride selection
A logged-in user goes to the ride flow, selects a pickup and dropoff location, sees available cars, and chooses one.

### 3. Distance and pricing
The system calculates distance based on the selected locations and applies a fare rule of roughly **25 BDT per kilometer**.

### 4. Payment and booking
After a car is selected, the user completes billing and payment details. The booking is stored in MongoDB.

### 5. Wallet and activity
After successful payment:
- a wallet transaction is recorded
- an activity log entry is created

### 6. Car management
Employees can add and remove cars from the system and assign them to pickup points.

## Environment Variables

Create a `.env` file in the project root and add the following:

```env
SECRET_KEY=your_secret_key_here
MONGODB_URI=your_mongodb_connection_string_here
```

Example:

```env
SECRET_KEY=drivex_secret_key
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/DriveX?retryWrites=true&w=majority
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/DriveX.git
cd DriveX
```

### 2. Create a virtual environment

**Windows**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file and add your `SECRET_KEY` and `MONGODB_URI`.

### 5. Run the application

```bash
python app.py
```

The app should now be running at:

```bash
http://127.0.0.1:5000
```

## Important Routes

| Route | Method | Description |
|---|---|---|
| `/` | GET | Home page |
| `/register` | GET, POST | Register as user, employee, or admin |
| `/login` | GET, POST | Login page |
| `/user_dashboard` | GET | User dashboard |
| `/employee_dashboard` | GET, POST | Employee dashboard and car management |
| `/route` | GET | Ride selection page |
| `/select_car` | POST | Store selected car and route in session |
| `/payment` | GET, POST | Payment and booking flow |
| `/wallet` | GET | User wallet history |
| `/activity` | GET | User ride activity history |
| `/search_car` | POST | Search cars |
| `/calculate_distance` | POST | Calculate route distance and price |
| `/logout` | POST | Logout current user |
| `/init_db` | GET | Initialize default pickup points |

## Database Collections

The application currently uses the following MongoDB collections:

- `user`
- `employee`
- `admin`
- `cars`
- `pickup_points`
- `wallet`
- `activity`
- `bookings`

## Screens / Pages

- Home page
- Registration page
- Login page
- User dashboard
- Route selection page
- Payment page
- Wallet page
- Activity page
- Employee dashboard

## Notes

- The current application logic uses **MongoDB**, not MySQL.
- The included `.env.example` may need updating to match the current MongoDB-based implementation.
- The project also contains older files such as `drivex.sql` and `instance/local.db`, but the active app logic in `app.py` uses MongoDB through PyMongo.

## Future Improvements

- Dedicated admin dashboard
- Better validation and error handling
- Booking cancellation flow
- Ride status tracking in real time
- Payment gateway integration
- Better role-based access separation
- Responsive UI refinements
- Deployment-ready production configuration

## Author

**Samiul Alim**

If you are using this project for learning or academic work, feel free to fork it and customize it further.

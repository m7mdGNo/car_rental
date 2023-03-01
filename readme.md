
# Car Rental Web App

This is a web application for car rental services built with Django Web Framework. It allows users to browse available cars, make reservations, and process payments via Stripe, 
and companies to add cars .

## Demo

https://carbook.m7mdgno.me/



## Features

- User authentication: users can create accounts, log in.
- Browse cars: users can browse available cars in specific location and in specific date range and choose the best price.
- Make reservations: users can reserver a car by filling out a form.
- Payment processing: users can pay for their reservations using Stripe Payment Gateway.
- Blog: administrators can add blogs.
- Companies : companies can create accounts ,log in, and add cars.
- Admin dashboard: administrators can log in and access a dashboard to manage cars, reservations, users and companies.


## Installation
Clone the repository:

```bash
$ git clone https://github.com/m7mdGNo/car_rental.git
$ cd car_rental
```


### Create a virtual environment and activate it:

```bash
$ python3 -m venv env
$ source env/bin/activate
```

### Install the dependencies:

```bash
$ pip install -r requirements.txt
```

### create postgres database
```bash
$ sudo apt-get install python3-dev libpq-dev postgresql postgresql-contrib
$ sudo su - postgres
$ psql
$ create database <database_name>;
$ create role <name> with encrypted password <'password'>;
$ alter role <name> with LOGIN;
$ grant all on DATABASE <db_name> to <role_name>;
```

### Create a .env file in the root directory with the following environment variables:

see .env.example in the root directory and replace these values with real values
```makefile
SECRET_KEY=secret-key
DEBUG=True
DATABASE_URL=psql://postgres:<password>@localhost:<password>/<db_name>
STATIC_URL=/static/
STATIC_ROOT=static/
MEDIA_URL=/media/
MEDIA_ROOT=media/
ALLOWED_HOSTS=*
STRIPE_PUBLIC_KEY=kkk
STRIPE_SECRET_KEY=kkk
DOMAIN=127.0.0.1:8000
STRIPE_ENDPOINT_SECRET=fff
```
### Run the migrations:

```Copy code
$ python manage.py migrate
```

### Run the development server:

```Copy code
$ python manage.py runserver
```

Open the web browser and go to http://localhost:8000.

### create administrators user
```Copy code
$ python manage.py createsuperuser
```

Open the web browser and go to http://localhost:8000/admin.


## Usage
- Register a new user account or log in as an existing user.

- for users click on profile icon in navbar then signup a new account.

- for companies click on company icon in navbar then register new company.

- click on company icon in navbar and add some cars.

- Choose a pick-up date and return date for the reservation.

- Browse available cars and select a car to reserve.

- fill a reaservation form to complete reservation.

- Enter payment information and complete the checkout process.

- View reservations on the user profile (profile icon in navbar) and cancel or modify them as necessary.

- Log in as an administrator to access the admin dashboard and manage cars, reservations, and users.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
This project is licensed under the MIT License.
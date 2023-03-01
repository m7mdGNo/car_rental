
First, make sure that you have Python 3 installed on your system. After downloading the project directory, open a terminal window (or command prompt) and navigate to the project's directory. Then type pip install -r requirements.txt and press Enter. This will install all the necessary packages needed to run the project.

Once the packages are installed, type python manage.py migrate and press Enter. This will create the database objects in the local DB so that they can be accessed by the application.

Finally, if you need to start the server, type python manage.py runserver and press Enter. You should see something like "Running on http://127.0.0.1:8000/". You can now open your web browser and access the project by opening the URL http://127.0.0.1:8000/ in the address bar.
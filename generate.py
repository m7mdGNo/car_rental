# Import the models
from main.models import Car_Brand, Brand_Model, Car,Car_imgs
from users.models import User

# create a list of real car brands
brands = [
    'Audi', 'BMW', 'Chevrolet', 'Ford', 'Honda', 'Hyundai', 'Kia', 'Mazda',
    'Mercedes-Benz', 'Nissan', 'Porsche', 'Subaru', 'Tesla', 'Toyota', 'Volkswagen'
]

# loop through the list of brands and create a new Car_Brand object for each one
for brand in brands:
    Car_Brand.objects.create(name=brand)

from django.core.files import File
from urllib.request import urlopen
from tempfile import NamedTemporaryFile
import random

# create three brands
brand1 = Car_Brand.objects.create(name='Toyota')
brand2 = Car_Brand.objects.create(name='Ford')
brand3 = Car_Brand.objects.create(name='BMW')

# create three brand models
model1 = Brand_Model.objects.create(
    brand=brand1, name='Camry', year='2022', color='Red',
    transmission=Brand_Model.TransmissionChoices.AUTOMATIC,
    fuel=Brand_Model.FuelChoices.PETROL, seats=5, luggage=2
)
model2 = Brand_Model.objects.create(
    brand=brand2, name='Explorer', year='2023', color='Blue',
    transmission=Brand_Model.TransmissionChoices.AUTOMATIC,
    fuel=Brand_Model.FuelChoices.PETROL, seats=7, luggage=3
)
model3 = Brand_Model.objects.create(
    brand=brand3, name='X5', year='2021', color='Black',
    transmission=Brand_Model.TransmissionChoices.AUTOMATIC,
    fuel=Brand_Model.FuelChoices.DIESEL, seats=5, luggage=2
)

# create two cars for each model
for model in [model1, model2, model3]:
    for i in range(2):
        # choose a random user as the owner
        owner = User.objects.first()
        # download a random image as the car image
        img_url = 'https://picsum.photos/400/300'
        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(urlopen(img_url).read())
        img_temp.flush()
        # create the car
        Car.objects.create(
            owner=owner, brand_model=model,
            plate_number=f'ABC123{i}',
            description='Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
            mileage=random.randint(1000, 100000),
            price=random.randint(30, 100) * 1000,
            added_at='2022-02-15 00:00:00',
        )




from main.models import Car, Brand_Model, Car_Brand

# Delete all cars
Car.objects.all().delete()

# Delete all brand models
Brand_Model.objects.all().delete()

# Delete all car brands
Car_Brand.objects.all().delete()




from main.models import Car_Brand, Brand_Model, Car


brands = [
    'Audi', 'BMW', 'Chevrolet', 'Ford', 'Honda', 'Hyundai', 'Kia', 'Mazda',
    'Mercedes-Benz', 'Nissan', 'Porsche', 'Subaru', 'Tesla', 'Toyota', 'Volkswagen'
]




for i in brands:
    Car_Brand.objects.create(name=i)
    
    


import requests
import random
from main.models import Car_Brand, Brand_Model, Car


# Replace with your own Edmunds API key
API_KEY = "ar355ajjgkz5pxxv5g3dfakx"

# List of car brands
brands = [
    'Audi', 'BMW', 'Chevrolet', 'Ford', 'Honda', 'Hyundai', 'Kia', 'Mazda',
    'Mercedes-Benz', 'Nissan', 'Porsche', 'Subaru', 'Tesla', 'Toyota', 'Volkswagen'
]

for brand_name in brands:
    # Make a request to the Edmunds API for car models for this brand
    url = f"https://api.edmunds.com/api/vehicle/v2/{brand_name}/models?fmt=json&api_key={API_KEY}"
    response = requests.get(url)
    data = response.json()

    # Create a Car_Brand instance for this brand
    brand = Car_Brand.objects.create(name=brand_name)
    
    # Create a Brand_Model instance for each car model returned by the API
    for model in data["models"]:
        name = model["name"]
        year = model["years"][-1]["year"]
        color = "N/A"
        transmission = random.choice(['manual','automatic'])
        fuel = 'petrol'
        seats = 5
        luggage = 6
        
        model = Brand_Model.objects.create(
            brand=brand,
            name=name,
            year=year,
            color=color,
            transmission=transmission,
            fuel=fuel,
            seats=seats,
            luggage=luggage
        )
        
        
        
        
        
        
        
        
        
        
from main.models import Car_Brand, Brand_Model, Car,Car_imgs
from users.models import User   
        
for i in range(9):
    brand = Car_Brand.objects.create(name=f"brand{i}")
    
    for _ in range(2):
        brand_model = Brand_Model.objects.create(brand=brand, name=f'brand_model {i}_{_}', year='2023', color='Blue',
                        transmission=Brand_Model.TransmissionChoices.AUTOMATIC,
                        fuel=Brand_Model.FuelChoices.PETROL, seats=7, luggage=3)
        for car in range(2):
            car = Car.objects.create(owner=User.objects.first(), brand_model=brand_model,
                                    plate_number=f'ABC123{i}',
                                    description='Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
                                    mileage=random.randint(1000, 100000),
                                    price=random.randint(30, 100),
                                    added_at='2022-02-15 00:00:00',)
            car_imgs = Car_imgs.objects.create(
                car=car,
                img = 'x6.jpg'
            )
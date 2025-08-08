from django.shortcuts import render
from django.http import HttpResponse
import requests
import datetime
from django.conf import settings


def home(request):
    city = request.POST.get('city', 'indore').strip()  # Default to 'indore' if not provided
    print(f'City received: {city}')

    #search engine for our image
    API_KEY = 'AIzaSyC6hsNkNvAzMgLyvJs8v6Vou5C-2uxRywk'
    SEARCH_ENGINE_ID = '573f90398fb2c44ca'

    query = city+ "1920*1080"
    page = 1
    start = (page-1) * 10 + 1
    searchType = 'image'
    city_url =f'https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}&searchType={searchType}&imgSize=xlarge'

    data = requests.get(city_url).json()
    count= 1
    search_items = data.get("items", [])
    image_url = search_items[1]["link"] if len(search_items) > 1 else None


    try:
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={settings.OPENWEATHER_API_KEY}'
        PARAMS = {'units': 'metric'}
        response = requests.get(url, params=PARAMS)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        data = response.json()
        print(data)

        # Check if required data exists
        if not all(key in data for key in ['weather', 'main']):
            raise ValueError("Invalid API response structure")

        description = data['weather'][0]['description']
        icon = data['weather'][0]['icon']
        temp = data['main']['temp']

    except (requests.RequestException, KeyError, ValueError) as e:
        # Fallback values or error message
        description = "clear sky"
        icon = "01d"  # Default clear sky icon
        temp = 21.9
        error_message = f"Couldn't fetch weather data: {str(e)}"
    else:
        error_message = None

    day = datetime.date.today()


    return render(request, 'index.html', {
        'description': description,
        'icon': icon,
        'temp': temp,
        'day': day,
        'city': city.capitalize(),  # Capitalize for display
        'error_message': error_message,
        'image_url': image_url
    })
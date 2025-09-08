from django.shortcuts import render

from .forms import CityForm
from .models import City
import requests
from django.contrib import messages
# Create your views here.
def home(request):
    Url="http://api.openweathermap.org/data/2.5/weather?q={},&appid=0db552203a2ffa54187aa852da8b41b5&units=metric"
    form=CityForm()
    if request.method=='POST':
        form=CityForm(request.POST)
        if form.is_valid():
            NCity=form.cleaned_data['name']
            CCity=City.objects.filter(name=NCity).count()
            print(CCity)
            if CCity==0:
                res=requests.get(Url.format(NCity)).json()
                if res['cod']==200:
                    form.save()
                    messages.success(request, "City Added Successfully!")
                else:
                    messages.error(request, "City Doesn't Exist!")

            else:
                messages.error(request, "City Already Exists!")
    form=CityForm()
    cities=City.objects.all()
    data=[]
    for city in cities:
        res=requests.get(Url.format(city)).json()
        print(res)
        city_weather={
            'city':city,
            'temperature':res['main']['temp'],
            'description':res['weather'][0]['description'],
            'country':res['sys']['country'],
            'humidity':res['main']['humidity'],
            'icon':res['weather'][0]['icon'],
        }
        data.append(city_weather)
    context={'data':data,'form':form}

    return render(request, 'WeatherApp.html',context)

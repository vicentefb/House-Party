"""music_controller URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')), # Whatever the url is dispatch/send it over to api.urls
    path('', include('frontend.urls')), # Whenever we type a url that's not api or admin we send it to frontend.urls
    path('spotify/', include('spotify.urls'))
]


# command to run the server: python .\manage.py runserver
# commands to run anytime we make changes to models or database:
#           python .\manage.py makemigrations
#           python .\manage.py migrate
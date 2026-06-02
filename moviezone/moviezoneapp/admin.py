from django.contrib import admin
from .models import Customer,Category, Movie, Favorite

admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Movie)
admin.site.register(Favorite)
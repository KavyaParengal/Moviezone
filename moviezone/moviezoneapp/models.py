from django.db import models

class Customer(models.Model):
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.username

class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Movie(models.Model):
    title = models.CharField(max_length=200)
    poster = models.ImageField(upload_to='movies/')
    description = models.TextField()
    release_date = models.DateField()
    actors = models.CharField(max_length=300)
    rating = models.FloatField(default=0.0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(Customer,on_delete=models.CASCADE)
    trailer_link = models.URLField()

    def __str__(self):
        return self.title
    
class Favorite(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'movie')  # prevent duplicates

    def __str__(self):
        return f"{self.movie.title} by {self.user.username}"

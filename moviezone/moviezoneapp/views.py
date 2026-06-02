from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer, Category, Movie, Favorite
from django.contrib import messages
from django.contrib.auth import authenticate, login

def register_user(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('register_user')

        if Customer.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register_user')

        if Customer.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('register_user')
        
        user = Customer.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )
        messages.success(request, "Account created successfully")
        return redirect('login_user')
    return render(request, 'register.html')

def login_user(request):
    if request.session.get('user_id'):
        return redirect('home')   
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = Customer.objects.filter(username=username, password=password).first()

        if user:
            request.session['user_id'] = user.id
            request.session['username'] = user.username

            messages.success(request, "Login successful")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login_user')
    return render(request, 'login.html')

def home_display(request):
    if not request.session.get('user_id'):
        return redirect('login_user')
    query = request.GET.get('q')
    user_id = request.session.get('user_id')
    fav_ids = Favorite.objects.filter(user_id=user_id).values_list('movie_id', flat=True)
    if query:
        movies = Movie.objects.filter(title__icontains=query)
    else:
        movies = Movie.objects.all()
    context = {
        'movies': movies,
        # 'carousel_movies': carousel_movies,
        "fav_ids": fav_ids,
        'query': query
    }
    return render(request,"home.html", context)

def profile_view(request):
    if not request.session.get('user_id'):
        return redirect('login_user')
    user = Customer.objects.get(id=request.session['user_id'])
    messages.error(request, "")
    messages.success(request, "")
    return render(request, 'profile.html', {'user': user})

def profile_edit(request):
    if not request.session.get('user_id'):
        return redirect('login_user')

    user = Customer.objects.get(id=request.session['user_id'])
    print(user)
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        print(first_name)
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        if Customer.objects.exclude(id=user.id).filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('profile_edit')
        if Customer.objects.exclude(id=user.id).filter(email=email).exists():
            messages.error(request,"Email already exists")
            return redirect('profile_edit')
        user.first_name=first_name
        user.last_name=last_name
        user.email=email
        user.username=username
        user.save()
        messages.success(request, "Profile updated successfully")
        return redirect('profile_edit')

    return render(request, 'profile.html', {'user': user})

def add_movies(request):
    if not request.session.get('user_id'):
        return redirect('login_user')
    user = Customer.objects.get(id=request.session['user_id'])
    categories = Category.objects.all()
    if request.method=='POST':
        title=request.POST.get('title')
        poster=request.FILES.get('poster')
        description=request.POST.get('description')
        release_date=request.POST.get('release_date')
        actors=request.POST.get('actors')
        rating=request.POST.get('rating')
        category_id=request.POST.get('category')
        trailer_link=request.POST.get('trailer_link')

        category = Category.objects.get(id=category_id)

        Movie.objects.create(
            title=title,
            poster=poster,
            description=description,
            release_date=release_date,
            actors=actors,
            rating=rating,
            category=category,
            trailer_link=trailer_link,
            user=user
        )
        return redirect("home")
    return render(request,"add_movies.html",{'categories': categories})

def toggle_favorite(request, movie_id):
    if not request.session.get('user_id'):
        return redirect('login_user')
    user_id = request.session['user_id']
    movie = get_object_or_404(Movie, id=movie_id)
    favorite = Favorite.objects.filter(user_id=user_id, movie=movie).first()
    if favorite:
        favorite.delete()
    else:
        Favorite.objects.create(user_id=user_id, movie=movie)
    # Go back to the Same page (home OR favorites)
    return redirect(request.META.get('HTTP_REFERER', 'home'))

def favorite_display(request):
    if not request.session.get('user_id'):
        return redirect('login_user')
    user_id = request.session.get('user_id')
    query = request.GET.get('q')
    # Get favorite movie IDs
    fav_ids = Favorite.objects.filter(user_id=user_id).values_list('movie_id', flat=True)
    # Filter ONLY favorite movies
    movies = Movie.objects.filter(id__in=fav_ids)
    # Search inside favorites only
    if query:
        movies = movies.filter(title__icontains=query)
    context = {
        'movies': movies,
        'fav_ids': fav_ids,
        'query': query
    }
    return render(request, "favorite_list.html", context)

def single_user_movies(request):
    if not request.session.get('user_id'):
        return redirect('login_user')
    user_id = request.session['user_id']
    movies = Movie.objects.filter(user=user_id)
    query = request.GET.get('q')
    if query:
        movies = movies.filter(title__icontains=query)
    context = {
        'movies': movies,
        'query': query
    }
    return render(request, "single_user_movies.html", context)

def edit_movie(request, movie_id):
    if not request.session.get('user_id'):
        return redirect('login_user')
    movie = get_object_or_404(Movie, id=movie_id)
    categories = Category.objects.all()
    if request.method == "POST":
        category_id=request.POST.get('category')
        category = Category.objects.get(id=category_id)

        movie.title = request.POST.get('title')
        movie.description = request.POST.get('description')
        movie.release_date = request.POST.get('release_date')
        movie.actors = request.POST.get('actors')
        movie.trailer_link = request.POST.get('trailer_link')
        movie.rating = request.POST.get('rating')
        movie.category = category
        
        movie.save()
        return redirect('single_user_movies')
    return render(request, "edit_movies.html", {"movie": movie, "categories":categories})

def delete_movie(request, movie_id):
    if not request.session.get('user_id'):
        return redirect('login_user')
    movie = get_object_or_404(Movie, id=movie_id)
    movie.delete()
    return redirect('single_user_movies')

def logout_user(request):
    request.session.flush()   #clear session
    messages.success(request, "Logout successful")
    return redirect('login_user')
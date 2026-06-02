from django.urls import path
from .import views

urlpatterns = [
    path("",views.register_user,name="register_user"),
    path("login-user/",views.login_user,name="login_user"),
    path("logout/",views.logout_user,name="logout_user"),

    path("home-page/",views.home_display,name="home"),

    path("profile/",views.profile_view,name="profile_view"),
    path("profile-edit/",views.profile_edit,name="profile_edit"),

    path("add-movies/",views.add_movies,name="add_movies"),
    path('toggle-favorite/<int:movie_id>/', views.toggle_favorite, name='toggle_favorite'),
    path("favorite-movie-list/", views.favorite_display, name="favorite_display"),

    path("single-user-movies/", views.single_user_movies,name="single_user_movies"),
    path('edit-movie/<int:movie_id>/', views.edit_movie, name='edit_movie'),
    path('delete-movie/<int:movie_id>/', views.delete_movie, name='delete_movie'),
]
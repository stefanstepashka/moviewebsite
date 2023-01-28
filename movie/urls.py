from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from movie_app import views
from movie_app.views import SignUpView, LoginView, LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('movies/', views.show_all_movies, name='movies'),
    path('movies/<int:id_mov>', views.one_movie, name='one_movie'),
    path('directors/', views.all_directors, name='directors'),
    path('directors/<int:id_dir>', views.one_director, name='one_director'),
    path('actors/', views.all_actors, name='actors'),
    path('actors/<int:id_act>', views.one_actor, name='one_actors'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('personal', views.personal_cabinet, name='personal'),
    path('add_to_favorites/', views.add_to_personal, name='add_to_favorites'),
    path('favorites/', views.favorites, name='favorites'),
    path('cinema-detail/<int:cinema_id>', views.cinema_detail, name='cinema-detail'),
    path('reserve-seat/<int:cinema_id>/<int:seat_id>', views.reserve_seat, name='reserve_seat'),
    path('my_reservations/', views.my_reservations, name='my_reservations'),
    path('cancel_reservation/<int:reservation_id>', views.cancel_reservation, name='cancel_reservation'),
]+ static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)\
              + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


from django.urls import path

from users import views

urlpatterns = [
    path('me', views.MyProfileView.as_view()),
    path('me/fbv', views.my_profile_fbv),
]

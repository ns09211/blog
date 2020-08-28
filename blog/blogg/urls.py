

from django.urls import path
from . import views


urlpatterns = [

    path('',views.home,name="home"),


    path('contact/',views.contact,name="contact"),
    path('about/',views.about,name="about"),
    path('blogpost/',views.blogpost,name="blogpost"),
    path('search/',views.search,name="search"),
    path('logout/',views.handlelogout,name="logout"),
    path('signup/',views.signup,name="signup"),
    path('login/',views.handlelogin,name="login"),
    path('comment/',views.postcomment,name="comment"),
path('<str:slug>/',views.blog,name="blog"),





]

from django.urls import path
from blogs import views
from.views import category

urlpatterns = [
    path('',views.home,name="home"),
    path('blog/<slug:url>',views.trans, name="trans"),
    path('category/<slug:url>',category),
    path('contact/',views.contact,name="contact"),
    path('about/',views.about,name='about'),
    path('Search/', views.Search, name='Search'),
    path('subscribe/', views.subscriber_user, name='subscribe'),
    path('notes/', views.notes, name="notes"),
    path('notecategory/<slug:url>/', views.dox_details, name="dox_details"),
]

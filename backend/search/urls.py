from django.urls import path, include
import search.views as views
urlpatterns = [
    path("search", views.search),
    path("autocomplete/<short_query>",views.autocomplete),
    path("details",views.details),
]

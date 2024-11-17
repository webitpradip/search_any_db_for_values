from django.urls import path
from .views import SearchView

app_name = 'search_app'

urlpatterns = [
    path('', SearchView.as_view(), name='search'),  # Root URL for the search interface
]
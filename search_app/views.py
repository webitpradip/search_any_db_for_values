from django.shortcuts import render
from django.views import View
from django.contrib import messages

from .forms import DatabaseConnectionForm, SearchForm
from .db_utils import DatabaseConnector, DatabaseSearcher

class SearchView(View):
    template_name = 'search_app/search.html'
    
    def get(self, request):
        """Display the database connection and search forms"""
        context = {
            'connection_form': DatabaseConnectionForm(),
            'search_form': SearchForm(),
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        """Handle database connection and search"""
        connection_form = DatabaseConnectionForm(request.POST)
        search_form = SearchForm(request.POST)
        
        context = {
            'connection_form': connection_form,
            'search_form': search_form,
        }
        
        if connection_form.is_valid() and search_form.is_valid():
            try:
                # Get form data
                db_type = connection_form.cleaned_data['database_type']
                credentials = {
                    'host': connection_form.cleaned_data['host'],
                    'database': connection_form.cleaned_data['database'],
                    'username': connection_form.cleaned_data['username'],
                    'password': connection_form.cleaned_data['password'],
                }
                search_value = search_form.cleaned_data['search_value']

                # Establish database connection
                connection = DatabaseConnector.get_connection(db_type, credentials)
                
                # Perform search
                results = DatabaseSearcher.search_all_tables(connection, db_type, search_value)

                # Close connection for SQL databases (not MongoDB)
                if db_type.lower() != 'mongodb':
                    connection.close()
                
                context['results'] = results
                context['search_performed'] = True
                
            except Exception as e:
                messages.error(request, f"Error: {str(e)}")
        
        return render(request, self.template_name, context)

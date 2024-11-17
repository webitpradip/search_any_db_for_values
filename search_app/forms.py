from django import forms

class DatabaseConnectionForm(forms.Form):
    """Form for database connection details"""
    
    DATABASE_CHOICES = [
        ('mysql', 'MySQL'),
        ('postgresql', 'PostgreSQL'),
        ('mongodb', 'MongoDB'),
        ('sqlserver', 'SQL Server'),
        ('sqlite', 'SQLite'),
    ]
    
    database_type = forms.ChoiceField(
        choices=DATABASE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    host = forms.CharField(
        required=False,  # Not required for SQLite
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'localhost'
        })
    )
    
    database = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Database name or path for SQLite'
        })
    )
    
    username = forms.CharField(
        required=False,  # Not required for SQLite
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        })
    )
    
    password = forms.CharField(
        required=False,  # Made optional for all database types
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password (optional)'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        db_type = cleaned_data.get('database_type')
        
        # SQLite only requires database path
        if db_type == 'sqlite':
            return cleaned_data
            
        # For other databases, validate required fields (excluding password)
        required_fields = ['host', 'database', 'username']
        for field in required_fields:
            if not cleaned_data.get(field):
                self.add_error(field, f'{field.title()} is required for {db_type}')
        
        return cleaned_data

class SearchForm(forms.Form):
    """Form for search functionality"""
    
    search_value = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter search value...'
        })
    )
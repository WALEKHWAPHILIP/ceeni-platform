from django.urls import path
from apps.ceeni_documents.views.api import search_api
from apps.ceeni_documents.views.ui import search_htmx  # Import HTMX-enhanced UI search view

# Define the application namespace for URL reversing and namespacing
app_name = "ceeni_documents"

# URL patterns for the ceeni_documents app
urlpatterns = [
    # API endpoint for document search
    # Maps GET requests at 'api/search/' to the search_api view function,
    # which returns JSON-formatted semantic search results.
    path("api/search/", search_api, name="documents_search_api"),

    # UI endpoint for document search powered by HTMX
    # Maps GET requests at 'ui/search/' to the search_htmx view function,
    # which renders an HTML partial with search results for dynamic page updates.
    path("ui/search/", search_htmx, name="documents_search_htmx"),
]

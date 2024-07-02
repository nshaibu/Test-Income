from django.urls import path

from api import views
from .swagger_schema import SwaggerSchemaView

app_name = "api"

urlpatterns = [
    path("docs/", SwaggerSchemaView.as_view(), name="docs"),
    path("salary/details", views.UserSalaryDetailView.as_view(), name="index"),
]

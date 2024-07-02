from django.urls import path, include

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.schemas import SchemaGenerator
from rest_framework.views import APIView
from rest_framework_swagger import renderers

from . import views

ROOT_URl = "/api/"


class SwaggerSchemaView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [renderers.OpenAPIRenderer, renderers.SwaggerUIRenderer]
    config = {
        "title": "Income API",
        "description": "Salary Income API",
        "url": ROOT_URl,
        "patterns": [
            path("salary/details", views.UserSalaryDetailView.as_view(), name="index"),
        ],
    }

    def get(self, request):
        generator = SchemaGenerator(**self.config)
        schema = generator.get_schema(request=request, public=True)
        return Response(schema)

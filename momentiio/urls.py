from django.conf.urls.static import static
from django.conf import settings
from graphene_file_upload.django import FileUploadGraphQLView
from django.views.decorators.csrf import csrf_exempt
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', csrf_exempt(FileUploadGraphQLView.as_view(graphiql=True))),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^facebook/', TemplateView.as_view(template_name="template.html"))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.conf.urls.static import static
from django.conf import settings
from graphene_file_upload.django import FileUploadGraphQLView
from django.views.decorators.csrf import csrf_exempt
from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', csrf_exempt(FileUploadGraphQLView.as_view(graphiql=True))),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

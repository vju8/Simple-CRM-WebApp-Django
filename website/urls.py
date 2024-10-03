from django.urls import path
from . import views 
from django.conf import settings
from django.conf.urls.static import static

# create urls
urlpatterns = [
    path("", views.home, name='home'),
    # path("login/", views.login_user, name='login'),
    path("logout/", views.logout_user, name='logout'),
    path("register/", views.register_user, name='register'),
    path("record/<int:pk>", views.customer_record, name='record'),
    path("delete_record/<int:pk>", views.delete_record, name='delete_record'),
    path("add_record/", views.add_record, name='add_record'),
    path("update_record/<int:pk>/", views.update_record, name='update_record'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
from django.urls import path

from . import views
from .check_system import do_checks

urlpatterns = [
    path('', views.index_organilab, name='index'),
    path('tutorial/<int:org_pk>', views.index_tutorial, name='tutorials'),
    path('donate', views.donate, name='donate'),
    path('donate_success', views.donate_success, name='donate_success'),
    path('feedback', views.FeedbackView.as_view(), name='feedback'),
    path('check_ok', do_checks, name="check_ok")
]

"""web_app URL configuration"""
from django.urls import path

from .views import home_view
from .views import about_view
from .views import contact_page_view
from .views import comment_remove_view
from .views import my_bot_projects_view
from .views import my_resume_download_view
from .views import my_projects_view
from .views import CertificateListView, CertificateDetailView

urlpatterns = [

    path('', home_view, name='home'),
    path('about-my-self/', about_view, name='about-my-self'),
    path('about-my-self/<str:pk>/', comment_remove_view, name='about-my-self-comment-remove'), # noqa
    path('download-resume/', my_resume_download_view, name='download-resume'),
    path('my-projects/', my_projects_view, name='my-projects'),
    path('my-projects-bot/', my_bot_projects_view, name='my-projects-bot'),
    path('contact-me/', contact_page_view, name='contact-me'),
    path('certificates/', CertificateListView.as_view(), name='certificate_list_page'), # noqa
    path('certificates/<slug:slug>/', CertificateDetailView.as_view(), name='certificate_detail_page'), # noqa
]

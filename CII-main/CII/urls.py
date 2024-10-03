"""CII URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from main import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('profile/', views.profile, name='profile'),
    path('myapplications/', views.student_applications, name='student_applications'),
    path('myapplications/<str:pk>/delete/', views.delete_application, name='delete_application'),
    path('contact/', views.contact, name='contact'),
    path('openings/', views.openings, name='openings'),
    #  path('/', views.consent, name='apply'),
    path('openings/<str:pk>/delete/', views.deleteopening, name='deleteopening'),
    path('consultancies/', views.consultancies, name='consultancies'),
    path('consultancies/<str:pk>/details/',views.consultancy_details, name='consultancy_details'),
    # path('openings/details/', views.details, name='details'),
    path('openings/<str:pk>/<str:ic>/details/', views.details, name='details'),
    # path('openings/<str:pk>/<str:ic>/apply/', views.consent, name='apply'),
    path('industries/', views.industries, name='industry'),
    path('industries/industry_details/', views.industry_details, name='industry_details'),
    path('industries/industry_registration/', views.industry_registration, name='industry_registration'),
    path('industry-api/', views.industry_data, name="industry_api"),
    path('institutes/', views.institutes, name='institute'),
    path('institutes/institutes_details/', views.institute_details, name='institute_details'),
    path('institutes/institute_registration/', views.institute_registration, name='institute_registration'),
    path('institute-api/', views.institute_data, name="institute_api"),
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('dashboard/', views.send_mails, name='send_mails'),
    path('login/institute_dashboard/<str:pk>/',views.institute_dashboard, name='institute_dashboard'),
    path('institute_dashboard/<str:pk>/studentlist/',views.institute_student_list,name = 'institute_student_list'),
    path('institute_dashboard/<str:pk>/internship/manage',views.manage_institute_internship,name = 'manage_institute_internship'),
    path('institute_dashboard/<str:pk>/openings',views.view_openings,name = 'view_openings'),
    path('institute_dashboard/<str:pk>/openings/<str:ic>/details',views.openings_details,name = 'openings_details'),
    path('institute_dashboard/<str:pk>/openings/<str:ic>/apply',views.apply_openings,name = 'apply_openings'),
    path('institute_dashboard/<str:pk>/openings/<str:ic>/apply/consent',views.consent_,name = 'consent'),
    path('institute_dashboard/<str:pk>/openings/<str:ic>/apply/application',views.application,name = 'application'),
    path('dashboard/<str:pk>/', views.dashboard, name='dashboard'),
    path('dashboard/<str:pk>/studentlist/', views.student_list, name='internship'),
    path('dashboard/<str:pk>/studentlist/<str:ic>/institutes', views.institutes_applied, name='institutes_applied'),
    path('dashboard/<str:pk>/studentlist/<str:ic>/students/<str:op>', views.students_applied, name='students_applied'),
    path('dashboard/<str:pk>/internship/manage', views.manage_internship, name='manageinternship'),
    path('dashboard/<str:pk>/internship/manage/add', views.add_internship, name='addinternship'),
    # path('institute_dashboard/studentlist/',views.get_excel,name = 'excel_form')     
    ] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)



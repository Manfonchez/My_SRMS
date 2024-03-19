from django.urls import path
from studentmanagement.views import *
from .views import SearchView
from django.contrib.auth import views as auth_views
from .forms import *


urlpatterns = [
    path('register/', registerPage, name="registerPage"),
   # path('activate/<uidb64>/<token>/', activate, name="activate"),
    path('login/', loginPage, name="loginPage"),
    path('logout/', logoutUser, name="logout"), 

    path('', home, name="home"),
    path('contact/', contact, name="contact"),
    path('email_received/', email_received, name="email_received"),
    path('about/', about, name="about"),
    
    path('dashboard/', dashboard, name="dashboard"),
    path('delete_students/<str:pk>/', delete_students, name="delete_students"),
    path('update_fees/<str:pk>/', update_fees, name="update_fees"),
    path('update_cert/<str:pk>/', update_cert, name="update_cert"),
    path('update_exam_results/<str:pk>/', update_exam_results, name="update_exam_results"),
    path('student_details/<str:pk>/', student_details, name="student_details"),
    
    path('student_page/', student_page, name="student_page"),
    path('account_settings/', account_settings, name="account_settings"),
    path('delete_profile/', delete_profile, name="delete_profile"),

# PASSWORD RESET URL PATHS
    # This path is for the change password function for an already logged in user
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name="password_change_form.html", form_class = pwdChangeForm), name="password_change"),
    path('password_change_done/', auth_views.PasswordChangeView.as_view(template_name="password_change_done.html"), name="password_change_done"),
    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name="password_reset.html"), name="reset_password"),

    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
        template_name="password_reset_sent.html"), name="password_reset_done"),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="password_reset_form.html"), name="password_reset_confirm"),

    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name="password_reset_done.html"), name="password_reset_complete"),


    # Search 
    path('search/', SearchView.as_view(), name='search'),
]

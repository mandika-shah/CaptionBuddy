from django.urls import path
from caption_generator import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login1, name='login'),
    path('signup', views.signup, name='signup'),
    path('index', views.index, name='index'),
    path('forgot_password/', auth_views.PasswordResetView.as_view(template_name='forgot_password.html'), name='forgot_password'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name ='reset_complete.html'), name='password_reset_complete'),
    path('logout/', views.logout1, name='logout'),
    path('verify/<uidb64>/<token>/', views.VerificationView.as_view(), name='verify_email'),
    path('popup/<int:pk>/',views.show_popup, name='show_popup'),
    path('dashboard', views.user_dashboard, name='dashboard'),
    path('save_data/', views.view_saved_data, name='save_data'),

]

handler404 = 'caption_generator.views.handler404'
handler500 = 'caption_generator.views.handler500'





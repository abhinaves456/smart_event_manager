from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='eventapp/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('', views.dashboard_view, name='dashboard'),

    # NEW URL: For booking tickets. The <int:event_id> part is a variable.
    path('book/<int:event_id>/', views.book_ticket_view, name='book_ticket'),
]
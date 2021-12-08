from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', login_required(views.DetailView.as_view()), name='detail'),
    path('<int:pk>/results/', login_required(views.ResultsView.as_view()), name='results'),
    path('<int:question_id>/vote/', login_required(views.vote), name='vote'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', login_required(views.LogoutView.as_view()), name='logout'),
    path('profile/', login_required(views.ProfileView.as_view()), name='profile'),
    path('<int:pk>/edit/', login_required(views.EditAccView.as_view()), name='edit'),
    path('<int:pk>/delete/', login_required(views.DeleteAccView.as_view()), name='delete')
]

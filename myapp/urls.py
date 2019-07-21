from myapp import views
from django.urls import path


urlpatterns=[
    path('post/', views.post, name='post'),
    path('<int:myapp_id>/',views.detail,name='detail'),
    path('show/', views.show, name='show'),
    path('<int:pk>/edit/', views.edit, name='edit'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('signup/',views.signup, name='signup'),
    path('signin/',views.signin, name='signin'),
    path('signout/',views.signout, name='signout'),
    
] 
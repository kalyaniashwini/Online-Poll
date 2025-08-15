from django.urls import path
from . import views

app_name = 'polls'

urlpatterns = [
    path('', views.polls_list, name='list'),
    path('mine/', views.list_by_user, name='list_by_user'),
    path('add/', views.polls_add, name='add'),
    path('<int:poll_id>/edit/', views.polls_edit, name='edit'),
    path('<int:poll_id>/delete/', views.polls_delete, name='delete'),
    path('<int:poll_id>/', views.poll_detail, name='detail'),
    path('<int:poll_id>/vote/', views.poll_vote, name='vote'),
    path('<int:poll_id>/end/', views.endpoll, name='end'),
    path('choice/<int:choice_id>/edit/', views.choice_edit, name='choice_edit'),
    path('choice/<int:choice_id>/delete/', views.choice_delete, name='choice_delete'),
    path('<int:poll_id>/choice/add/', views.add_choice, name='choice_add'),
]

from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
# ex: /polls/
path ('',views.IndexView.as_view(),name='index'),
# user poll list
path ('user/<str:username>',views.UserIndexView.as_view(),name='user-index'),
# ex: /polls/5/
path('<int:pk>/', views.DetailView.as_view(), name='detail'),
# ex: /polls/5/results/
path('<int:pk>/results/', views.ResultsView.as_view() , name='results'),
# To creaete new poll
path('polls/new/', views.createview, name='create'),
# To edit poll
path('<int:pk>/edit', views.editview, name='edit'),
# To delete poll
path('<int:question_id>/delete', views.deleteview, name='delete'),
# ex: /polls/5/vote/
path('<int:question_id>/vote/', views.vote , name='vote'),

]


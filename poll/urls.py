from django.urls import path
from . import views

urlpatterns = [
    # Poll Management endpoints
    path('', views.PollListCreateView.as_view(), name='poll-list-create'),
    path('my-polls/', views.UserPollListView.as_view(), name='user-poll-list'),
    path('<int:pk>/', views.PollDetailsView.as_view(), name='poll-details'),
    path('<int:pk>/delete/', views.PollDeleteView.as_view(), name='poll-delete'),
    path('<int:pk>/toogle-visibility/', views.toogle_poll_visibility, name='toogle-visiblity'),
    # Voting endpoints
    path('<int:pk>/vote/', views.VoteCreateView.as_view(), name='vote-create'),
    
    # Results endpoints
    path('<int:pk>/results/', views.PollResultView.as_view(), name='poll-results'),
]

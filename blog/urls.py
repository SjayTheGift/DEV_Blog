from django.urls import path
from .views import PostList, PostDetailsView

urlpatterns = [
    path('', PostList.as_view(), name='posts'),
    path('post/<slug:slug>/', PostDetailsView.as_view(), name='post_detail'),
]

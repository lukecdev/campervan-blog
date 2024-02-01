from . import views
from django.urls import path
from .views import PostCreateView
from .views import UpdatePostView
from .views import DeletePostView



urlpatterns = [
    path("", views.landing_page, name="landing_page"),
    path('posts/', views.PostList.as_view(), name="posts"),
    path('create_post/', PostCreateView.as_view(), name='create_post'),
    path('update_post/<slug:slug>', UpdatePostView.as_view(), name='update_post'),
    path('delete_post/<slug:slug>/delete', DeletePostView.as_view(), name='delete_post'),
    path('/<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('like/<slug:slug>', views.PostLike.as_view(), name='post_like'),
    path('profile/', views.profile, name ='profile'),
]

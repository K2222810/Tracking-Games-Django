from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('games/', views.GameListView.as_view(), name='game-list'),
    path('games/create/', views.GameCreate.as_view(), name='game-create'),
    path('games/<int:pk>/edit/', views.GameUpdate.as_view(), name='game-update'),
    path('games/<int:pk>/delete/', views.GameDelete.as_view(), name='game-delete'),
    path('games/<int:pk>/', views.GameDetailView.as_view(), name='game-detail'),
    path('games/<int:pk>/progress/', views.add_progress, name='game-add-progress'),
    path('games/progress/<int:pk>/edit/', views.edit_progress, name='game-edit-progress'),
    path('games/progress/<int:pk>/delete/', views.delete_progress, name='game-delete-progress'),
    path('games/<int:pk>/reviews/add/', views.add_review, name='game-add-review'),
    path('games/reviews/<int:pk>/delete/', views.delete_review, name='game-delete-review'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/toggle/<int:pk>/', views.wishlist_toggle, name='wishlist-toggle'),
]

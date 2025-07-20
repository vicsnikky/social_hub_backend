from django.urls import path
from .views import ChatListView, ChatCreateView

urlpatterns = [
    path('<int:user_id>/', ChatListView.as_view(), name='chat-list'),
    path('<int:user_id>/send/', ChatCreateView.as_view(), name='chat-send'),
]

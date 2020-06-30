from django.urls import path
from .views import registration, Login, Logout, FilterUser, UserBookmarks, account, Password_reset, Password_reset_done,\
    Password_reset_confirm, Password_reset_complete, user_stats

urlpatterns = [
    path('registration/', registration, name='registration'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('account/', account, name='account'),
    path('filter/', FilterUser.as_view(), name='filter_user'),
    path('bookmarks/', UserBookmarks.as_view(), name='user_bookmarks'),
    path('password/reset/', Password_reset.as_view(), name='password_reset'),
    path('password/reset/done/', Password_reset_done.as_view(), name='password_reset_done'),
    path('password/reset/confirm/<uidb64>/<token>/', Password_reset_confirm.as_view(), name='password_reset_confirm'),
    path('password/reset/complete/', Password_reset_complete.as_view(), name='password_reset_complete'),
    path('account/<str:username>/stats/', user_stats, name='user_stats')
]

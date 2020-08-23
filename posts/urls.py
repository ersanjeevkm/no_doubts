from django.urls import path
from .views import PostList, PostDetail, CreatePost, EditPost, DeletePost, UserPost, CreateReply, EditReply, \
    DeleteReply, CreateAnswer, EditAnswer, DeleteAnswer, UserReply, UserAnswer, CategoryView, QuestionsSearchView, filter_page, \
    bookmark_post, remove_bookmark, verify_answer, undo_verification, like_answer, like_question, dislike_question, \
    dislike_answer

urlpatterns = [
    path('', PostList.as_view(), name='home'),
    path('post/create/', CreatePost.as_view(), name='create_post'),
    path('post/search/', QuestionsSearchView.as_view(), name='question_search'),
    path('post/<slug>/', PostDetail.as_view(), name='post_detail'),
    path('post/edit/<slug>/', EditPost.as_view(), name='edit_post'),
    path('post/delete/<slug>/', DeletePost.as_view(), name='delete_post'),
    path('post/view/<str:username>/', UserPost.as_view(), name='user_post'),
    path('post/<slug>/reply/', CreateReply.as_view(), name='create_reply'),
    path('post/reply/<int:pk>/edit/', EditReply.as_view(), name='edit_reply'),
    path('post/<slug>/reply/<int:pk>/delete/', DeleteReply.as_view(), name='delete_reply'),
    path('post/<slug>/answer/create/', CreateAnswer.as_view(), name='create_answer'),
    path('post/answer/edit/<slug>/', EditAnswer.as_view(), name='edit_answer'),
    path('post/<qslug>/answer/delete/<slug>/', DeleteAnswer.as_view(), name='delete_answer'),
    path('post/answer/view/<str:username>/', UserAnswer.as_view(), name='user_answer'),
    path('post/reply/view/<str:username>/', UserReply.as_view(), name='user_reply'),
    path('post/view/category/<str:category>/', CategoryView.as_view(), name='category_view'),
    path('filters/', filter_page, name='filter'),
    path('post/<slug>/bookmark/', bookmark_post, name='bookmark_post'),
    path('post/<slug>/remove_bookmark/', remove_bookmark, name='remove_bookmark'),
    path('post/answer/<slug>/accept/', verify_answer, name='verify_answer'),
    path('post/answer/<slug>/accept/remove/', undo_verification, name='undo_verification'),
    path('post/answer/<slug>/like/', like_answer, name='like_answer'),
    path('post/question/<slug>/like/', like_question, name='like_question'),
    path('post/question/<slug>/dislike/', dislike_question, name='dislike_question'),
    path('post/answer/<slug>/dislike/', dislike_answer, name='dislike_answer')
]

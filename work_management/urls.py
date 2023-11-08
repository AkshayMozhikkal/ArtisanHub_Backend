
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', Work_Posts.as_view(), name='Works_Posted'),
    path('new_post/', New_Work.as_view(), name='Post_Work'),
    path('single_work/<int:id>', Single_Work.as_view(), name='Single_Work'),
    path('my_works/<int:id>', My_Works.as_view() , name='My_Works'),
    path('delete_work/<int:id>', Delete_Work.as_view() , name='Delete_Work'),
    path('new_comment/', New_Comment.as_view() , name='new_comment'),
    path('delete_comment/<int:id>', Delete_Comment.as_view() , name='delete_comment'),
    path('new_like/', New_Like.as_view() , name='new_like'),
    path('remove_like/', Remove_Like.as_view() , name='remove_like'),
    path('search_posts/<str:value>', Search_Work_Posts.as_view() , name='search_posts'),
    path('post_count/<int:year>/<int:month>', MonthlyPostCountView.as_view() , name='post_count'),
]
 
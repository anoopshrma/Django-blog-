from django.conf.urls import url
from blog import views
app_name='blog'
urlpatterns = [
    url(r'^$',views.PostList.as_view(),name='post_list'),
    url(r'^post/(?P<pk>\d+)/$',views.PostDetail.as_view(),name='post_detail'),
    url(r'^post/new/$',views.CreatePostView.as_view(),name='post_new'),
    url(r'^post/(?P<pk>\d+)/edit/$',views.UpdatePostView.as_view(),name='post_update'),
    url(r'^post/(?P<pk>\d+)/remove/$',views.DeletePostView.as_view(),name='post_delete'),
    url(r'^draft/$', views.DraftPostView.as_view(),name='post_draft'),
    url(r'^post/(?P<pk>\d+)/publish/$',views.post_publish,name='post_publish'),
    url(r'^post/(?P<pk>\d+)/comment/$',views.add_comment_to_post,name='add_comment_to_post'),
    url(r'^comment/(?P<pk>\d+)/approve/$',views.comment_approve,name='comment_approve'),
    url(r'^comment/(?P<pk>\d+)/remove/$',views.comment_delete,name='comment_delete'),
    url(r'^about/$',views.AboutView.as_view(),name='about')

]
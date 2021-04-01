from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [
    path("", views.index, name="home"),
    path("login/", views.loginView, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logoutView, name="logout"),
    path("profile/<int:id>/", views.profileView, name="profile"),
    path("following/", views.followingView, name="following"),
    path("like-post/<int:id>/", views.likePostView, name="likePost"),
    path("delete-post/<int:id>/", views.deletePost, name="deletePost"),
    path("edit-post/<int:id>/", views.editPost, name="editPost"),
    path("follow/<int:id>/", views.follow, name="follow"),
    path('profile/<int:id>/password-rest/', views.passwordReset, name='passwordRest'),
    path("like-comment/<int:id>/", views.likeCommentView, name="likeComment"),

]


# if settings.DEBUG: 
#         urlpatterns += static(settings.MEDIA_URL, 
#                             document_root=settings.MEDIA_ROOT)
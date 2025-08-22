from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from posts.views import home, post_list_view, post_detail, post_create_view, post_create_model_form_view
from user.views import register_view, login_view, logout_view, profile_view

users_patterns = [
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("profile/", profile_view, name="profile"),  # 👈 без username
]

posts_patterns = [
    path("", home, name="home"),
    path("i18n/", include("django.conf.urls.i18n")),
    path("admin/", admin.site.urls),
    path("posts/", post_list_view, name="post_list"),
    path("posts/<int:post_id>/", post_detail, name="post_detail"),
    path("posts/create/", post_create_view, name="post_create"),
    path("posts/create_model_form/", post_create_model_form_view, name="post_create_model_form"),
]

urlpatterns = users_patterns + posts_patterns + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)

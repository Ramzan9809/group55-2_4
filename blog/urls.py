from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

# Users CBV
from user.views import RegisterView, LoginView, LogoutView, ProfileView, PostUpdateView

# Posts CBV
from posts.views import HomeView, PostListView, PostDetailView, PostCreateView, PostCreateModelFormView

urlpatterns = [
    # Users
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("posts/<int:pk>/update/", PostUpdateView.as_view(), name="post_update"),

    # Posts
    path("", HomeView.as_view(), name="home"),
    path("posts/", PostListView.as_view(), name="post_list"),
    path("posts/create/", PostCreateView.as_view(), name="post_create"),
    path("posts/create_model_form/", PostCreateModelFormView.as_view(), name="post_create_model_form"),
    path("posts/<int:pk>/", PostDetailView.as_view(), name="post_detail"),

    # Admin & i18n
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
]

# Статика и медиа
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

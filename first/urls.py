"""first URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from main.views import CategoryListView, DepartmentImageView, DepartmentsViewSet, ReplyViewSet, ProblemViewSet, \
    CommentViewSet, LikesViewSet, RatingViewSet, FavoriteViewSet

router = DefaultRouter()
router.register('department', DepartmentsViewSet)
router.register('problems', ProblemViewSet)
router.register('replies', ReplyViewSet)
router.register('comments', CommentViewSet)
router.register('likes', LikesViewSet)
router.register('rating', RatingViewSet)
router.register('favorite', FavoriteViewSet)

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/categories/', CategoryListView.as_view()),
    path('api/v1/add-image/', DepartmentImageView.as_view()),
    path('api/v1/account/', include('account.urls')),
    path('api/v1/', include(router.urls)),
    path('', schema_view.with_ui()),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

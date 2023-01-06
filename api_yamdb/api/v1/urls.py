from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.v1.views.reviews import (CategoryViewSet, CommentViewSet,
                                  GenreViewSet, ReviewViewSet, TitleViewSet)
from api.v1.views.users import UserViewSet, email_check, signup

router = DefaultRouter()

router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'titles', TitleViewSet, basename='titles')
router.register(r'users', UserViewSet, basename='users')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/signup/', signup, name='auth_signup'),
    path('auth/token/', email_check, name='auth_token'),
]

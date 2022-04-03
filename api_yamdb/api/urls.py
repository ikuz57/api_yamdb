from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (CategoriesViewSet, GenresViewSet, TitlesViewSet,
                    ReviewViewset, CommentViewset)

app_name = 'api'

router = DefaultRouter()

router.register('categories', CategoriesViewSet)
router.register('genres', GenresViewSet)
router.register('titles', TitlesViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewset,
    basename='review'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewset,
    basename='comment'
)

urlpatterns = [
    path('v1/', include(router.urls)),
]

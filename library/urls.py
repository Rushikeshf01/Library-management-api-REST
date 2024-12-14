from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

router = DefaultRouter()
router.register('books', views.BookViewSet)
router.register('members', views.MemberViewSet)
router.register('loans', views.LoanViewSet)

urlpatterns = [
    path('loans/return/<int:pk>/', views.BookReturnView.as_view(), name='book_return_view'),
    path('', include(router.urls)),
    path('token/', views.MyCustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
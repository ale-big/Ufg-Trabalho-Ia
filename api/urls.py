from django.urls import path
from .views import SentimentAnalysisView, CartRecoveryView

urlpatterns = [
    path('sentiment/', SentimentAnalysisView.as_view(), name='sentiment-analysis'),
    path('cart-recovery/', CartRecoveryView.as_view(), name='cart-recovery'),
]

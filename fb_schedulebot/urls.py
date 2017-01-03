from django.conf.urls import include, url
from .views import ScheduleBotView

urlpatterns = [
	url(r'^webhook/?$', ScheduleBotView.as_view()) 
]
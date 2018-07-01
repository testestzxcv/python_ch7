from django.urls import path
from . import views

# 서버로 요청이 들어오면 누가 처리할 것인지 담당자를 정해주는 코드
# 앞부분이 주소, 뒷부분이 누가 처리할 것인지를 의미
urlpatterns = [
    path(r'^$', views.index),
]

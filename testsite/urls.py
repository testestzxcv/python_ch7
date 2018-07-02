from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

from elections import views as ev

# 서버로 요청이 들어오면 누가 처리할 것인지 담당자를 정해주는 코드
# 앞부분이 주소, 뒷부분이 누가 처리할 것인지를 의미
# urlpatterns - 서버에 요청이 들어온 경우, 담당자를 지정하는 역할. url(주소, 주소에 접속하면 실행될 명령어)
app_name = 'elections'
urlpatterns = [
    # localhost:8000 으로 연결될 경우에 ev.index 에서 처리해라 라는 의미
    path('', ev.index, name='home'),  # ev.index 에 해당하는 url을  이름(name)을 이용해서 쉽게 가져올수 있다.
    path('admin/', admin.site.urls),
    path('areas/<area>/', ev.areas),
    path('areas/<area>/results', ev.results),
    path('polls/<poll_id>/', ev.polls),
    path('candidates/<name>/', ev.candidates),
    # url(r'^areas/(?P<area>.+)/$', ev.areas),
    # url(r'^polls/(?P<poll_id>\d+)/$', ev.polls),
]

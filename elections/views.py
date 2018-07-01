from django.shortcuts import render
from django.http import HttpResponse

from .models import Candidate, Poll2, Choice4

import datetime

# Create your views here.

# 페이지 요청에 대해서 http응답 해주는 코드
# def index(request):
#     candidates = Candidate.objects.all()    # candidates 는 모든 Candidate 의 row를 DB에서 불러와서 가지고 있게 된다.
#     str = ''
#     for candidate in candidates:    # candidates의 내용을 한줄씩 불러온다.
#         str += "<p>{} 기호{}번({})<br>".format(candidate.name, candidate.party_numbeer, candidate.area)  # 내용은 html이다.
#         str += candidate.introduction+"</p>"
#     return HttpResponse(str)


def index(request):
    candidates = Candidate.objects.all()    # candidates 는 모든 Candidate 의 row를 DB에서 불러와서 가지고 있게 된다.
    context = {'candidates':candidates}     # 정보를 전달하려면 딕셔너리를 하나 만들어야 한다. html에 저장되어 있는 정적인 정보를 DB에서 데이터를 불러와서 html에 동적으로 적용시키는 작업.
    return render(request, 'elections/index.html', context)  # HttpResponse 반복에 대한 단축 코드. render 함수는 request 객체를 첫번째 인자로, 템플릿 이름을 두번째 인자로 받습니다. 그리고 세번째 인자는 선택적으로써, 템플릿에 전달할 딕셔너리입니다. render() 함수는 주어진 템플릿과 딕셔너리로 렌더링된 결과를 HttpResponse 객체로 리턴합니다.
    # 1. DB를 불러와서 -> 2. Context에 넣어서 -> 3. html 파일로 전달 ->
    # 4. html 파일에서는 context 에 들어있는 candidates 를 불러서 이용할수가 있다.


def areas(request, area):
    today = datetime.datetime.now()
    try:
        poll = Poll2.objects.get(area = area, start_date__lte=today, end_date__gte=today)
        candidates = Candidate.objects.filter(area = area)  # 앞의 area는 Candidate의 area를 의미하고 뒤의 area는 매개변수로 받아온 area를 의미한다. Candidate 에서 지역구가 매개변수로 받아온 값과 같은 값만 필터해서 가져오라는 의미.
    except:
        poll = None
        candidates = None
    context = {'candidates': candidates, 'area': area, 'poll': poll}   # 후보와 지역에 대한 정보가 담긴다
    return render(request, 'elections/area.html', context)  # html 파일을 수정해서 데이터를 사용해야 한다.


def polls(request, poll_id):
    poll = Poll2.objects.get(pk=poll_id)
    selection = request.POST['choice']  #html 에 name 으로 정의되어 있다.

    try:
        choice = Choice4.objects.get(poll_id = poll_id, candidate_id = selection)
        choice.votes += 1
        choice.save()
    except:
        choice = Choice4(poll_id = poll_id, candidate_id = selection,  votes=1)
        choice.save()

    return HttpResponse("finish")
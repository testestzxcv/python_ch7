from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, Http404

from .models import Candidate, Poll2, Choice4

import datetime
from django.db.models import Sum

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

def candidates(request, name):
    candidate = get_object_or_404(Candidate, name = name)    # 오브젝트를 가져오거나 아니면 404를 발생시켜라 라는 의미
    # try:
    #     candidate = Candidate.objects.get(name = name)  # url이 저장되어있지 않으면 이부분에서 불러올수 없기때문에 에러난다.
    # except:
    #     # return HttpResponseNotFound("없는 페이지 입니다.")
    #     raise Http404
    return HttpResponse(candidate.name)


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

    return HttpResponseRedirect("/areas/{}/results".format(poll.area))


def results(request, area):
    candidates = Candidate.objects.filter(area = area)
    polls = Poll2.objects.filter(area = area)
    poll_results = []   # 한번한번의 투표의 결과를 리스트에 넣어준다.
    for poll in polls:
        result = {}
        result['start_date'] = poll.start_date
        result['end_date'] = poll.end_date
        total_votes = Choice4.objects.filter(poll_id = poll.id).aggregate(Sum('votes')) # 숫자를 넘겨주는게 아니라 딕셔너리를 넘겨준다.
        result['total_votes'] = total_votes['votes__sum']
        rates = []
        for candidate in candidates:
            try:
                choice = Choice4.objects.get(poll_id = poll.id,
                                             candidate_id = candidate.id)
                rates.append(round(choice.votes * 100 /result['total_votes'], 1))
            except:
                rates.append(0)
        result['rates'] = rates
        poll_results.append(result)

    context = {'candidates':candidates, 'area':area,
               'poll_results' : poll_results}
    return render(request, 'elections/result.html', context)
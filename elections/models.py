from django.db import models

# (후보들의) 정보를 담을수 있는 공간, 장고에서는 모델이라고 한다.
# Create your models here.
class Candidate(models.Model):
    name = models.CharField(max_length=10)
    introduction = models.TextField()
    area = models.CharField(max_length=15)
    party_numbeer = models.IntegerField(default=0)  # 기본값은 1부터 시작.

    def __str__(self):  # 이클래스를 표현할때 어떻게 표현할지에 대한 내용
        return self.name    # 이 클래스를 표현할때는 후보자의 이름으로 표현한다. 브라우저를 확인하면 DB에 저장된 이름이 항목에 표시된다.


class Poll2(models.Model):
    start_date = models.DateTimeField() # 조사를 시작하는 시간
    end_date = models.DateTimeField() # 조사를 종료하는 시간
    area = models.CharField(max_length=15)  # 지역
    # id는 모델을 만들면 자동으로 생성된다.


class Choice4(models.Model):
    # 다른 클래스를 사용할때 ForeignKey 를 사용한다. 인수로 on_delete 넣어줘야한다.
    poll = models.ForeignKey(Poll2, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    votes = models.IntegerField(default=0)

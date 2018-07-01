from django.contrib import admin

from .models import Candidate, Poll2, Choice4
# Register your models here.

admin.site.register(Candidate) # 여기에 등록하면 localhost:8000/admin 브라우저 항목에 추가된다.
admin.site.register(Poll2)
admin.site.register(Choice4)

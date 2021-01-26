from django.shortcuts import render, get_object_or_404
from django.utils import timezone

# Create your views here.
from django.http import HttpResponse
from .models import Question



def index(request):
    # 작성 일시 역순으로 데이터 조회
    question_list = Question.objects.order_by('-create_date')
    context = {'question_list': question_list}
    return render(request, 'pybo/question_list.html', context)

def detail(request, question_id):
    # get_object_or_404 함수는 모델의 기본키를 이용하여 모델 객체 한 건을 반환
    question = get_object_or_404(Question, pk=question_id) # pk에 해당하는 건이 없으면 404 페이지 반환
    context = {'question' : question}
    return render(request, 'pybo/question_detail.html', context)

def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())
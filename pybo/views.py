from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

# Create your views here.
from django.http import HttpResponse
from .forms import QuestionForm, AnswerForm
from .models import Question


def index(request):
    # 입력 파라미터
    page = request.GET.get('page', 1)  # default page 1

    # 작성 일시 역순으로 데이터 조회
    question_list = Question.objects.order_by('-create_date')

    # pagination
    paginator = Paginator(question_list, 10)  # per page 10
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj}
    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    # get_object_or_404 함수는 모델의 기본키를 이용하여 모델 객체 한 건을 반환
    question = get_object_or_404(Question, pk=question_id)  # pk에 해당하는 건이 없으면 404 페이지 반환
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)


@login_required(login_url='common:login')
def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user  # 답변 글쓴이는 현재 로그인한 계정
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question_id)
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)

    # Answer 모델이 Question 모델을 Foreign Key로 참조하고 있으므로 question.answer_set 표현을 사용할 수 있다.
    # 하나의 질문에 여러개의 answer(답변)이 달릴 수 있음, 질문에 달린 답변은 set 을 통하여 답변 세트를 조회.
    # Answer 모델을 직접 사용하여 데이터를 저장할 수도 있다.
    # answer = Answer(question=question, content=request.POST.get('content'), create_date=timezone.now())
    # question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())


@login_required(login_url='common:login')
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)  # commit=False -> 임시저장
            question.author = request.user
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)
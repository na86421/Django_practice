from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .forms import QuestionForm, AnswerForm
from django.core.paginator import Paginator

# Create your views here.
from django.http import HttpResponse
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


def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())
    return redirect('pybo:detail', question_id=question_id)


def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)  # commit=False -> 임시저장
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)


def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question_id)
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)

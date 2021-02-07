from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from ..models import Question


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
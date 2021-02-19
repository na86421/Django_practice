from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from ..models import Question


def index(request):
    # 입력 파라미터
    page = request.GET.get('page', 1)  # default page 1
    kw = request.GET.get('kw', '')  # 검색어

    # 작성 일시 역순으로 데이터 조회
    question_list = Question.objects.order_by('-create_date')
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목검색
            Q(content__icontains=kw) |  # 내용검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이검색
        ).distinct()

    # pagination
    paginator = Paginator(question_list, 10)  # per page 10
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj, 'page': page, 'kw': kw}
    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    # get_object_or_404 함수는 모델의 기본키를 이용하여 모델 객체 한 건을 반환
    question = get_object_or_404(Question, pk=question_id)  # pk에 해당하는 건이 없으면 404 페이지 반환
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)

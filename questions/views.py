from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
# from .forms import QuestionForm
from questions.forms import QuestionForm

from django.core.paginator import Paginator
# from django.shortcuts import render
# from .models import Question
from taggit.models import Tag

from django.http import JsonResponse
from django.views import View
from voting.models import Vote
from .models import Question, Answer


@login_required
def question_list(request):
    questions = Question.objects.all().order_by('-created_at')
    paginator = Paginator(questions, 5)  # 5 per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    related_tags = Tag.objects.filter(taggit_taggeditem_items__object_id__in=questions.values_list('id', flat=True)).distinct()
    other_tags = Tag.objects.exclude(id__in=related_tags).distinct()

    return render(request, 'questions/question_list.html', {
        'page_obj': page_obj,
        'related_tags': related_tags[:10],
        'other_tags': other_tags[:10]
    })

@login_required
def question_create(request):
    if request.method == 'POST':
        print("Request POST data:", request.POST)  # Debugging line
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()
            form.save_m2m()
            return redirect('question_list')
    else:
        form = QuestionForm()
    return render(request, 'questions/question_form.html', {'form': form})


@login_required
def question_edit(request, pk):
    question = get_object_or_404(Question, pk=pk, user=request.user)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('question_list')
    else:
        form = QuestionForm(instance=question)
    return render(request, 'questions/question_form.html', {'form': form})

@login_required
def question_delete(request, pk):
    question = get_object_or_404(Question, pk=pk, user=request.user)
    if request.method == 'POST':
        question.delete()
        return redirect('question_list')
    return render(request, 'questions/question_confirm_delete.html', {'question': question})

@login_required
def vote(request, pk, target):
    obj = None

    if target == "question":
        obj = get_object_or_404(Question, pk=pk)
    elif target == "answer":
        obj = get_object_or_404(Answer, pk=pk)
    else:
        return redirect("question_detail", pk=pk)

    direction = request.POST.get("direction")

    current_vote = Vote.objects.get_for_user(obj, request.user)

    if direction == "up":
        if current_vote == 1:
            Vote.objects.delete_vote(obj, request.user)  # remove upvote
        else:
            Vote.objects.record_vote(obj, request.user, +1)
    elif direction == "down":
        if current_vote == -1:
            Vote.objects.delete_vote(obj, request.user)  # remove downvote
        else:
            Vote.objects.record_vote(obj, request.user, -1)

    # Redirect to question detail
    if isinstance(obj, Answer):
        return redirect("question_detail", pk=obj.question.pk)
    return redirect("question_detail", pk=pk)



def question_detail(request, pk):
    question = get_object_or_404(
        Question.objects.select_related("user").prefetch_related("tags", "answers__user"),
        pk=pk,
    )

    # Get user's vote if authenticated
    user_vote = None
    if request.user.is_authenticated:
        user_vote = Vote.objects.get_for_user(question, request.user)

    # Handle new answer submission
    if request.method == "POST" and request.POST.get("action") == "add_answer":
        if request.user.is_authenticated:
            detail = request.POST.get("detail", "").strip()
            if detail:
                Answer.objects.create(user=request.user, question=question, detail=detail)
        return redirect("question_detail", pk=pk)

    # Get vote score
    vote_score = Vote.objects.get_score(question)

    return render(request, "questions/question_detail.html", {
        "question": question,
        "vote_score": vote_score,
        "user_vote": user_vote,
    })



class TagAutocompleteView(View):
    """
    Return JSON the way Select2 expects:
    { "results": [ {"id": "python", "text": "python"}, ... ] }
    """
    def get(self, request, *args, **kwargs):
        term = request.GET.get("term", "")     # Select2 uses 'term'
        qs = Tag.objects.filter(name__icontains=term).values_list("name", flat=True).distinct()[:10]
        data = [{"id": tag, "text": tag} for tag in qs]
        return JsonResponse({"results": data})
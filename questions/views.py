from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Question
# from .forms import QuestionForm
from questions.forms import QuestionForm


@login_required
def question_list(request):
    questions = Question.objects.filter(user=request.user)
    return render(request, 'questions/question_list.html', {'questions': questions})

@login_required
def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk, user=request.user)
    return render(request, 'questions/question_detail.html', {'question': question})

@login_required
def question_create(request):
    if request.method == 'POST':
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

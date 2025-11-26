from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views import generic
from django.contrib import messages
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import QuestionForm

from .models import Question, Choice, Vote
from .forms import RegistrationForm, ProfileUpdateForm

User = get_user_model()


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        now = timezone.now()
        if self.request.user.is_staff:
            return Question.objects.order_by('-pub_date')
        return Question.objects.filter(expires_at__isnull=True, pub_date__lte=now).order_by('-pub_date')

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = self.get_object()

        if self.request.user.is_authenticated:
            context['has_voted'] = Vote.objects.filter(user=self.request.user, question=question).exists()
        else:
            context['has_voted'] = False

        return context

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = self.get_object()

        total_votes = sum(choice.votes for choice in question.choice_set.all())

        choices_with_percent = []
        for choice in question.choice_set.all():
            if total_votes > 0:
                percent = (choice.votes / total_votes) * 100
            else:
                percent = 0
            choices_with_percent.append({
                'choice': choice,
                'percent': round(percent, 2)
            })

        context['choices_with_percent'] = choices_with_percent
        context['total_votes'] = total_votes
        return context

@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if Vote.objects.filter(user=request.user, question=question).exists():
        messages.error(request, "Вы уже голосовали за этот вопрос.")
        return redirect('polls:detail', pk=question_id)

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': 'вы не сделали выбор'
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()

        Vote.objects.create(user=request.user, choice=selected_choice, question=question)
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('polls:index')
    else:
        form = RegistrationForm()

    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile_detail(request):
    user = request.user
    return render(request, 'registration/profile_detail.html', {'user': user})


@login_required
def profile_update(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлён!')
            return redirect('polls:profile_detail')
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'registration/profile_update.html', {'form': form})


@login_required
def profile_delete(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, 'Профиль успешно удалён!')
        return redirect('polls:index')

    return render(request, 'registration/profile_delete.html')


from .forms import QuestionForm, ChoiceFormSet

@login_required  
def create_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES)
        formset = ChoiceFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()

            formset.instance = question
            formset.save()

            messages.success(request, 'Опрос успешно создан!')
            return redirect('polls:detail', pk=question.pk)
    else:
        form = QuestionForm()
        formset = ChoiceFormSet()

    return render(request, 'polls/create_question.html', {
        'form': form,
        'formset': formset,
    })
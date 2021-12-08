import datetime

from django.contrib.auth import views
from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView, TemplateView, UpdateView, DeleteView

from .forms import RegisterForm
from .models import Question, Choice, SomeUser
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.views import generic, View


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date').filter(
            pub_date__range=[datetime.datetime.now() - datetime.timedelta(days=30), datetime.datetime.now()]
        )

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['description'] = Question.objects.all().values_list('description')
        return context


class LoginView(views.LoginView):
    template_name = 'polls/login.html'

    def get_redirect_url(self):
        return reverse('polls:index')



class RegisterView(CreateView):
    template_name = 'polls/register.html'
    model = User
    form_class = RegisterForm
    success_url = reverse_lazy('polls:login')


class LogoutView(views.LogoutView):
    template_name = 'polls/logout.html'

    def get_success_url(self):
        return reverse_lazy('polls:index')


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

    def get_context_data(self, **kwargs):

        context = super(ResultsView, self).get_context_data(**kwargs)
        context['votes'] = Choice.objects.all().filter(question_id=self.kwargs['pk']).aggregate(Sum('votes'))
        return context


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': 'вы не сделали выбор'
        })
    else:
        if Question.objects.filter(id=question.id).filter(voted_users=request.user).exists():
            return render(request, 'polls/detail.html', {
                'question': question,
                'error_message': 'вы уже проголосовали'
            })
        else:
            question.voted_users.add(request.user)
            selected_choice.votes += 1
            selected_choice.save()
            return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


class ProfileView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'polls/profile.html')


class EditAccView(UpdateView):
    model = SomeUser
    template_name = 'polls/edit.html'
    fields = (
        'username',
        'img'
    )

    def get_success_url(self):
        return reverse_lazy('polls:profile')


class DeleteAccView(DeleteView):
    model = SomeUser
    template_name = 'polls/delete.html'

    def get_object(self, **kwargs):
        pk = self.kwargs.get(self.pk_url_kwarg)
        user = SomeUser.objects.get(pk=pk)
        return user

    def get_success_url(self):
        return reverse_lazy('polls:profile')

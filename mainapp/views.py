"""views for mainapp"""
from django.views.generic import ListView, DetailView
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .forms import RecruitCreateForm
from .models import Answers, Question, Quiz, Recruit, Sith, Task


def main(request):
    """render main page"""
    page_title = "Main page"
    context = {
        'page_title': page_title,
    }
    return render(request, 'mainapp/index.html', context=context)

def profile(request):
    """render form of recruit's data"""
    page_title = 'Recruit profile'
    if request.method == 'POST':
        form = RecruitCreateForm(request.POST)
        if form.is_valid():
            recruit = form.save(commit=False)
            recruit.save()
            # make task with quiz of questions, then render form for quiz
            task = recruit.make_task()
            return HttpResponseRedirect(reverse('test', kwargs={'pk': task.id}))
    else:
        form = RecruitCreateForm()

    context = {
        'page_title': page_title,
        'form': form
    }
    return render(request, 'mainapp/profile.html', context)

def add_task(request, pk):
    """add new task for current recruit"""
    recruit = get_object_or_404(Recruit, pk=pk)
    task = recruit.make_task()
    return HttpResponseRedirect(reverse('test', kwargs={'pk': task.id}))

def test(request, pk):
    """
    create and render task for recruit
    :param request:
    :param pk: id of task
    :return render:
    """
    page_title = 'Recruit test'
    recruit_task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        versions = list(map(lambda x: int(x), list(request.POST.values())[1:]))
        recruit_task.check_done(versions)
        return HttpResponseRedirect(reverse('info', kwargs={'pk': recruit_task.recruit_id}))
    else:
        context = {
            'page_title': page_title,
            'task': recruit_task
        }
        return render(request, 'mainapp/test.html', context)

def info(request, pk):
    page_title = 'Recruit info'
    recruit = get_object_or_404(Recruit, pk=pk)
    context = {
        'page_title': page_title,
        'recruit': recruit
    }
    return render(request, 'mainapp/info.html', context)


class SithList(ListView):
    model = Sith


class SithDetail(DetailView):
    model = Sith

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recruits'] = Recruit.objects.all()
        return context

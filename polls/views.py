from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, Http404 
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from .models import Choice, Question
from django.views import generic
from django.utils import timezone
from django.contrib.auth.models import User
from .forms import QuestionCreateForm, ChoiceCreateForm
from django.contrib.auth.decorators import login_required

class IndexView(generic.ListView):
    model = Question
    template_name = 'polls/index.html' # <app>/<model>_<viewtype>.html
    # That means you can change the original parameter name(object_list) in templates into any name 
    # through "context_object_name" for your view
    context_object_name = 'latest_question_list' 
    paginate_by = 4

    def get_queryset(self):
        # Python’s array-slicing syntax to limit your QuerySet to a certain number of results
        # In this case, we are limiting it to 5 results.
        # All enteries whose timezone is less than and equal to timezone.now().
        # This is handled by __lte . https://code.djangoproject.com/wiki/BasicComparisonFilters
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')


    
class UserIndexView(generic.ListView):
    model = Question
    template_name = 'polls/user_index.html' # <app>/<model>_<viewtype>.html
    # That means you can change the original parameter name(object_list) in templates into any name 
    # through "context_object_name" for your view
    context_object_name = 'latest_question_list' 
    paginate_by = 4

    def get_queryset(self):
        # Python’s array-slicing syntax to limit your QuerySet to a certain number of results
        # In this case, we are limiting it to 5 results.
        # All enteries whose timezone is less than and equal to timezone.now().
        # This is handled by __lte . https://code.djangoproject.com/wiki/BasicComparisonFilters
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Question.objects.filter(author=user).order_by('-pub_date')




class DetailView(generic.DetailView):    
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

 
class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


@login_required
def createview(request):
    """ Create New Poll."""
    if request.method == 'POST':
        q_form = QuestionCreateForm(request.POST)
        c_form = [ChoiceCreateForm(request.POST, prefix=str(x), instance=Choice()) for x in range(0,3)]
        
        if q_form.is_valid() and all([cf.is_valid() for cf in c_form]):
            new_q = q_form.save(commit=False)
            new_q.author = request.user
            new_q.save()
            for cf in c_form:
                new_c = cf.save(commit=False)
                new_c.question = new_q
                new_c.save() 
                
            messages.success(request, f'New Question Posted!')
            return redirect("polls:index")
    else:
        q_form = QuestionCreateForm()
        c_form = [ChoiceCreateForm(prefix=str(x), instance=Choice()) for x in range(0,3)]

    context = {
        'q_form': q_form,
        'c_form': c_form
    }

    return render (request, 'polls/question_form.html',context)


@login_required
def editview(request, pk):
    """ Edit Poll"""
    question = get_object_or_404(Question, id=pk)
    choices = question.choice_set.all()
    if request.user == question.author:
        if request.method == 'POST':
            q_form = QuestionCreateForm(request.POST, instance=question)
            c_form = [ChoiceCreateForm(request.POST, prefix=str(ch.id), instance=ch) for ch in choices]
            
            if q_form.is_valid() and all([cf.is_valid() for cf in c_form]):
                new_q = q_form.save(commit=False)
                new_q.author = request.user
                new_q.save()
                for cf in c_form:
                    new_c = cf.save(commit=False)
                    new_c.question = new_q
                    new_c.save() 
                    
                messages.success(request, f'Poll Updated!')
                return redirect("polls:index")
        else:
            q_form = QuestionCreateForm(instance=question)
            c_form = [ChoiceCreateForm(prefix=str(ch.id), instance=ch) for ch in choices]

        context = {
            'q_form': q_form,
            'c_form': c_form
        }

    else:
        return HttpResponseForbidden('403 Forbidden')
    return render (request, 'polls/question_form.html',context)


@login_required
def deleteview(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    choices = question.choice_set.all()
    if request.user == question.author and request.method == 'POST':
        Question.objects.filter(id=question_id).delete()
        for ch in choices:
            ch.delete()
        messages.success(request, f'Poll Deleted!')    
        return redirect('polls:index')    
    else:
        context = {'question': question}      
        return render (request,'polls/delete.html',context)
        # delete Question and choices



def vote(request,question_id):
    question = get_object_or_404(Question,pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, ObjectDoesNotExist): 
        return render(request,'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })   
    else:
        selected_choice.votes += 1
        selected_choice.save()
    
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
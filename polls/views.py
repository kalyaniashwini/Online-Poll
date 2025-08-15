from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib import messages
from django.http import HttpResponse
from .models import Poll, Choice, Vote
from .forms import PollAddForm, EditPollForm, ChoiceAddForm

@login_required()
def polls_list(request):
    all_polls = Poll.objects.all().order_by('-pub_date')
    search_term = ''

    if 'name' in request.GET:
        all_polls = all_polls.order_by('text')
    if 'date' in request.GET:
        all_polls = all_polls.order_by('pub_date')
    if 'vote' in request.GET:
        all_polls = all_polls.annotate(vote_count=Count('vote')).order_by('vote_count')
    if 'search' in request.GET:
        search_term = request.GET.get('search', '')
        all_polls = all_polls.filter(text__icontains=search_term)

    paginator = Paginator(all_polls, 6)
    page = request.GET.get('page')
    polls = paginator.get_page(page)
    get_dict_copy = request.GET.copy()
    params = get_dict_copy.pop('page', True) and get_dict_copy.urlencode()

    context = {'polls': polls, 'params': params, 'search_term': search_term}
    return render(request, 'polls/polls_list.html', context)

@login_required()
def list_by_user(request):
    all_polls = Poll.objects.filter(owner=request.user).order_by('-pub_date')
    paginator = Paginator(all_polls, 7)
    page = request.GET.get('page')
    polls = paginator.get_page(page)
    params = ''
    search_term = ''
    context = {'polls': polls, 'params': params, 'search_term': search_term, 'mine': True}
    return render(request, 'polls/polls_list.html', context)

'''@login_required()
def polls_add(request):
    if not request.user.has_perm('polls.add_poll'):
        # allow owners by default; for demo we allow any authenticated user to add
        pass
    if request.method == 'POST':
        form = PollAddForm(request.POST)
        if form.is_valid():
            poll = form.save(commit=False)
            poll.owner = request.user
            poll.save()
            Choice.objects.create(poll=poll, choice_text=form.cleaned_data['choice1'])
            Choice.objects.create(poll=poll, choice_text=form.cleaned_data['choice2'])
            messages.success(request, "Poll & Choices added successfully", extra_tags='alert alert-success alert-dismissible fade show')
            return redirect('polls:list')
    else:
        form = PollAddForm()
    return render(request, 'polls/add_poll.html', {'form': form})'''

@login_required()
def polls_add(request):
    if not request.user.has_perm('polls.add_poll'):
        return HttpResponse("Sorry but you don't have permission to do that!")

    if request.method == 'POST':
        form = PollAddForm(request.POST)
        # read all <input name="choices"> values
        raw_choices = request.POST.getlist('choices')
        choices = [c.strip() for c in raw_choices if c and c.strip()]

        # basic server-side validation
        errors = []
        if len(choices) < 2:
            errors.append("Please provide at least two choices.")
        # (optional) enforce uniqueness
        if len(set([c.lower() for c in choices])) != len(choices):
            errors.append("Choices must be unique.")

        if form.is_valid() and not errors:
            poll = form.save(commit=False)
            poll.owner = request.user
            poll.save()

            # bulk create choices
            Choice.objects.bulk_create([Choice(poll=poll, choice_text=c) for c in choices])

            messages.success(
                request, "Poll & choices added successfully",
                extra_tags='alert alert-success alert-dismissible fade show'
            )
            return redirect('polls:list')

        # if we get here, form invalid or errors present
        for e in errors:
            messages.error(request, e, extra_tags='alert alert-warning alert-dismissible fade show')
        return render(request, 'polls/add_poll.html', {"form": form, "posted_choices": raw_choices})

    # GET
    form = PollAddForm()
    return render(request, 'polls/add_poll.html', {"form": form})

@login_required()
def polls_edit(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.user != poll.owner:
        return redirect('home')
    if request.method == 'POST':
        form = EditPollForm(request.POST, instance=poll)
        if form.is_valid():
            form.save()
            messages.success(request, "Poll Updated successfully", extra_tags='alert alert-success alert-dismissible fade show')
            return redirect('polls:list')
    else:
        form = EditPollForm(instance=poll)
    return render(request, "polls/poll_edit.html", {'form': form, 'poll': poll})

@login_required()
def polls_delete(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.user != poll.owner:
        return redirect('home')
    poll.delete()
    messages.success(request, "Poll Deleted successfully", extra_tags='alert alert-success alert-dismissible fade show')
    return redirect("polls:list")

@login_required()
def add_choice(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.user != poll.owner:
        return redirect('home')
    if request.method == 'POST':
        form = ChoiceAddForm(request.POST)
        if form.is_valid():
            new_choice = form.save(commit=False)
            new_choice.poll = poll
            new_choice.save()
            messages.success(request, "Choice added successfully", extra_tags='alert alert-success alert-dismissible fade show')
            return redirect('polls:edit', poll.id)
    else:
        form = ChoiceAddForm()
    return render(request, 'polls/add_choice.html', {'form': form})

@login_required()
def choice_edit(request, choice_id):
    choice = get_object_or_404(Choice, pk=choice_id)
    poll = choice.poll
    if request.user != poll.owner:
        return redirect('home')
    if request.method == 'POST':
        form = ChoiceAddForm(request.POST, instance=choice)
        if form.is_valid():
            form.save()
            messages.success(request, "Choice Updated successfully", extra_tags='alert alert-success alert-dismissible fade show')
            return redirect('polls:edit', poll.id)
    else:
        form = ChoiceAddForm(instance=choice)
    return render(request, 'polls/add_choice.html', {'form': form, 'edit_choice': True, 'choice': choice})

@login_required()
def choice_delete(request, choice_id):
    choice = get_object_or_404(Choice, pk=choice_id)
    poll = choice.poll
    if request.user != poll.owner:
        return redirect('home')
    choice.delete()
    messages.success(request, "Choice Deleted successfully", extra_tags='alert alert-success alert-dismissible fade show')
    return redirect('polls:edit', poll.id)

def poll_detail(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    if not poll.active:
        return render(request, 'polls/poll_result.html', {'poll': poll})
    loop_count = poll.choice_set.count()
    context = {'poll': poll, 'loop_time': range(0, loop_count)}
    return render(request, 'polls/poll_detail.html', context)

@login_required()
def poll_vote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    choice_id = request.POST.get('choice')
    if not poll.user_can_vote(request.user):
        messages.error(request, "You already voted this poll", extra_tags='alert alert-warning alert-dismissible fade show')
        return redirect("polls:list")
    if choice_id:
        choice = get_object_or_404(Choice, id=choice_id, poll=poll)
        Vote.objects.create(user=request.user, poll=poll, choice=choice)
        return render(request, 'polls/poll_result.html', {'poll': poll})
    messages.error(request, "No choice selected", extra_tags='alert alert-warning alert-dismissible fade show')
    return redirect("polls:detail", poll_id)

@login_required()
def endpoll(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.user != poll.owner:
        return redirect('home')
    if poll.active:
        poll.active = False
        poll.save()
    return render(request, 'polls/poll_result.html', {'poll': poll})

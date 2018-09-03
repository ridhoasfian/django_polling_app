from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from .models import Poll, Choice, Vote
from django.contrib.auth.decorators import login_required
from .forms import AddPollForm, EditPollForm, AddChoiceForm, EditChoiceForm, CariPollForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
import datetime

# Create your views here. bleh bleh bleh
@login_required
def list(request):
    poll = Poll.objects.all()

    if 'abjad' in request.GET:          #teks disini maksudnya url mengandung abjad=True
        poll = poll.order_by('text')   #teks disini maksudnya artibut 'text' models Poll

    if 'pub_date' in request.GET:
        poll = poll.order_by('-pub_date') # negatif maksudnya Descending

    if 'jumlah_pemilih' in request.GET:
        poll = poll.annotate(Count('vote')).order_by('vote__count')

    if request.method == "GET" and 'cari' in request.GET:
        form = CariPollForm(request.GET)
        if form.is_valid():
            cari = form.cleaned_data['cari']
            poll = poll.filter(text__icontains=cari)
    else:
        form = CariPollForm()

    paginato = Paginator(poll, 3)
    page = request.GET.get('page')
    poll = paginato.get_page(page)

    get_dict_copy = request.GET.copy()
    params = get_dict_copy.pop('page', True) and get_dict_copy.urlencode()
    return render(request, 'polling/polling_list.html', {'poll':poll, 'params':params, 'form':form})

@login_required
def poll_detail(request, polling_id):
    poll_detail = get_object_or_404(Poll, pk=polling_id)
    user_bisa_voting = poll_detail.user_bisa_voting(request.user)
    hasil = poll_detail.get_hasil_dict()
    return render(request, 'polling/polling_detail.html', {'poll_detail':poll_detail, 'user_bisa_voting':user_bisa_voting, 'hasil':hasil})

@login_required
def add_poll(request):
    if request.method == "POST":
        form = AddPollForm(request.POST)
        if form.is_valid():
            owner = request.user
            text = form.cleaned_data['text']
            pub_date = datetime.datetime.now()
            new_poll = Poll.objects.create(owner=owner,text=text,pub_date=pub_date)
            new_poll.save()

            new_choice1 = Choice.objects.create(poll=new_poll, choice_text=form.cleaned_data['pilihan1'])
            new_choice1.save()

            new_choice2 = Choice.objects.create(poll=new_poll, choice_text=form.cleaned_data['pilihan2'])
            new_choice2.save()
            return redirect('list')
    else :
        form = AddPollForm()
    return render(request, 'polling/add_poll.html', {'form':form})


@login_required
def edit_poll(request, polling_id):
    poll = get_object_or_404(Poll, pk=polling_id)
    if request.user != poll.owner:
        return redirect('/')
    if request.method == "POST":
        form = EditPollForm(request.POST, instance=poll)
        if form.is_valid():
            form.save()
            messages.success(request, 'polling berhasil di edit !')
            return redirect('list')
    else :
        form = EditPollForm(instance=poll)
    return render(request, 'polling/edit_poll.html', {'poll':poll, 'form':form})


@login_required
def add_choice(request, polling_id):
    poll = get_object_or_404(Poll, pk=polling_id)
    if request.user != poll.owner:
        return redirect('/')
    if request.method == "POST":
        form = AddChoiceForm(request.POST)
        if form.is_valid():
            new_choice = form.save(commit=False)
            new_choice.poll = poll
            new_choice.save()
            messages.success(request, 'Berhasil menambahkan pilihan pada polling {} !'.format(poll.text))
            return redirect('list')
    else :
        form = AddChoiceForm()
    return render(request, 'polling/add_choice.html', {'form':form})

@login_required
def edit_choice(request, choice_id):
    choice = get_object_or_404(Choice, pk=choice_id)
    poll = get_object_or_404(Poll, pk=choice.poll.id)
    if request.user != poll.owner:
        return redirect('/')
    if request.method == "POST":
        form = EditChoiceForm(request.POST, instance=choice)
        if form.is_valid():
            form.save()
            messages.success(request, 'Choice dari {}, berhasil di edit !'.format(poll.text))
            return redirect('list')
    else:
        form = EditChoiceForm(instance=choice)
    return render(request, 'polling/edit_choice.html', {'form':form, 'choice':choice})


@login_required
def delete_choice(request, choice_id):
    pilihan = get_object_or_404(Choice, pk=choice_id)
    poll = get_object_or_404(Poll, pk=pilihan.poll.id)
    if request.user != poll.owner:
        return redirect('/')
    if request.method == "POST":
        pilihan.delete()
        messages.success(request, 'berhasil menghapus choice dari polling {} !'.format(poll.text))
        return redirect('list')
    return render(request, 'polling/delete_choice_confirm.html', {'choice':pilihan})


@login_required
def delete_poll(request, polling_id):
    poll = get_object_or_404(Poll, pk=polling_id)
    if request.user != poll.owner:
        return redirect('/')
    if request.method == "POST":
        poll.delete()
        messages.success(request, 'berhasil menghapus polling \'{}\' !'.format(poll.text))
        return redirect('list')
    return render(request, 'polling/delete_poll_confirm.html', {})


@login_required
def poll_vote(request, polling_id):
    poll = get_object_or_404(Poll, pk=polling_id)
    choice_id = request.POST.get('pilihan')

    if not poll.user_bisa_voting(request.user): # jika hasilnya True
        messages.error(request, 'anda sudah voting sebelumnya !!!')
        return redirect('poll_detail', polling_id)

    if request.method == "POST":
        if choice_id :
            choice = Choice.objects.get(id=choice_id)
            new_vote = Vote(user=request.user, poll=poll, choice=choice)
            new_vote.save()
        else:
            messages.error(request, 'anda belum memilih voting !')
            return redirect('poll_detail', polling_id)
        return redirect('poll_detail', polling_id)
















#

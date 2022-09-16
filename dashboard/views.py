from django.shortcuts import render,redirect
from .forms import *
from .models import *
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import generic
from youtubesearchpython import VideosSearch
import wikipedia
import re



def home(request):
    
    # web scraping
    # url = "https://corona.gov.bd/"
    # co = requests.get(url)
    # co.ok

    # text = co.text

    # text = text.replace("\n", ' ')
    # patt = re.compile(r'<b>(.*?)</b>')
    # r = re.findall(patt, text)
    # print(r)

    context = {
        'cases':0,
        'dade':10
    }
    return render(request,'dashboard/home.html',context)

@login_required
def notes(request):
    notes = Note.objects.filter(user=request.user)
    if request.method == 'POST':
        form = Note_create_form(request.POST)
        if form.is_valid():
            new_note = Note(user=request.user,title=request.POST['title'],description=request.POST['description'])
            new_note.save()
            messages.success(request,f'Note created successfilly! by {request.user.username} ')

    form = Note_create_form()


    context = {
        'notes':notes,
        'form':form,
    }
    return render(request,'dashboard/notes.html',context)
@login_required
def delete_note(request,pk):
    note = Note.objects.get(id=pk)
    note.delete()
    return redirect('notes')


class NotesDetail(generic.DetailView):
    model = Note


@login_required
def homework(request):
    homework = Homework.objects.filter(uesr=request.user)
    form = Homework_create_form()
    if request.method == 'POST':
        form = Homework_create_form(request.POST)
        if form.is_valid():
            new_homework = Homework(uesr=request.user,subject=request.POST['subject'],title=request.POST['title'],description=request.POST['description'])
            new_homework.save()
            return redirect('homework')
    context = {
        'homework': homework,
        'form': form,
    }
    return render(request,'dashboard/homework.html',context)

@login_required
def delete_homework(request,pk):
    Homework.objects.get(id=pk).delete()
    return redirect('homework')


def youtube(request):
    form = Dashboard_Search()

    if request.method == 'POST':
        form = Dashboard_Search(request.POST)
        text = request.POST['text']
        video = VideosSearch(text,limit=10)
        result_list = []
        for i in video.result()['result']:
            result_dict = {
                'input':text,
                'title': i['title'],
                'duration': i['duration'],
                'thumbnail': i['thumbnails'][0]['url'],
                'channel': i['channel']['name'],
                'link': i['link'],
                'views': i['viewCount']['short'],
                'published': i['publishedTime'],

            }
            desc = ''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
            result_dict['description'] = desc
            result_list.append(result_dict)
        context = {
            'form':form,
            'youtubeSearchResult':result_list
        }
        return render(request,'dashboard/youtube.html',context)



    context = {
        'form': form
    }
    return render(request,'dashboard/youtube.html',context)

@login_required
def todo(request):
    todo = Todo.objects.filter(user=request.user)
    if request.method == 'POST':
        form = TodoCreate_form(request.POST)
        if form.is_valid():
            Todo(user=request.user,title=request.POST['title']).save()
            return redirect('todo')
    else:
        form = TodoCreate_form()
    return render(request,'dashboard/todo.html',{'todo':todo,'form':form})


@login_required
def delete_todo(request,pk):
    Todo.objects.get(id=pk).delete()
    return redirect('todo')


import requests
def books(request):
    form = Dashboard_Search()
    if request.method == 'POST':
        form = Dashboard_Search(request.POST)
        text = request.POST['text']
        url = "https://www.googleapis.com/books/v1/volumes?q="+text
        r = requests.get(url)
        answer = r.json()



        result_list = []
        for i in range(10):
            result_dict = {
                'title':answer['items'][i]['volumeInfo']['title'],
                'subtitle':answer['items'][i]['volumeInfo'].get('subtitle'),
                'description':answer['items'][i]['volumeInfo'].get('description'),
                'count':answer['items'][i]['volumeInfo'].get('pageCount'),
                'categories':answer['items'][i]['volumeInfo'].get('categories'),
                'rating':answer['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail':answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview':answer['items'][i]['volumeInfo'].get('previewLink'),


            }

            result_list.append(result_dict)
        context = {
            'form':form,
            'bookSearchResult':result_list
        }
        return render(request,'dashboard/books.html',context)



    context = {
        'form': form
    }
    return render(request,'dashboard/books.html',context)

def dictionary(request):
    form = Dashboard_Search()
    if request.method == 'POST':
        text = request.POST['text']
        url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/"+text
        print(url)
        r = requests.get(url)
        answer = r.json()
        try:
            phonetics = answer[0]['phonetics'][0]['text']
            audio = answer[0]['phonetics'][0]['audio']
            definition = answer[0]['meanings'][0]['definitions'][0]['definition']
            example = answer[0]['meanings'][0]['definitions'][0]['example']
            synonyms = answer[0]['meanings'][0]['definitions'][0]['synonyms']
            context = {
                'form':form,
                'input':text,
                'phonetics':phonetics,
                'audio':audio,
                'definition':definition,
                'example':example,
                'synonyms':synonyms,
            }
        except:
            context = {
                'form':form,
                'input':''
            }
        return render(request,'dashboard/dictionary.html',context)


    return render(request, 'dashboard/dictionary.html', {'form':form})

def wiki(request):
    form = Dashboard_Search()
    if request.method == 'POST':
        form = Dashboard_Search(request.POST)
        text = request.POST['text']
        wiki = wikipedia.page(text)
        context = {
            'form': form,
            'title': wiki.title,
            'link': wiki.url,
            'summary': wiki.summary,

        }

        return render(request,'dashboard/wiki.html',context)


    context = {
        'form':form
    }
    return render(request,'dashboard/wiki.html',context)

def conversion(request):
    if request.method == 'POST':
        form = ConversionForm(request.POST)
        measure_form = request.POST['measurements']
        if measure_form == 'length':
            length_form = ConvertLength()
            context = {
                'form':form,
                'm_form':length_form,
                'input':True
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input_ = request.POST['input']
                answer = ''
                if input_ and int(input_) >=0:
                    if first == 'yard' and second == 'foot':
                        answer = f'{input_} yard = {int(input_)*3}feet'
                    if first == 'foot' and second == 'yard':
                        answer = f'{input_} foot = {int(input_)/3} yard'
                context = {
                    'form': form,
                    'm_form': length_form,
                    'input': True,
                    'answer': answer,
                }



        if measure_form == 'mass':
            mass_form = ConvertMass()
            context = {
                'form': form,
                'm_form': mass_form,
                'input': True
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input_ = request.POST['input']
                answer = ''
                if input_ and int(input_) >= 0:
                    if first == 'pound' and second == 'kg':
                        answer = f'{input_} pound = {int(input_) * 0.453592}Kg'
                    if first == 'kg' and second == 'pound':
                        answer = f'{input_} Kg = {int(input_) * 2.20462} Pound'

            context = {
                'form': form,
                'm_form': mass_form,
                'input': True,
                'answer': answer,
            }

    else:
        form = ConversionForm()
        context = {
            'form':form,
        }
    return render(request,'dashboard/conversion.html',context)


def signup(request):
    form = UserSignupForm()
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context = {
        'form':form
    }
    return render(request,'authentication/signup.html',context)

def logout_(request):
    logout(request)
    return redirect('/')

def profile(request):

    todos = Todo.objects.filter(user=request.user)
    hw = Homework.objects.filter(uesr=request.user)
    context = {
        'todos':todos,
        'hw':hw
    }
    return render(request,'dashboard/profile.html',context)
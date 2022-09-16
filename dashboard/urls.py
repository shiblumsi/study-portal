from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('notes',views.notes,name='notes'),
    path('note_delete/<int:pk>',views.delete_note,name='note_delete'),
    path('delete_homework/<int:pk>',views.delete_homework,name='delete_homework'),
    path('note_details/<int:pk>',views.NotesDetail.as_view(),name='notes_details'),
    path('homework',views.homework,name='homework'),
    path('youtube',views.youtube,name='youtube'),
    path('todo',views.todo,name='todo'),
    path('books',views.books,name='books'),
    path('dictionary',views.dictionary,name='dictionary'),
    path('wiki',views.wiki,name='wiki'),
    path('conversion',views.conversion,name='conversion'),
    path('profile',views.profile,name='profile'),
    path('logout',views.logout_,name='logout'),
    path('delete_todo/<int:pk>',views.delete_todo,name='delete_todo'),
]
from django.shortcuts import render
from django.http import HttpResponse
from .models import Movie
import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64


def home(request):
    #return HttpResponse('<h1>Welcome to home page</h1>')
    #return render(request, 'home.html', {'name':'Darieth Sánchez'})
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html',{'searchTerm':searchTerm, 'movies': movies})

def about(request):
    #return HttpResponse('<h1>Welcome to About Page')
    return render(request, 'about.html')

def statitstics_view(request):
    matplotlib.use('Agg')
    genres= Movie.objects.values_list('genre', flat=True).distinct()
    movie_counts_by_genre = {}
    for genre in genres:
        if genre:
            first_genre = genre.split(',')[0].strip()
            movies_in_genre = Movie.objects.filter(genre__startswith=first_genre)
        else:
            movies_in_genre = Movie.objects.filter(genre__isnull=True)
            first_genre = "None"
        count = movies_in_genre.count()
        movie_counts_by_genre[first_genre]=count
    
    bar_width = 0.5
    bar_positions = range(len(movie_counts_by_genre))

    plt.bar(bar_positions, movie_counts_by_genre.values(), width=bar_width, align='center')

    plt.title('Movies per genre')
    plt.xlabel('genre')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions,movie_counts_by_genre.keys(), rotation=90)

    plt.subplots_adjust(bottom=0.3)

    buffer = io.BytesIO()
    plt.savefig(buffer,format='png')
    buffer.seek(0)
    plt.close()

    image_png=buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    return render(request,'statistics.html', {'graphic':graphic})

def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email':email})
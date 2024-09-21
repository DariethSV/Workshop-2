from django.core.management.base import BaseCommand
from movie.models import Movie
import json
import os
import numpy as np
from openai import OpenAI

class Command(BaseCommand):
    help = 'Modify emb field in the database'

    def handle(self, *args, **kwargs):
        from dotenv import load_dotenv, find_dotenv

        load_dotenv(r'C:\Users\Darieth\Desktop\Proyecto_Integrador_1\Workshop-3\Workshop-3\api_keys.env')
        client = OpenAI(
            api_key=os.environ.get('openai_api_key'),
        )
            
        def get_embedding(text, model="text-embedding-3-small"):
            text = text.replace("\n", " ")
            return client.embeddings.create(input = [text], model=model).data[0].embedding
        
        movies = Movie.objects.all()
        for movie in movies:
            emb = get_embedding(movie.description)
            movie.emb = np.array(emb).tobytes()
            movie.save()
            print(f'EMBEDDING DE MOVIE: {movie.title}')
            print(list(np.frombuffer(movie.emb))[0])

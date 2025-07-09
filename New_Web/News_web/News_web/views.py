from django.shortcuts import render
import requests

def home(request):
  apiKey = "1d61ec490a764d7ba519eb3d9b9df9ec"
  requestUrl = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={apiKey}"

  response = requests.get(requestUrl)
  data = response.json()

  articles = data['articles']

  return render(request, 'index.html' , {'articles': articles})
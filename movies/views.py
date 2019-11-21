from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Movie, Genre, Review
from .forms import ReviewForm


# Create your views here.
@require_GET
def index(request):
    movies = Movie.objects.all()
    context = {'movies': movies}
    return render(request, 'movies/index.html', context)


@require_GET
def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    review_form = ReviewForm()
    reviews = movie.reviews.all()
    context = {
        'movie': movie,
        'review_form': review_form,
        'reviews': reviews
    }
    return render(request, 'movies/detail.html', context)


@require_POST
def review_create(request, movie_pk):
    if request.user.is_authenticated:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie_id = movie_pk
            review.user = request.user
            review.save()
            return redirect('movies:detail', movie_pk)
    return redirect('movies:index')



@require_POST
def review_delete(request, movie_pk, review_pk):
    if request.user.is_authenticated:
        review = get_object_or_404(Review, pk=review_pk)
        if review.user == request.user:
            review.delete()
        return redirect('movies:detail', movie_pk)
    return HttpResponse('You are Unauthorized', status=401)


def like(request, movie_pk):
    pass

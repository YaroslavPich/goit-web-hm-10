from django.shortcuts import render, redirect, get_object_or_404
from quotes import scraper
from quotes.models import Quote, Author, Tag
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from quotes.forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from quotes.forms import AuthorForm, QuoteForm
from django.contrib.auth.models import User
from django.contrib import messages

TOP_TAGS = Tag.objects.annotate(num_quotes=Count('quote')).order_by('-num_quotes')[:10].values_list('name',
                                                                                                    'num_quotes')


def register_view(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			if not User.objects.filter(username=username).exists():
				user = form.save()
				login(request, user)
				return redirect('/')
			else:
				messages.warning(request, 'User with that name already exists.', extra_tags='danger')
				return redirect('register_view')
	else:
		form = RegisterForm()
	return render(request, 'quotes/register.html', {'form': form})


def login_view(request):
	if request.method == 'POST':
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect('/')
	else:
		form = AuthenticationForm()
	return render(request, 'quotes/login.html', {'form': form})


def logout_view(request):
	logout(request)
	return redirect('/')


def scrape_to_base(request):
	if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
		scraper.scrape_quotes_and_authors()
		return JsonResponse({'status': 'success'})
	return render(request, 'quotes/waiting.html')


def main(request, page=1):
	quotes = Quote.objects.all()
	per_page = 10
	paginator = Paginator(quotes, per_page)
	quotes_on_page = paginator.page(page)
	return render(request, 'quotes/index.html', {'quotes': quotes_on_page, 'top_tags': TOP_TAGS})


def author_detail(request, author_fullname):
	author = get_object_or_404(Author, fullname=author_fullname)
	return render(request, 'quotes/author_description.html', {'author': author})


def quotes_by_tag(request, tag):
	tag_object = get_object_or_404(Tag, name=tag)
	quotes = tag_object.quote_set.all()
	return render(request, 'quotes/quotes_by_tag.html', {'quotes': quotes, 'tag': tag, 'top_tags': TOP_TAGS})


@login_required
def add_author(request):
	if request.method == 'POST':
		form = AuthorForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')
	else:
		form = Author()
	return render(request, 'quotes/add_author.html', {'form': form})


@login_required
def add_quote(request):
	if request.method == 'POST':
		form = QuoteForm(request.POST)
		if form.is_valid():
			quote = form.save(commit=False)
			quote.user = request.user
			quote.save()
			form.save_m2m()
			return redirect('/')

	else:
		form = QuoteForm()
	return render(request, 'quotes/add_quote.html', {'form': form})

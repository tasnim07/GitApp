
# system imports
import uuid
import json
import requests

# Third party library imports
from github import Github
from requests import Request

# Application imports
from .models import GitHubUser, Create_repo
from GitApp.settings import GITHUB_API_ID,\
    GITHUB_API_SECRET

# Django imports
from django.http import Http404
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, render_to_response,\
    redirect


def index(request):
	return render(request, 'app/index.html')

def get_token(request):
	state =  uuid.uuid4().get_hex()
	request.session['github_auth_state'] = state
	params = {
		'client_id': GITHUB_API_ID,
		'scope': 'user:email, repo, name',
		'state': state
	}
	github_auth_url = 'https://github.com/login/oauth/authorize'
	r = Request('GET', url=github_auth_url, params=params).prepare()
	return redirect(r.url)

def github_callback(request):
	#original_state = request.session.get('github_auth_state')
	#if not original_state:
	#	raise Http404
	#del(request.session['github_auth_state'])

	state = request.GET.get('state')
	code = request.GET.get('code')

	if not state or not code:
		raise Http404
	#if original_state != state:
		#raise Http404

	params = {
		'client_id': GITHUB_API_ID,
		'client_secret': GITHUB_API_SECRET,
		'code': code,
		'state': state,
	}
	headers = {'accept': 'application/json'}
	url = 'https://github.com/login/oauth/access_token'
	r = requests.post(url, params=params, headers=headers)

	if not r.ok:
		raise Http404

	data = r.json()
	access_token = data['access_token']
	
	try:
		github_user = GitHubUser.objects.get(access_token=access_token)
		user = github_user.user
	except:
		# New user
		github_instance = Github(login_or_token=access_token).get_user()
		user = User(username=github_instance.login, password='#!', email=github_instance.email)
		user.save()
		github_user = GitHubUser(user=user, access_token=access_token)
		github_user.save()

	user.backend = 'django.contrib.auth.backends.ModelBackend'
	login(request, user)
		
	print access_token
	return redirect(reverse('get-repo'))

@login_required
def show_repository(request):
	user = request.user
	github_user = GitHubUser.objects.get(user=user)
	access_token = github_user.access_token
	github_user = Github(login_or_token=access_token).get_user()
	
	repos = []
	for repo in github_user.get_repos():
		print repo.name
		repos.append(repo.name)
	return HttpResponse(json.dumps({'repos': repos}))

def logout_view(request):
	logout(request)
	return render(request, 'app/logout.html')

@login_required
def create_repo(request):
	if request.method == 'GET':
		return render(request, 'app/create_repo.html')
	import pdb; pdb.set_trace()
	user = request.user
	try:
		repo_name = 'repo_name' in request.POST
	except:
		repo_name = 'repo_name' in request.POST and request.POST.get('repo_name')
	try:
		description = 'description' in request.POST
	except:
		description = 'description' in request.POST and request.POST.get('description')
	access_token = GitHubUser.objects.get(user=user).access_token
	github_user = Github(login_or_token=access_token).get_user()
	new_repo = github_user.create_repo(repo_name, description=description)
	return render(request, 'app/create_repo.html')

def profile(request):
	parsedData = []
	if request.method == 'POST':
		username = request.POST.get('user')
		req = requests.get('https://api.github.com/users/' + username)
		jsonList = []
		jsonList.append(json.loads(req.content))
		userData = {}
		for data in jsonList:
			userData['name'] = data['name']
			userData['location'] = data['location']
			userData['blog'] = data['blog']
			userData['email'] = data['email']
			userData['public_gists'] = data['public_gists']
			userData['public_repos'] = data['public_repos']
			userData['avatar_url'] = data['avatar_url']
			userData['followers'] = data['followers']
			userData['following'] = data['following']
		parsedData.append(userData)
	return render(request, 'app/profile.html', {'data': parsedData})

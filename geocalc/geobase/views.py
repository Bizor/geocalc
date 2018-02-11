from django.shortcuts import render
from geobase.models import *
from geobase.forms import *
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse

# Create your views here.

def index(request):
    response_data = {}
    if request.user.is_authenticated:
        user = request.user
        response_data['first_name'] = user.first_name
        response_data['last_name'] = user.last_name
        project_list = Project.objects.all
        response_data['project_list'] = project_list
        return render(request, 'index.html', response_data)
    else:
        return HttpResponseRedirect('/login/')

def login(request):
    response_data = {}
    response_data['loginform'] = LoginForm()
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect('/')
        else:
            response_data['login_error'] = "Пользователь с таким логином или пароль не найден."
            return render(request, 'login.html', response_data)
    return render(request, 'login.html', response_data)

def logout(request):
    response_data = {}
    if request.user.is_authenticated:
        auth.logout(request)
        return HttpResponseRedirect('/login/')
    else:
        return HttpResponseRedirect('/login/')


def edit_project(request, project_id):
	response_data = {}
	if request.user.is_authenticated:
		user = request.user
		project = Project.objects.get(id=project_id)
		if request.POST:
			projectform = ProjectForm(request.POST, instance=project)
			if projectform.is_valid():
				project = projectform.save()
				response_data['project_url'] = '/edit_project/%s/' % (project.pk)
				return JsonResponse(response_data)
		response_data['ProjectForm'] = ProjectForm(instance=project)
		response_data['project_name'] = project.project_name
		response_data['project_owner'] = project.project_owner.first_name + ' ' + project.project_owner.last_name
		response_data['project_points'] = project.project_points
		response_data['project_url'] = '/edit_project/%s/' % (project_id) 
		return render(request, 'geocalc.html', response_data)
	else:
		return HttpResponseRedirect('/login/')

def new_project(request):
	response_data = {}
	if request.user.is_authenticated:
		user = request.user
		if request.POST:
			projectform = ProjectForm(request.POST)
			if projectform.is_valid():
				newproject = projectform.save(commit=False)
				newproject.project_owner = user
				project = projectform.save()
				response_data['project_url'] = '/edit_project/%s/' % (project.pk)
				return JsonResponse(response_data)
		response_data['ProjectForm'] = ProjectForm()
		response_data['project_owner'] = user.first_name + ' ' + user.last_name
		response_data['project_points'] = '[]'
		return render(request, 'geocalc.html', response_data)
	else:
		return HttpResponseRedirect('/login/')

def delete_project(request, project_id):
	response_data = {}
	if request.user.is_authenticated:
		user = request.user
		project = Project.objects.get(id=project_id)
		project.delete()
		return HttpResponseRedirect('/')
	else:
		return HttpResponseRedirect('/login/')

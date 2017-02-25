from django.shortcuts import render, get_object_or_404
from django import template
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from models import Bike, User, Slot

import os
def empty_slot(request):
	x = []
	places = Slot.objects.all()
	for place in places:
		if place.vacancy == True:
			x.append(place)
	t = template.loader.get_template('empty_slot.html')
	d = template.RequestContext(request, locals())
	return HttpResponse(t.render(d))

def find_bike(request):
	now_dir = os.path.dirname(__file__)
	file_path = os.path.join(now_dir, 'id.txt')
	f = open(file_path)
	for line in f:
		num = line.split()
		id = num[0]
		x = num[1]
		y = num[2]
		num = Bike.objects.filter(myId = id).count()
		if num == 0:
			return HttpResponseRedirect('/menu/')
		bike = Bike.objects.get(myId = id)
		if x == 0:
			bike.status = 0
		else:
			bike.status = 1
		bike.x = x
		bike.y = y
		bike.save()
	if request.POST:
		name = request.POST['name']
		theUser = User.objects.get(name = name)
	data = f.read()
	bikes = Bike.objects.all()
	jason = [0, 50]
	t = template.loader.get_template('find_bike.html')
	d = template.RequestContext(request, locals())
	return HttpResponse(t.render(d))
def menu(request):
	t = template.loader.get_template('menu.html')
	if request.POST:
		myId = request.POST['myId']
		myName = request.POST['myName']
		num = User.objects.filter(name = myName).count()
		if num == 0:
			user = User.objects.create(name = myName)
		else:
			user = User.objects.get(name = myName)
		num = Bike.objects.filter(myId = myId).count()
		if num == 0:
			Bike.objects.create(myId = myId, user = user)
	d = template.RequestContext(request, locals())
	return HttpResponse(t.render(d))
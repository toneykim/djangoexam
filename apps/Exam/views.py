# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.shortcuts import render, redirect
from . models import User, Trip
from datetime import datetime
import datetime
from datetime import timedelta

# Create your views here.
def index(request):
	return render(request, 'Exam/index.html')


def register(request):
	result = User.objects.register(request.POST)

	if isinstance(result, list):
		for err in result:
			messages.add_message(request, messages.ERROR, err)
		return redirect('/')

	request.session['id'] = result.id
	request.session['name'] = result.name

	return redirect('/travels')

def login(request):
	result = User.objects.login(request.POST)

	print "result is2"
	print result
	print type(result)


	if isinstance(result, unicode):
		messages.add_message(request, messages.ERROR, result)
		return redirect('/')


	print "result is"
	print result

	request.session['id'] = result[0].id
	request.session['name'] = result[0].name




	return redirect('/travels')

def travels(request):
	context = {

	"query1" : Trip.objects.filter(scheduledby__id = request.session['id']),

	"query2" :Trip.objects.all().exclude(scheduledby__id = request.session['id'])
	



	}






	return render(request, 'Exam/travels.html', context)

def logout(request):
	request.session.clear()
	return redirect('/')	

def add(request):




	return render(request, 'Exam/add.html')

def insert(request):

	count = 0

	if len(request.POST['destination']) == 0:
		messages.add_message(request, messages.ERROR, "Destination cannot be empty")
		count = count + 1

	if len(request.POST['description']) == 0:
		messages.add_message(request, messages.ERROR, "Description cannot be empty")
		count = count + 1

	if len(request.POST['datefrom']) == 0:
		messages.add_message(request, messages.ERROR, "Date From cannot be empty")
		count = count + 1

	if len(request.POST['dateto']) == 0:
		messages.add_message(request, messages.ERROR, "Date to cannot be empty")
		count = count + 1


	if len(request.POST['datefrom']) != 0:

		today = datetime.datetime.today()
		print "today"
		print today

		myformat = "%Y-%m-%d"

		todayfix = today.strftime(myformat)
		print todayfix

		datefrom = request.POST['datefrom']
		datefromfix = datetime.datetime.strptime(datefrom, '%Y-%m-%d')
		datefromfix2 = datefromfix.strftime(myformat)
		print datefromfix2

		difference = datefromfix - today
		print "difference"
		print type(difference)
		
		print difference.days
		print type(difference.days)

		if difference.days < 0:
			count = count + 1
			messages.add_message(request, messages.ERROR, "Date from is in the past")		

		if difference.days >= 0:
			print "in the future"
			print request.POST['dateto']
			print type(request.POST['dateto'])

		if len(request.POST['dateto']) != 0 :

			dateto = request.POST['dateto']
			datetofix = datetime.datetime.strptime(dateto,  '%Y-%m-%d')

			difference2 = datetofix - datefromfix
			print "difference2"
			print difference2.days
			if difference2.days < 0:
				count = count + 1
				messages.add_message(request, messages.ERROR, "Date to cannot be before date from")	

	if count == 0:

		print "request.session"
		idsession = request.session['id']
		print type(request.session['id'])

		obj = User.objects.get(id = idsession)

		print obj.id
		print obj.name




		result = Trip.objects.create(destination=request.POST['destination'], description=request.POST['description'],datefrom=request.POST['datefrom'],dateto=request.POST['dateto']  )

		

		print "result"
		print result
		print result.id
		print result.destination


		thisUser = User.objects.get(id=idsession)
		thisTrip = Trip.objects.get(id=result.id)
		thisTrip.scheduledby.add(thisUser)


		messages.add_message(request, messages.ERROR, "Trip Inserted")



	print "count is " 
	print count
	print request.POST['destination']
	print request.POST['description']
	print request.POST['datefrom']
	print request.POST['dateto']



	return redirect('/travels/add')


def tripdetail(request, number):
	context ={

	"query11" : Trip.objects.filter(id = number),
	"query12" : User.objects.filter(scheduled__id = number)



	}

	return render(request, 'Exam/tripdetail.html', context)

def join(request,number):

	idsession = request.session['id']
	thisUser = User.objects.get(id=idsession)
	thisTrip = Trip.objects.get(id=number)
	thisTrip.scheduledby.add(thisUser)


	return redirect('/travels')

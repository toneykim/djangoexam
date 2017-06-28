# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re, datetime, bcrypt
from django.db import models
from datetime import datetime
import datetime

class UserManager(models.Manager):
	def register(self, data):
		EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


		errors = []

		for field in data:
			if len(data[field]) == 0:
				errors.append(field.replace('_',' ').title() + " may not be empty")


		if len(data['name']) < 3 or data['username'] < 3 :
			errors.append("Name and Username must be at least 3 characters long")

		if not data['name'].isalpha() or not data['username'].isalpha():
			errors.append("Name and Username may only be letters")



	
		if len(data['password']) < 8:
			errors.append("Password must be at least 8 characters long")


		print data['password']
		print data['confirm']

		print "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
	



		if data['password'] != data['confirm']:
			errors.append("Passwords do not match")
		try:
			User.objects.get(username=data['username'])
			errors.append("Username already registered. Forgot your username?")
		except:
			pass

		if len(errors) == 0:
			hashed_pw = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())
			print hashed_pw 

			user = User.objects.create(name=data['name'], username=data['username'],  password=hashed_pw)

			return user
		return errors






	def login(self, data):
		EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')



		print "password is"
		print data['password']
		print len(data['password'])


		if len(data['username']) == 0:
			return "Username is empty"

		if len(data['password']) == 0:
			print "Password is empty"
			return "Password is empty"

		
		user = User.objects.filter(username=data['username'])		


		print "user is"
		print user
		print len(user)

		if len(user) == 0:
			return "Username not registered"


		hashed_pw = bcrypt.hashpw(data['password'].encode(), user[0].password.encode())
	
		print "the password is"

		print user[0].password
		print hashed_pw


		if hashed_pw == user[0].password:
			return user


		return "incorrect password"

















# Create your models here.

class User(models.Model):
	name = models.CharField(max_length=255)
	username = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	update_at = models.DateTimeField(auto_now=True)
	objects = UserManager()

class Trip(models.Model):
	destination = models.CharField(max_length=255)
	description = models.CharField(max_length=255)
	datefrom = models.DateTimeField()
	dateto = models.DateTimeField()
	scheduledby = models.ManyToManyField(User, related_name="scheduled")	
	objects = UserManager()


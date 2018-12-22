from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class User(AbstractUser):
	is_admin = models.BooleanField(default=False)
	is_customer = models.BooleanField(default=False)
	

class Customer(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
	def __str__(self):
		return self.user.username
		
class Ticket(models.Model):
	customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
	subject = models.CharField(max_length=500,blank=False)
	is_resolved = models.BooleanField(default=False)

	def open_ticket(self):
		return Ticket.objects.filter(is_resolved = False).length()

	

class Comment(models.Model):
	ticket = models.ForeignKey(Ticket,on_delete=models.CASCADE)
	is_admin_response = models.BooleanField(default=False)
	text = models.CharField(max_length=500, blank=False)


	def get_absolute_url(self):
		if(self.is_admin_response):
			return reverse('admin_ticket_detail',kwargs={'pk':self.ticket.pk})

		return reverse('ticket_detail',kwargs={'pk':self.ticket.pk})






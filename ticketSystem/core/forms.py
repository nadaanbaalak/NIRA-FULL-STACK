from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import (User,Customer,Ticket,Comment)
from django.urls import reverse_lazy




class CustomerSignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User

    
    def save(self):
        user = super().save(commit=False)
        user.is_customer = True
        user.save()
        customer = Customer.objects.create(user=user)
        
        return user


class TicketCreateForm(forms.ModelForm):

    message = forms.CharField(max_length=500)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(TicketCreateForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Ticket
        fields = ('subject',)

    def save(self):
        message = self.cleaned_data['message']
        ticket = super().save(commit=False)
        ticket.customer = self.request.user.customer
        ticket.save()
        Comment.objects.create(ticket=ticket,is_admin_response=False,text=message)
        return ticket


class CommentCreateForm(forms.ModelForm):

    ticket_pk = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(CommentCreateForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Comment
        fields = ('text',)

    def save(self):
        print("ok")
        ticket_pk = self.cleaned_data['ticket_pk']
        ticket = Ticket.objects.get(pk = ticket_pk)
        comment = super().save(commit=False)
        comment.ticket = ticket
        if self.request.user.is_admin:
            comment.is_admin_response=True
        comment.save()
        
        return comment


class TicketListForm(forms.Form):

    FILTER_CHOICES = ((1,"All"),(2,"Open"),(3,"Closed"))
    filter_by = forms.ChoiceField(choices=FILTER_CHOICES, widget=forms.RadioSelect())


    



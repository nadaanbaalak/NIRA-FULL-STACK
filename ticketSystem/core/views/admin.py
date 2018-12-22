from django.shortcuts import render,redirect
from django.views.generic import CreateView, ListView, UpdateView,DetailView
from ..models import Ticket,User
from ..forms import CustomerSignUpForm,TicketCreateForm,TicketListForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from ..decorators import admin_required


@method_decorator([login_required, admin_required], name='dispatch')
class AdminTicketListView(ListView):
	model = Ticket
	template_name = 'admin/admin_view_tickets.html'
	context_object_name = 'ticket_list'

	def get_context_data(self, **kwargs):
		context = super(AdminTicketListView, self).get_context_data(**kwargs)
		context['form'] = TicketListForm()

		context['open'] = Ticket.objects.filter(is_resolved = False).count()
		context['closed'] = Ticket.objects.filter(is_resolved = True).count()
		
		return context
		

	def get_queryset(self):
		try:
			filter_by = self.request.GET.get('filter_by')
		except KeyError:
			filter_by = "1"

		
		if filter_by == "2":
			return Ticket.objects.filter(is_resolved=False)

		if filter_by == "3":
			return Ticket.objects.filter(is_resolved=True)

				
		return Ticket.objects.all()


@method_decorator([login_required, admin_required], name='dispatch')
class AdminTicketDetailView(DetailView):
	model = Ticket
	template_name = 'admin/admin_ticket_detail.html'


@login_required

def AdminTicketUpdateView(request,pk):
	if request.method == "POST":
		Ticket.objects.filter(pk = pk).update(is_resolved = True)

	return redirect('admin_home')
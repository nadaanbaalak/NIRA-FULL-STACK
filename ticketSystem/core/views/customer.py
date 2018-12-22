from django.shortcuts import render,redirect
from django.views.generic import CreateView, ListView, UpdateView, DetailView

from ..models import Ticket,User
from ..forms import CustomerSignUpForm,TicketCreateForm,CommentCreateForm,TicketListForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from ..decorators import customer_required,creator


@method_decorator([login_required, customer_required], name='dispatch')
class TicketListView(ListView):
	model = Ticket
	template_name = 'customer/view_tickets.html'
	context_object_name = 'customer_ticket_list'

	def get_context_data(self, **kwargs):
		context = super(TicketListView, self).get_context_data(**kwargs)
		context['form'] = TicketListForm()
		context['username'] = self.request.user.username
		return context

	def get_queryset(self):
		try:
			filter_by = self.request.GET.get('filter_by')
		except KeyError:
			filter_by = "1"
		print(type(filter_by))
		if filter_by == "2":
			return self.request.user.customer.ticket_set.filter(is_resolved=False)

		if filter_by == "3":
			return self.request.user.customer.ticket_set.filter(is_resolved=True)

		return self.request.user.customer.ticket_set.all()


class CustomerSignUpView(CreateView):
    model = User
    form_class = CustomerSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'customer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('customer_home')


@method_decorator([login_required, customer_required], name='dispatch')
class TicketCreateView(CreateView):
	model = Ticket
	template_name = 'customer/create_ticket.html'
	form_class = TicketCreateForm
	success_url = reverse_lazy('customer_home')

	def get_form_kwargs(self):
		kwargs = super(TicketCreateView, self).get_form_kwargs()
		kwargs['request'] = self.request
		return kwargs


@method_decorator([login_required, customer_required,creator], name='dispatch')
class TicketDetailView(DetailView):
	model = Ticket
	template_name = 'customer/ticket_detail.html'



@method_decorator([login_required], name='dispatch')
class CommentCreateView(CreateView):
	
	model = Ticket
	template_name = 'customer/ticket_detail.html'
	form_class = CommentCreateForm

	


	def get_form_kwargs(self):
		kwargs = super(CommentCreateView, self).get_form_kwargs()
		kwargs['request'] = self.request
		return kwargs

	
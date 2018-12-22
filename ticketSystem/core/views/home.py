from django.shortcuts import redirect

def login_success(request):
    """
    Redirects users based on whether they are in the admins group
    """
    if request.user.is_admin:
        # user is an admin
        return redirect("admin_home")
    else:
        return redirect("customer_home")
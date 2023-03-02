from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from accounts.forms import LoginForm
from accounts.decorators import unauthenticated_user_required


@unauthenticated_user_required
def log_in(request):
    form = LoginForm()
    context = {"form": form, "error_message": None}
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                if user.is_admin:
                    return redirect("admin:index")
                elif user.is_staff:
                    if request.user.groups.exists():
                        group = request.user.groups.first().name
                        if group == "gestion":
                            return redirect("/gestion-admin/")
                        elif group == "vente":
                            return redirect("/vente-admin/")
                        elif group == "support":
                            return redirect("/support-admin/")
                else:
                    return redirect("about")
            else:
                error_message = "Identifiants invalides."
                context["error_message"] = error_message
        else:
            context["form"] = form
    return render(request, "accounts/login_form.html", context)


@login_required
def log_out(request):
    logout(request)
    return redirect("login")

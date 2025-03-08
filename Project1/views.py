import logging
import sqlite3

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password, password_changed, \
    password_validators_help_text_html
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from Project1.models import Msg

logger = logging.getLogger(__name__)


def index_view(request):
    msgs = Msg.objects.all()
    return render(request, "index.html", {"msgs": msgs, "user": request.user})


@login_required
def send_view(request):
    if request.method != "POST":
        return HttpResponse(status=405)

    data = request.POST.get("data")

    if data is None:
        return HttpResponse(status=400)

    # Fix for SQL injection
    # msg = Msg(user=request.user, data=data)
    # msg.save()

    # Unsafe code that causes SQL injection
    from Project1.settings import BASE_DIR
    conn = sqlite3.connect(BASE_DIR / 'db.sqlite3')
    cursor = conn.cursor()

    sql = f"INSERT INTO Project1_msg (data, user_id) VALUES (\"{data}\", {request.user.id})"
    cursor.execute(sql)
    conn.commit()

    return redirect("/")


def delete_view(request):
    if request.method != "POST":
        return HttpResponse(status=405)

    id = request.POST.get("id")
    if id is None:
        return HttpResponse(status=400)

    object = Msg.objects.get(id=id)

    # Fix broken access
    # if object.user != request.user:
    #    return HttpResponse(status=401)

    object.delete()
    return redirect("/")


def new_account_view(request):
    if request.method != "GET":
        return HttpResponse(status=405)

    password_error = request.session.get("password_error", default=None)
    try:
        del request.session["password_error"]
    except KeyError:
        pass

    password_help = password_validators_help_text_html()
    return render(request, "new_account.html", {"password_error": password_error, "help": password_help})


def new_account_submit_view(request):
    if request.method != "POST":
        return HttpResponse(status=405)

    username = request.POST.get("username")
    password1 = request.POST.get("password1")
    password2 = request.POST.get("password2")

    if username is None or password1 is None or password2 is None:
        return HttpResponse(status=400)

    if User.objects.filter(username=username).exists():
        request.session["password_error"] = "Username already exists"
        return redirect("/new_account")

    if password1 != password2:
        request.session["password_error"] = "Given passwords are different"
        return redirect("/new_account")

    try:
        validate_password(password1)
    except ValidationError as errors:
        request.session["password_error"] = " ".join(errors.messages)
        return redirect("/new_account")
    usr = User(password=make_password(password1), username=username)
    usr.save()
    password_changed(password1, user=usr)

    #Log new users
    #logger.info(f"New account made: {username}")
    return redirect("/")


class LoggingLoginView(LoginView):
    def form_valid(self, form):
        res = super().form_valid(form)
        logger.info(f"{form["username"].value()} logged in successfully")
        return res

    def form_invalid(self, form):
        res = super().form_invalid(form)
        logger.info(f"Login attempt: {form["username"].value()} with errors: {form.errors.as_json()}")
        return res

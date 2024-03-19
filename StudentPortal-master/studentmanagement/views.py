from django.shortcuts import render, redirect
#from django.http import HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# from django.utils.decorators import method_decorator

from .decorators import admin_only, unauthenticated_user, allowed_users
from django.contrib.auth.models import User

# EMAIL ACTIVATION AND SEND EMAIL LINKS
# from django.contrib.sites.shortcuts import get_current_site
# from django.template.loader import render_to_string
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.utils.encoding import force_bytes, force_text
# from .utils import generate_token
from django.core.mail import send_mail
# from django.core.mail import EmailMessage
# from validate_email import validate_email
from django.conf import settings
from django.db.models import Q
from django.views import generic
# PAGE PAGINATION
from django.core.paginator import Paginator

from .models import *
from .forms import *


@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
           # user.is_active = False
            user.save()

            # # EMAIL ACTIVATION LINK FOR USER AUTHENTICATION
            # current_site = get_current_site(request)
            # subject = 'Activate your Student Account'
            # message = render_to_string('account_activation_email.html', {
            #     'user': user,
            #     'domain': current_site.domain,
            #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            #     'token': generate_token.make_token(user),
            # })
            # email_message=EmailMessage(
            #     subject,
            #     message,
            #     settings.EMAIL_HOST_USER,
            #     to=[email]
            # )
            # email_message.send(fail_silently=False)
            messages.success(request, "Account was created for " + username)
            return redirect('loginPage')
           # return HttpResponse('Check your Email for the activation link')

        else:
            form = CreateUserForm()
            messages.warning(
                request, "Your details are invalid. Ensure they are correct and try again")

    context = {
        'form': form,
    }
    return render(request, 'register.html', context)

# @unauthenticated_user
# def activate(request, uidb64, token):
#     try:
#         uid = force_text(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except(TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None

#     if user is not None and generate_token.check_token(user, token):
#         user.is_active = True
#         user.save()
#         #login(request, user)
#         messages.success(request, 'Account activated successfully')
#         return redirect('loginPage')
#     else:
#         return render(request, 'activation_invalid.html')


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_staff:
                login(request, user)
                return redirect('dashboard')
            elif user.is_active:
                login(request, user)
                return redirect('student_page')
        else:
            messages.warning(request, "username OR password is incorrect")
    return render(request, 'login.html', {})


@login_required(login_url='loginPage')
def logoutUser(request):
    logout(request)
    return redirect('home')


@unauthenticated_user
def home(request):
    return render(request, 'home.html', {})


@login_required(login_url='loginPage')
@admin_only
def dashboard(request):
    students = Student.objects.all().order_by('date_created')
    total_students = students.count()

    # #PAGINATION
    p = Paginator(Student.objects.all().order_by('date_created'), 30)
    page = request.GET.get('page')
    student_list = p.get_page(page)
    nums = "a" * student_list.paginator.num_pages

    # # SEARCH FORM
    # form = StudentSearchForm(request.POST or None)
    # if request.method == 'POST':
    #     form = StudentSearchForm(request.POST or None)
    #     student_list = Student.objects.filter(
    #         full_name__icontains=form['full_name'].value(),
    #         reg_number__icontains=form['reg_number'].value(),
    #     )

    context = {
        'total_students': total_students,
        # 'form': form,
        'students': students,
        'student_list': student_list,
        'nums': nums,
    }
    return render(request, 'dashboard.html', context)

# Search View

class SearchView(generic.TemplateView):
    template_name = "search.html"

    models = Student

    def get_queryset(self):
        return Student.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get('keyword')
        student_list = Student.objects.filter(
            Q(full_name__icontains=kw) | Q(reg_number__icontains=kw))
        print('student_list')
        context['student_list'] = student_list
        return context


@login_required(login_url='loginPage')
@admin_only
def student_details(request, pk):
    student = Student.objects.get(id=pk)
    context = {
        'student': student,
    }
    return render(request, 'student_details.html', context)


@login_required(login_url='loginPage')
@admin_only
def delete_students(request, pk):
    student = Student.objects.get(id=pk)
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student deleted successfully')
        return redirect('dashboard')
    context = {
        'student': student,
    }
    return render(request, 'delete_students.html', context)


@login_required(login_url='loginPage')
@admin_only
def update_fees(request, pk):
    student = Student.objects.get(id=pk)
    form = FeeUpdateForm(instance=student)
    if request.method == 'POST':
        form = FeeUpdateForm(request.POST or None, instance=student)
        if form.is_valid():
            fee_required = form.cleaned_data.get('fee_required')
            fee_paid = form.cleaned_data.get('fee_paid')
            student.fee_balance = fee_paid - fee_required
            form.save()
            return redirect(reverse('student_details', kwargs={
                'pk': student.pk,
            }))
    context = {
        'student': student,
        'form': form,
    }
    return render(request, 'update_fees.html', context)


@login_required(login_url='loginPage')
@admin_only
def update_cert(request, pk):
    student = Student.objects.get(id=pk)
    form = CertUpdateForm(instance=student)
    if request.method == 'POST':
        form = CertUpdateForm(request.POST or None, instance=student)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    context = {
        'student': student,
        'form': form,
    }
    return render(request, 'update_cert.html', context)


@login_required(login_url='loginPage')
@admin_only
def update_exam_results(request, pk):
    student = Student.objects.get(id=pk)
    form = ExamUpdateForm(instance=student)
    if request.method == 'POST':
        form = ExamUpdateForm(request.POST or None, instance=student)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    context = {
        'student': student,
        'form': form,
    }
    return render(request, 'exam_results.html', context)


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['student'])
def student_page(request):
    student = request.user.student
    context = {
        'student': student
    }
    return render(request, 'studentpage.html', context)


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['student'])
def account_settings(request):
    student = request.user.student
    form = StudentAccountSettingsForm(instance=student)
    if request.method == 'POST':
        form = StudentAccountSettingsForm(
            request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_page')
    context = {
        'form': form,
        'student': student
    }
    return render(request, 'account_settings.html', context)


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['student'])
def delete_profile(request):
    if request.method == 'POST':
        user = User.objects.get(username=request.user)
        user.is_active = False
        user.save()
        return redirect('loginPage')
    return render(request, 'delete_profile.html')


@unauthenticated_user
def contact(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST or None)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            send_mail(f"{first_name} {last_name} sent an email", message,
                      email, [settings.EMAIL_HOST_USER], fail_silently=False)
            return redirect('email_received')

    context = {
        'form': form,
    }

    return render(request, 'contact.html', context)


@unauthenticated_user
def email_received(request):
    context = {
        'success': True,
    }
    return render(request, 'email_received.html', context)


@unauthenticated_user
def about(request):
    return render(request, 'about.html', {})


# @login_required(login_url='loginPage')
# @admin_only
# def add_students(request):
#     form = StudentCreationForm(request.POST or None, request.FILES)
#     if request.method == 'POST':
#         form = StudentCreationForm(request.POST or None, request.FILES)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Student added successfully')
#             return redirect('dashboard')

#     context={
#         'form': form,
#     }
#     return render(request, 'add_students.html', context)


# @login_required(login_url='loginPage')
# @admin_only
# def update_students(request, pk):
#     student = Student.objects.get(id=pk)
#     form = StudentUpdateForm(instance=student)
#     if request.method =='POST':
#         form = StudentUpdateForm(request.POST or None, request.FILES, instance=student)
#         if form.is_valid():
#             form.save()
#             messages.success(request, str(student.full_name + ' details updated successfully'))
#             return redirect('dashboard')

#     context = {
#         'student': student,
#         'form': form,
#     }
#     return render(request, 'update_students.html', context)

from django.contrib.auth.hashers import make_password
from unicodedata import category
from urllib import request
from django.shortcuts import render
from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.core import serializers

from django.core.mail import send_mail

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import Group
from main.decorators import unauthenticated_user,allowed_users

import csv
from django.http import HttpResponseRedirect

# Create your views here.
from .models import *
from .forms import Industryregistrationform, Instituteregistrationform, AddInternshipform ,ProfileUpdate
from django.core.paginator import Paginator


#dashboard views
def loginPage(request):
        if request.method == 'POST':
            username = request.POST.get('username')
            password =request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                group=request.user.groups.all()[0].name
                if group == 'industry':
                    industry = Industries.objects.filter(user = request.user).get()
                    return redirect('dashboard',pk=industry)
                if group == 'institute':
                    institute = Institutes.objects.filter(user = request.user).get()
                    return redirect('institute_dashboard',pk=institute)
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'login.html', context)

@login_required(login_url=loginPage)
@allowed_users(allowed_roles=['industry'])
def dashboard(request,pk):
    if pk != str(Industries.objects.filter(user = request.user).get()):
         return HttpResponse("You are not authorized to view this page")
    context = {'industry': pk}
    return render(request, 'dashboard/dashboard_main.html',context)

@login_required(login_url=loginPage)
@allowed_users(allowed_roles=['institute'])
def institute_dashboard(request,pk):
     if pk != str(Institutes.objects.filter(user = request.user).get()):
         return HttpResponse("You are not authorized to view this page")
     context = {'institute': pk}
     return render(request ,'institute_dashboard/dashboard_main.html',context )


@login_required(login_url='login')
@allowed_users(allowed_roles=['industry'])
def student_list(request,pk):
    if pk != str(Industries.objects.filter(user = request.user).get()):
         return HttpResponse("You are not authorized to view this page")
    openings=Openings.objects.all().filter(industry= Industries.objects.get(user= request.user))
    context = {'openings': openings,'industry':pk}
    return render(request, 'dashboard/studentlist.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['industry'])
def institutes_applied(request,pk,ic):
    open=Openings.objects.filter(id=ic).get()
    objects=consent_form.objects.filter(Openings=open).all()
    if request.method == 'POST':
        for i in objects:
            if request.POST.get(str(i.id)) == 'on':
                id = consent_form.objects.get(id=i.id)
                id.approved = True
                id.save()
        return HttpResponseRedirect(request.path_info)
    context = {'consents': objects,'industry':pk,'openings':ic}
    return render(request, 'dashboard/institutes_applied.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['industry'])
def students_applied(request,pk,ic,op):
    if pk != str(Industries.objects.filter(user = request.user).get()):
         return HttpResponse("You are not authorized to view this page")
    industry=Industries.objects.filter(user=request.user).get()
    open=Openings.objects.filter(id=op).get()
    institute=Institutes.objects.filter(name=ic).get()
    list_of_students=Application.objects.filter(openings_id=open.id).filter(institute__name=institute).all()
    context={'students':list_of_students,'industry':pk,'openings':op,'institute':ic}
    return render(request, 'dashboard/students_applied.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['industry'])
def manage_internship(request,pk):
    if pk != str(Industries.objects.filter(user = request.user).get()):
         return HttpResponse("You are not authorized to view this page")
    objects = Openings.objects.all().filter(industry= Industries.objects.get(user= request.user))
    context = {'openings': objects,'industry':pk}
    return render(request, 'dashboard/manage_internship.html',context)

@login_required(login_url=loginPage)
@allowed_users(allowed_roles=['institute'])
def openings_details(request,ic,pk):
    if pk != str(Institutes.objects.filter(user = request.user).get()):
         return HttpResponse("You are not authorized to view this page")
    objects=Openings.objects.filter(id=ic).get()
    institute=Institutes.objects.filter(user=request.user).get()
    num_of_applies=len(consent_form.objects.filter(Openings=objects).filter(institute_name=institute).all())
    status=True
    verified=False
    if num_of_applies==0:
        status=False
    if(status==True):
        obj=consent_form.objects.filter(Openings=objects).filter(institute_name=institute).all()[0]
        if obj.approved==True:
            verified=True
    context = {'openings': objects ,"institute":pk,"status":status,"verified":verified }
    return render(request, 'institute_dashboard/openings_details.html',context)

@login_required(login_url=loginPage)
@allowed_users(allowed_roles=['institute'])
def manage_institute_internship(request,pk):
    if pk != str(Institutes.objects.filter(user = request.user).get()):
         return HttpResponse("You are not authorized to view this page")
    openings = Openings.objects.all()
    applications= Application.objects.all()
    context = {'openings': openings,'applications':applications , 'institute':pk}
    return render(request, 'institute_dashboard/manage_internship.html',context)

@login_required(login_url=loginPage)
@allowed_users(allowed_roles=['institute'])
def view_openings(request,pk):
    if pk != str(Institutes.objects.filter(user = request.user).get()):
         return HttpResponse("You are not authorized to view this page")
    object = Openings.objects.all()
    context = {'openings': object , 'institute':pk}
    return render(request, 'institute_dashboard/view_openings.html',context)
   
@login_required(login_url='login')
@allowed_users(allowed_roles=['industry'])
def add_internship(request,pk):
    form=AddInternshipform()
    if request.method == 'POST':
            form = AddInternshipform(request.POST)
            if form.is_valid():
                industr = Industries.objects.filter(user = request.user).get()
                form.save(industry = industr)
                messages.info(request, 'The opening added is successfully posted.')
                return redirect('manageinternship')
    context = {'form':form , 'industry':pk}
    return render(request, 'dashboard/add_internship.html', context)



def index(request):
    industries=Industries.objects.all()
    return render(request, 'index.html', {'industries':industries})

@login_required(login_url=loginPage)
@allowed_users(allowed_roles=['student'])
def profile(request):
    user=request.user
    profile=Profile.objects.get(user=user)
    form=ProfileUpdate(initial={'headline':profile.headline,'profile_pic':profile.profile_pic,'contact_num':profile.contact_num,'currently_emp':profile.currently_emp,
                                'last_educational_degree':profile.last_educational_degree,'skills':profile.skills,
                                'institute':profile.institute,'open_for_jobs':profile.open_for_jobs,
                                'past_experience':profile.past_experience,'resume':profile.resume,
                                'linkedin_link':profile.linkedin_link,'github':profile.github,
                                'job_cat':profile.job_cat
                                })
    if request.method == "POST":
        form = ProfileUpdate(request.POST, instance=profile)
        if form.is_valid():
            try:
                form.save()
                model = form.instance
                return redirect('profile')
            except Exception as e:
                pass
    return render(request, 'profile.html', {'user':user,'form':form})


def contact(request):
    return render(request, 'contact.html')

def details(request,pk,ic):
    opening=Openings.objects.filter(job_title=pk).filter(industry__name=ic)
    user={'username':'guest'}
    if request.user.is_authenticated:
         user = request.user
        
    context={'opening':opening}
    return render(request, 'details.html',context)

def openings(request):
    openings= Openings.objects.all()
    context = {'openings':openings} 
    return render(request, 'openings.html', context)

def consultancies(request):
    problem=Consultancy.objects.all()
    context = {'problem':problem}
    return render(request, 'consultancies.html', context)

def consultancy_details(request,pk):
    problem=Consultancy.objects.filter(id=pk).get()
    context = {'problem':problem}
    return render(request, 'consultancy_details.html', context)

def registerPage(request):
    if request.method == 'POST':
        user=User.objects.create(
            username=request.POST['username'],
            email=request.POST['email'],
            password=make_password(request.POST['password2']),
            is_active=True)
        user.save()
        my_group = Group.objects.get(name='user')
        user.groups.add(my_group)
        return redirect('login')
    return render(request, 'signup_student.html')

@login_required(login_url=loginPage)
@allowed_users(allowed_roles=['institute'])
def institute_student_list(request,pk):
    if pk != str(Institutes.objects.filter(user = request.user).get()):
         return HttpResponse("You are not authorized to view this page")
    if request.method == 'POST':
          file = request.FILES["excel_file"]
          document = stud_data_upload.objects.create(excel_file = file,institute_name = request.user)
          document.save()
          doc = stud_data_upload.objects.filter(institute_name = request.user).latest('pk')
          filename = str(doc.excel_file)

          
          if not filename.endswith('.csv'):
              messages.info(request, 'File is not CSV type')
          else:
                #form = CreateUserForm_excel()
                usernames = []
                file = open('media/' + filename)
                df=csv.reader(file)
                print(df)

                header=[]
                header=next(df)
                

                previous=[]
                prev=[pro.user.email for pro in Profile.objects.filter(user=request.user)]
                print(prev)
                rows =[]
                new_not_created=[]
                for row in df :
                    if row[0] not in prev:
                        rows.append(row)
                    else:
                         new_not_created.append(row)
                print(new_not_created)
                pass_c=make_random_password()
                for row in rows:
                    user=User.objects.create(username=row[0],
                        email=row[0],
                        password=make_password(pass_c),
                        first_name=row[2],
                        is_active=True)
                    my_group = Group.objects.get(name='student')
                    user.groups.add(my_group)
                    institute = Institutes.objects.filter(user = request.user).get()
                    pro=Profile.objects.get(user=user)
                    pro.institute=institute
                    pro.contact_num=row[1]
                    pro.save()
                    messages.info(request, 'Your File was Uploaded Successfully')
    user=User.objects.filter(groups=4).all()
    profile = Profile.objects.filter(institute = Institutes.objects.filter(user=request.user).get()).filter(user__groups=4).all()
    context={'users':profile,'institute': Institutes.objects.filter(user=request.user).get()}
    return render(request, 'institute_dashboard/studentlist.html',context)

def logoutUser(request):
    logout(request)
    return redirect('login')

def industry_details(request):
    if request.method == 'POST' :
        name = request.POST['name']
        description = request.POST['description']
        email = request.POST['email']
        logo = request.POST['logo']
        category = request.GET.get('category')
        registration_date = request.POST['registration_date ']
        estb_year = request.POST['estb_year']
        cii_id = request.POST['cii_id']
        website = request.POST['website']
        contact_num = request.POST['contact_num']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        pincode = request.POST['pincode']
        country = request.POST['country']
        ob=Industries(name=name, description=description, email=email, logo=logo, category=category, registration_date=registration_date, estb_year=estb_year,website=website, contact_num=contact_num, address=address, city=city, state=state, pincode=pincode, country=country)
        ob.save()
        return render(request, 'industry_details.html')
    else:
        return render(request, 'industry_details.html')

def industry_data(request):
    industries = Industries.objects.all()
    paginator = Paginator(industries, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    jsondata = serializers.serialize('json', page_obj)
    return HttpResponse(jsondata, content_type='application/json')


def industries(request):
    industries= Industries.objects.all()
    paginator = Paginator(industries, 2) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'industries.html', {'page_obj': page_obj})

def institute_details(request):
    if request.method == 'POST' :
        name = request.POST['name']
        description = request.POST['description']
        email = request.POST['email']
        logo = request.POST['logo']
        category = request.GET.get('category')
        registration_date = request.POST['registration_date ']
        estb_year = request.POST['estb_year']
        cii_id = request.POST['cii_id']
        website = request.POST['website']
        contact_num = request.POST['contact_num']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        pincode = request.POST['pincode']
        country = request.POST['country']
        ob=Industries(name=name, description=description, email=email, logo=logo, category=category, registration_date=registration_date, estb_year=estb_year,website=website, contact_num=contact_num, address=address, city=city, state=state, pincode=pincode, country=country)
        ob.save()
        return render(request, 'institute_details.html')
    else:
        return render(request, 'institute_details.html')

def institute_data(request):
    institutes = Institutes.objects.all()
    paginator = Paginator(institutes, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    jsondata = serializers.serialize('json', page_obj)
    return HttpResponse(jsondata, content_type='application/json')

def institutes(request):
    institutes= Institutes.objects.all()
    paginator = Paginator(institutes, 2) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'institutes.html', {'page_obj': page_obj})

@login_required(login_url=loginPage)
@allowed_users(allowed_roles=["user"])
def industry_registration(request):
    form=Industryregistrationform()
    if request.method == 'POST':
            form = Industryregistrationform(request.POST)
            if form.is_valid():
                form.save()
                messages.info(request, 'Industry is registered and sent for Verification to the CII')
                return redirect('industry')
            else:
                print("invlid")
            
    context = {'form':form}
    return render(request, 'industry_registration.html', context)

@login_required(login_url=loginPage)
@allowed_users(allowed_roles=["user"])
def institute_registration(request):
    form=Instituteregistrationform()
    if request.method == 'POST':
            form = Instituteregistrationform(request.POST)
            if form.is_valid():
                form.user=request.user
                form.save()
                messages.info(request, 'Institute is registered and sent for Verification to the CII')
                return redirect('institute')
            else:
                print("invalid")
                print(form.errors)
            
    context = {'form':form}
    return render(request, 'institute_registration.html', context)

def apply_openings(request,pk,ic):
    institute=Institutes.objects.filter(user=request.user).get()
    openings = Openings.objects.filter(id=ic).get()
    industry_name = Openings.objects.filter(id=ic).get().industry
    
    consent=institute_applied.objects.filter(industry=industry_name).filter(institute_name = institute)
    if consent: 
        if consent.approved =='Approved':
            users=User.objects.filter(groups=4).all()
            profile = Profile.objects.filter(institute = Institutes.objects.filter(user=request.user).get()).filter(user__groups=4).all()
            context = {'openings':openings, 'users':profile,"institute":pk}
            return render(request, 'institute_dashboard/apply_openings.html', context)
        else:
            messages.info(request, 'You can only apply after the Industry approves your request')
    else:
        messages.info(request, 'You need to fill consent form before applying')
        context={"institute":pk}
        return redirect('consent_form',context)
 
def consent_(request,pk,ic):
    if request.method=="POST":
        pdf_file = request.FILES["pdf_file"]
        institute_name = Institutes.objects.filter(user=request.user).get()
        industry = Openings.objects.filter(id=ic).get().industry
        opening=Openings.objects.filter(id=ic).get()
        name=request.POST.get("name")
        print(request.FILES)
        
        obj=consent_form.objects.create(name=name, pdf_file=pdf_file, institute_name=institute_name, industry=industry,Openings=opening)
        obj.save()
        
    context={"institute":pk,"openings":ic}
    return render(request,'institute_dashboard/consent_form.html',context)
    


def make_random_password( length=10, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'):
        from random import SystemRandom as random
        return ''.join([random().choice(allowed_chars) for i in range(length)])


def application(request,pk,ic):
    openings = Openings.objects.get(id=ic)
    
    profile = Profile.objects.filter(institute = Institutes.objects.filter(user=request.user).get()).filter(user__groups=4).all()
    context = {'openings':openings, 'users':profile , 'institute':pk}
    print(request)
    if request.method=="POST":
            print(request.POST)
            s = request.POST.getlist("chk[]")
            print(s)

            for i in s:
                print(i)
                prof=Profile.objects.get(pk=i)
                user=User.objects.get(pk=prof.user.id)  
                openings = Openings.objects.get(id=ic)
                institute = Institutes.objects.filter(user = request.user).get()
                #profile = Profile.objects.filter(user = request.user).get()
                print(user,openings,institute)
                ob = Application.objects.create(user=user,openings=openings,institute=institute)
                ob.save()
    return render(request,"institute_dashboard/apply_openings.html",context)    

@login_required(login_url=loginPage)
@allowed_users(allowed_roles=["student"])
def student_applications(request):
    applications = Application.objects.all()
    context = {'applications':applications}
    return render(request, 'student_applications.html', context)

@login_required(login_url=loginPage)
@allowed_users(allowed_roles=["student"])
def delete_application(request,pk):
    applications = Application.objects.get(id=pk)
    applications.delete()
    return redirect('student_applications')

@login_required(login_url=loginPage)
@allowed_users(allowed_roles=["industry"])
def deleteopening(request,pk):
    openings = Openings.objects.get(id=pk)
    openings.delete()
    return redirect('openings')


def send_mails(request):
    if request.method == 'POST':
        students = Profile.objects.all()  

        for student in students:
            action = request.POST.get(f'action_{student.id}')
            
            if action == 'selected':
                send_student_mail(student, 'You have been selected!')
            elif action == 'schedule':
                send_student_mail(student, 'Your interview is scheduled.')
            elif action == 'consideration':
                send_student_mail(student, 'You are under consideration.')
            elif action == 'reject':
                send_student_mail(student, 'Unfortunately, you have been rejected.')

        messages.success(request, "Emails have been sent successfully!")
        return redirect('/dashboard/send_mails.html')  
    else:
        # Handle GET requests or other cases
        return redirect('/dashboard/send_mails.html')

def send_student_mail(student, message_body):
    subject = 'Application Status Update'
    message = message_body
    recipient = 'example@gmail.com'

    print(recipient)

    try:
        send_mail(
            subject,
            message,
            'example@gmail.com',  
            [recipient],
            fail_silently=False,
        )
        print(f"Email sent to {recipient}")
    except Exception as e:
        print(f"Failed to send email to {recipient}: {e}")  # Lo



# def consent(request):
#     if consent object false:
#         return render(request, 'consent.html')
#     else if consent object true:
#         return redirect('apply_openings')



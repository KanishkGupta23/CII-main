from sys import displayhook
from django.db import models
from django.forms import DateField, DateTimeField
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver





class Industries(models.Model):
    DOMAIN_CHOICES = (
    ('Business','Business'),
    ('Engineering', 'Engineering'),
    ('Finance', 'Finance'),
    ('Healthcare', 'Healthcare'),
    ('IT', 'IT'),
    ('Law', 'Law'),
    ('Marketing', 'Marketing'),
    ('Media', 'Media'),
    ('Science', 'Science'),
    ('Manufacturing', 'Manufacturing'),
    ('Teaching', 'Teaching'),
    ('Other', 'Other'),

    )
    State_choices=(
    ("Madhya Pradesh","Madhya Pradesh"),
    ("Assam","Assam"),
    ("Bihar","Bihar"),
    ("Andhra Pradesh","Andhra Pradesh"),
    ("","")
    )
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    name=models.CharField(max_length=200,null=True)
    description=models.TextField(max_length=500,null=True)
    logo=models.ImageField(upload_to="images/industries/",null=True ,default='images/industries/default.jpg')
    registration_date=models.DateField(null=True,blank=True)
    estb_year=models.DateField(null=True,blank=True)
    cii_id=models.IntegerField()
    website=models.URLField(null=True,blank=True)
    contact_num=models.IntegerField(null=True,blank=False)
    email_id=models.EmailField(null=True,blank=False)
    address=models.TextField(max_length=500,null=True)
    city=models.TextField(max_length=200,null=True)
    state=models.CharField(max_length=20, choices=State_choices, default='______')
    pincode=models.IntegerField(null=True,blank=False)
    country=models.TextField(max_length=200,null=True)
    verified=models.BooleanField(default=False)
    domain=models.CharField(max_length=20, choices=DOMAIN_CHOICES, default='______')
    
    def __str__(self):
        return self.name

class Institutes(models.Model):
    DOMAIN_CHOICES = (
    ('Demo0','Demo0'),
    ('Demo1', 'Demo1'),
    ('Demo2', 'Demo2'),
    ('Demo3', 'Demo3'),
    ('Demo4', 'Demo4'),
    ('Demo5', 'Demo5'),
    ('Demo6', 'Demo6'),
    ('Demo7', 'Demo7'),
    ('Demo8', 'Demo8'),
    ('Demo9', 'Demo9'),
    ('Demo10', 'Demo10'),
    ('Demo11', 'Demo11'),
    )

    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    name=models.CharField(max_length=200,null=True)
    description=models.TextField(max_length=500,null=True)
    logo=models.ImageField(upload_to="images/institutes/",null=True ,default='images/institutes/default.jpg')
    registration_date=models.DateField(null=True,blank=True)
    estb_year=models.DateField(null=True,blank=True)
    cii_id=models.IntegerField()
    website=models.URLField(null=True,blank=True)
    contact_num=models.IntegerField(null=True,blank=False)
    email_id=models.EmailField(null=True,blank=False)
    address=models.TextField(max_length=500,null=True)
    city=models.CharField(max_length=200,null=True)
    state=models.CharField(max_length=200,null=True)
    pincode=models.IntegerField(null=True,blank=False)
    country=models.CharField(max_length=200,null=True)
    verified=models.BooleanField(default=False)
    domain=models.CharField(max_length=20, choices=DOMAIN_CHOICES, default='______')
    
    def __str__(self):
        return self.name
    
class Profile(models.Model):
    DEGREE_CHOICES = (
    ('______','______'),
    ('______', '______'),
    )
    JOBS_CHOICES = (
    ('______','______'),
    ('______', '______'),
    )
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    name=models.CharField(max_length=200,null=True)
    headline=models.TextField(max_length=500,null=True,blank=True)
    currently_emp=models.BooleanField(default=True,blank=True)
    last_educational_degree=models.CharField(max_length=20, choices=DEGREE_CHOICES, default='______')
    institute=models.ForeignKey(Institutes,on_delete=models.SET_NULL,null=True,default=None)
    open_for_jobs=models.BooleanField(default=True)
    resume=models.FileField(upload_to="pdf/resume/",null=True ,default='pdf/resume.pdf')
    past_experience=models.IntegerField(validators=[MinValueValidator(0)],default=0, blank=True, null=True)
    skills=models.TextField(max_length=500,null=True)
    linkedin_link=models.URLField(null=True,blank=True)
    github = models.URLField(null=True,blank=True)
    job_cat=models.CharField(max_length=20, choices=JOBS_CHOICES, default='______')
    contact_num=models.IntegerField(null=True,blank=False)
    email_id=models.EmailField(null=True,blank=False)
    profile_pic=models.ImageField(upload_to="profile_pic/",null=True ,default='profile_pic/default.jpg')
   # company=models.ForeignKey(Industries,on_delete=models.SET_NULL,null=True,default=None)
   #applications = models

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class Openings(models.Model):
    id=models.AutoField(primary_key=True)
    job_title=models.TextField(max_length=200,null=True)
    description=models.TextField(max_length=500,null=True)
    # logo=models.ImageField(upload_to="images/openings/",null=True ,default='images/openings/default.jpg')
    key_skills=models.TextField(max_length=200, null=True)
    opening_date=models.DateField(null=True,blank=True)
    city=models.TextField(max_length=200,null=True)
    state=models.TextField(max_length=200,null=True)
    stipend=models.IntegerField(null=True,blank=False)
    past_experience_required=models.IntegerField(validators=[MinValueValidator(0)],default=0, blank=True, null=True)
    industry=models.ForeignKey(Industries,on_delete=models.SET_NULL,null=True)
    apply_by=models.DateField(null=True,blank=True)

    def __str__(self):
        return self.job_title

class Consultancy(models.Model):
    Domain_Choices = (
    ('Demo1','Demo1'),
    ('Demo2', 'Demo2'),
    ('Demo3', 'Demo3'),
    ('Demo4', 'Demo4'),
    ('Demo5', 'Demo5'),
    ('Demo6', 'Demo6'),
    ('Demo7', 'Demo7'),
    ('Demo8', 'Demo8'),
    ('Demo9', 'Demo9'),
    )
    Category_Choices = (
    ('Hardware','Hardware'),
    ('Software', 'Software'),
    ('Embedded', 'Embedded'),
    ('Networking', 'Networking'),
    ('Web', 'Web'),
    ('App', 'App'),
    ('AI', 'AI'),
    ('ML', 'ML'),
    )
    problem=models.TextField(max_length=200,null=True)
    problem_description=models.TextField(max_length=500,null=True)
    domain=models.CharField(max_length=20, choices=Domain_Choices, default='______')
    category=models.CharField(max_length=20, choices=Category_Choices, default='______')
    consultancy_date=models.DateField(null=True,blank=True)
    industry=models.ForeignKey(Industries,on_delete=models.SET_NULL,null=True)
    apply_by=models.DateField(null=True,blank=True)
    
    def __str__(self):
        return self.problem
    
class Application(models.Model):
    application_date=models.DateTimeField(null=True,blank=True,auto_now_add=True)
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    openings=models.ForeignKey(Openings,on_delete=models.SET_NULL,null=True)
    institute = models.ForeignKey(Institutes,on_delete=models.SET_NULL,null=True)
    
    def str(self):
        return self.user.username
    

class stud_data_upload(models.Model):
    institute_name = models.ForeignKey(User,on_delete = models.SET_NULL,null=True)
    excel_file = models.FileField(upload_to='instittute_excelfile', blank = True)
    insertion_time = models.DateTimeField(auto_now_add=True)


class institute_applied(models.Model):
    institute_name = models.ForeignKey(Institutes,on_delete = models.SET_NULL,null=True)
    industry = models.ForeignKey(Industries,on_delete = models.SET_NULL,null=True)
    approved = models.CharField(max_length=200,null=True)
    status = models.CharField(max_length=20, default='Pending')
    date = models.DateTimeField(null=True,blank=True,auto_now_add=True)
    applied = models.BooleanField(default=False)
    name = models.TextField(max_length=200,null=True)
    pdf_file = models.FileField(upload_to='institute_pdf',default='institute_pdf/pdfdemo.pdf', blank = False)

class consent_form(models.Model):
    id=models.AutoField(primary_key=True)
    institute_name = models.ForeignKey(Institutes,on_delete = models.SET_NULL,null=True)
    industry = models.ForeignKey(Industries,on_delete = models.SET_NULL,null=True)
    Openings = models.ForeignKey(Openings,on_delete = models.SET_NULL,null=True)
    name=models.TextField(max_length=200,null=True)
    pdf_file = models.FileField(upload_to='consent_pdf',default='consent_pdf/pdfdemo.pdf', blank = False)
    date = models.DateTimeField(null=True,blank=True,auto_now_add=True)
    approved = models.BooleanField( default=False)

    def str(self):
        return self.institute_name+self.industry+self.name


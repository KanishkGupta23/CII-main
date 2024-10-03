from django.forms import ModelForm, NumberInput
from django.contrib.auth.models import User
from django import forms
from .models import Industries
from .models import Institutes
from .models import Openings
from .models import Profile



# class CreateUserForm(UserCreationForm):
# 	class Meta:
# 		model = User
# 		fields = ['username', 'email', 'password1', 'password2']
class Industryregistrationform(ModelForm):
	required_css_class="required-field"
	error_css_class="error-field"
	name=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Your name"}))
	description=forms.CharField(widget=forms.Textarea(attrs={"class":"form-control","placeholder":"Add Description","type":"textarea","rows":3}))
	email_id=forms.EmailField(widget=forms.EmailInput(attrs={"class":"form-control mt-2","placeholder":"Email"}))
	address=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"add address"}))
	city=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"add city"}))
	registration_date=forms.DateField(label="Date", widget=NumberInput(attrs={'type':'date','class':'form-control'}))
	estb_year=forms.DateField(label="Date", widget=NumberInput(attrs={'type':'date','class':'form-control'}))
	country=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"add Country"}))
	class Meta:
		model = Industries
		fields = "__all__"
	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)
		for field in self.fields:
			new_Data={"class":"form-control"}
			self.fields[str(field)].widget.attrs.update(
				new_Data
			)
		

class Instituteregistrationform(ModelForm):
	required_css_class="required-field"
	error_css_class="error-field"
	name=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Your name"}))
	description=forms.CharField(widget=forms.Textarea(attrs={"class":"form-control","placeholder":"Add Description","type":"textarea","rows":3}))
	email_id=forms.EmailField(widget=forms.EmailInput(attrs={"class":"form-control mt-2","placeholder":"Email"}))
	# logo=forms.ImageField(widget=forms.FileInput(attrs={"class":"form-control mt-2","placeholder":"Logo"}))
	address=forms.CharField(widget=forms.Textarea(attrs={"class":"form-control","placeholder":"Add address","type":"textarea","rows":3}))
	city=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Add city"}))
	registration_date=forms.DateField(label="Date", widget=NumberInput(attrs={'type':'date','class':'form-control'}))
	estb_year=forms.DateField(label="Date", widget=NumberInput(attrs={'type':'date','class':'form-control'}))
	country=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Add Country"}))
	state=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Add State"}))
	cii_id=forms.CharField(widget=forms.NumberInput(attrs={"class":"form-control","placeholder":"CII ID"}))
	website=forms.CharField(widget=forms.URLInput(attrs={"class":"form-control","placeholder":"Website"}))
	contact_num=forms.CharField(widget=forms.NumberInput(attrs={"class":"form-control","placeholder":"Contact Number"}))
	pincode=forms.CharField(widget=forms.NumberInput(attrs={"class":"form-control","placeholder":"Pincode"}))
	class Meta:
		model = Institutes
		fields = "__all__"
	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)
		for field in self.fields:
			new_Data={"class":"form-control"}
			self.fields[str(field)].widget.attrs.update(
				new_Data
			)


class AddInternshipform(ModelForm):
	job_title=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Job Title"}))
	description=forms.CharField(widget=forms.Textarea(attrs={"class":"form-control","placeholder":"Add Description","Type":"textarea","rows":3}))
	opening_date=forms.DateField(label="Date", widget=NumberInput(attrs={'type':'date','class':'form-control'}))
	industry=forms.ModelChoiceField(queryset=Industries.objects.all(),widget=forms.Select(attrs={"placeholder":"Select Industry","class":"form-control"}))
	key_skills=forms.CharField(widget=forms.Textarea(attrs={"class":"form-control","placeholder":"Add Skills","Type":"textarea","rows":3}))
	city=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"City"}))
	state=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"State"}))
	stipend=forms.CharField(widget=forms.NumberInput(attrs={"class":"form-control","placeholder":"Stipend"}))
	past_experience_required=forms.CharField(widget=forms.NumberInput(attrs={"class":"form-control","placeholder":"Experience in Years"}))
	apply_by=forms.DateField(label="Last Date to Apply", widget=NumberInput(attrs={'type':'date','class':'form-control'}))

	class Meta:
		model = Openings
		fields = "__all__"


class ProfileUpdate(ModelForm):
	EDUCATION_CHOICES = Profile.DEGREE_CHOICES
	required_css_class="required-field"
	error_css_class="error-field"
	name=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Your name"}))
	email_id=forms.EmailField(widget=forms.EmailInput(attrs={"class":"form-control mt-2","placeholder":"Email"}))
	contact_num=forms.CharField(widget=forms.NumberInput(attrs={"class":"form-control","placeholder":"Contact Number"}))
	currently_emp=forms.CheckboxInput(attrs={"class":"form-control","placeholder":"Currently Employed"})
	last_educational_degree=forms.ChoiceField(choices=EDUCATION_CHOICES,widget=forms.Select(attrs={"class":"form-control","placeholder":"Last Educational Degree"}))
	linkedin_link=forms.URLField(widget=forms.URLInput(attrs={"class":"form-control","placeholder":"LinkedIn Link"}))

	class Meta:
		model = Profile
		fields = "__all__"
	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)
		for field in self.fields:
			new_Data={"class":"form-control"}
			self.fields[str(field)].widget.attrs.update(new_Data)
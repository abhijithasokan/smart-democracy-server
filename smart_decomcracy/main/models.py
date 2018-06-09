from django.db import models
from django.contrib.auth.hashers import is_password_usable,make_password,check_password

# Create your models here.

'''
Assumptions:
	user doesn't forget userid
'''


from django.db.models.signals import pre_save


class Constituency(models.Model):
	models.AutoField(primary_key=True)
	constituency_name = models.CharField(max_length=30)
	constituency_mla = models.ForeignKey('MLA',on_delete=models.CASCADE,null=True,related_name='cmla')
	indexes = [
		models.Index(fields=['constituency_name',]),
	]

	def __str__(self):
		return self.constituency_name


class User(models.Model):
	name = models.CharField(max_length=30, null=False)
	voter_id = models.CharField(max_length=20, unique=True, null=False)
	user_id = models.CharField(max_length=20, primary_key=True)
	hashed_password = models.CharField(max_length=40, null=False)
	
	constituency = models.ForeignKey(Constituency, on_delete=models.CASCADE)


	indexes = [
		models.Index(fields=['voter_id',]),
	]

	def __init__(self,*args,**kwargs):
		super(User,self).__init__(*args,**kwargs)
		self.old_pass = self.hashed_password

	@classmethod
	def isIdAvailable(cls,user_id):
		return not cls.objects.filter(user_id=user_id).exists()

	
	@classmethod
	def create(cls,name,voter_id,user_id,password,constituency_name):
		if cls.isIdAvailable(user_id):
			return None		#if user is already registered

		constituency, _ =  Constituency.objects.get_or_create(constituency_name=constituency_name)

		x = cls(name=name, 
			voter_id=voter_id, 
			user_id = user_id, 
			hashed_password = make_password('%s_%s'%(user_id,password)),
			constituency=constituency
		)
		x.save()
		return x


	@classmethod
	def getUser(cls,user_id,password):
		usr_obj = cls.objects.get(user_id=user_id)
		if check_password('%s_%s'%(user_id,password),usr_obj.hashed_password):
			return usr_obj
		return None





class MLA(models.Model):
	name = models.CharField(max_length=30)
	user_id = models.CharField(max_length=20, primary_key=True)
	hashed_password = models.CharField(max_length=40)
	constituency = models.ForeignKey(Constituency,on_delete=models.CASCADE)

	def __init__(self,*args,**kwargs):
		super(MLA,self).__init__(*args,**kwargs)
		self.old_pass = self.hashed_password

	@classmethod
	def create(self,name,user_id,password,constituency_name):
		constituency, _ =  Constituency.objects.get_or_create(constituency_name=constituency_name)
		x = cls(
				name=name, 
				user_id = user_id, 
				hashed_password = make_password('%s_%s'%(user_id,password)),
				constituency=constituency
			)
		x.save()
		return x

	def __str__(self):
		return '%20s,%10s'%(self.name,self.constituency)


def handle_password(sender, instance, *args, **kwargs):
	if instance.hashed_password!=instance.old_pass:
		instance.hashed_password = make_password('%s_%s'%(instance.user_id,instance.hashed_password))
		instance.old_pass = instance.hashed_password

pre_save.connect(handle_password, sender=MLA)
pre_save.connect(handle_password, sender=User)
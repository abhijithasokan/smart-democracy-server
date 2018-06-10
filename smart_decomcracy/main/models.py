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
		if not cls.isIdAvailable(user_id):
			return None		#if user is already registered

		constituency, _ =  Constituency.objects.get_or_create(constituency_name=constituency_name)

		x = cls(name=name, 
			voter_id=voter_id, 
			user_id = user_id, 
			hashed_password = make_password('%s_%s'%(user_id,password)),
			constituency=constituency
		)
		x.save()
		print(x)
		return x


	@classmethod
	def getUser(cls,user_id,password):
		usr_obj = cls.objects.get(user_id=user_id)
		if check_password('%s_%s'%(user_id,password),usr_obj.hashed_password):
			return usr_obj
		return None

	def __str__(self):
		return '%s | %s'%(self.name,self.constituency)





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





#======================================================================================================================
#======================================================================================================================
#======================================================================================================================


class Issue(models.Model):
	#keys
	issue_id = models.AutoField(primary_key=True)
	creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	constituency = models.ForeignKey(Constituency, on_delete=models.CASCADE)

	official = models.BooleanField(default=False)

	

	time_created = models.DateTimeField(auto_now_add=True)
	heading = models.CharField(max_length=100)
	description = models.CharField(max_length=1000)

	upvotes = models.PositiveIntegerField(default=0)
	downvotes = models.PositiveIntegerField(default=0)

	resolved = models.BooleanField(default=False)


	indexes = [
		models.Index(fields=['creator',]),
		models.Index(fields=['constituency',]),
	]

	@classmethod
	def create(cls,heading,description,creator):
		official =  isinstance(creator,MLA)
		constituency = creator.constituency

		x = cls(
				heading = heading,
				description = description,
				official = official,
				creator = (None if official else creator),
				constituency = constituency,
			)
		x.save()
		return x

	@classmethod
	def getIssues(cls,user):
		data = []
		for issue in Issue.objects.filter(constituency=user.constituency,resolved=False).order_by('-upvotes', 'downvotes', '-time_created'):
			data.append({
					'heading' : issue.heading,
					'issue_id' : issue.issue_id,
					'upvotes' : issue.upvotes,
					'downvotes' : issue.downvotes,
				})
		return data

	def upvote(self,user):
		if VoteCast.isEligible(user,'issue',self.issue_id):
			self.upvotes += 1
			self.save()
			VoteCast.cast(user,'issue',self.issue_id)


	def downvote(self,user):
		if VoteCast.isEligible(user,'issue',self.issue_id):
			self.downvotes += 1
			self.save()
			VoteCast.cast(user,'issue',self.issue_id)


	def __str__(self):
		return '%s | %s'%(self.heading,self.constituency)



class Solution(models.Model):
	solution_id = models.AutoField(primary_key=True)
	issue = models.ForeignKey(Issue,on_delete=models.CASCADE)
	creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	official = models.BooleanField(default=False)


	time_created = models.DateTimeField(auto_now_add=True)
	heading = models.CharField(max_length=100)
	description = models.CharField(max_length=1000)

	upvotes = models.PositiveIntegerField(default=0)
	downvotes = models.PositiveIntegerField(default=0)



	@classmethod
	def create(cls,heading,description,issue_id,creator):
		official =  isinstance(creator,MLA)

		x = cls(
				heading = heading,
				description = description,
				official = official,
				creator = (None if official else creator),
				issue_id = issue_id,
			)
		x.save()
		return x



	@classmethod
	def getSolutions(cls,issue_id):
		issue = Issue.objects.get(issue_id=issue_id)

		if issue.official:
			creator = issue.constituency.constituency_mla
		else:
			creator = issue.creator
		
		data = [ 
			{
					'upvotes': issue.upvotes,
					'downvotes' : issue.downvotes,
					'heading' : issue.heading,
					'description' : issue.description,
					'official' : issue.official,
					'creator' : creator.name,
					'solution_id' : issue.issue_id,
			}
		]

		for sol in Solution.objects.filter(issue_id=issue_id).order_by('-upvotes', 'downvotes', '-time_created'):
			if sol.official:
				creator = sol.issue.constituency.constituency_mla
			else:
				creator = sol.creator


			data.append({
					'upvotes': sol.upvotes,
					'downvotes' : sol.downvotes,
					'heading' : sol.heading,
					'description' : sol.description,
					'official' : sol.official,
					'creator' : creator.name,
					'solution_id' : sol.solution_id,
				})

		print("Data here: ",data)
		return data




	def upvote(self,user):
		if VoteCast.isEligible(user,'solution',self.solution_id):
			self.upvotes += 1
			self.save()
			VoteCast.cast(user,'solution',self.solution_id)


	def downvote(self,user):
		if VoteCast.isEligible(user,'solution',self.solution_id):
			self.downvotes += 1
			self.save()
			VoteCast.cast(user,'solution',self.solution_id)


	def __str__(self):
		return '%s | %s'%(self.issue,self.heading)





# =========================================
# =========================================


class Poll(models.Model):
	poll_id = models.AutoField(primary_key=True)
	creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	constituency = models.ForeignKey(Constituency, on_delete=models.CASCADE)

	official = models.BooleanField(default=False)

	

	time_created = models.DateTimeField(auto_now_add=True)
	heading = models.CharField(max_length=100)
	description = models.CharField(max_length=1000)

	vote_count =models.PositiveIntegerField(default=0)

	closed = models.BooleanField(default=False)


	indexes = [
		models.Index(fields=['creator',]),
		models.Index(fields=['constituency',]),
	]

	@classmethod
	def create(cls,heading,description,creator,options):
		official =  isinstance(creator,MLA)
		constituency = creator.constituency

		x = cls(
				heading = heading,
				description = description,
				official = official,
				creator = (None if official else creator),
				constituency = constituency,
			)
		
		x.save()

		start = 1
		for option in options:
			Option.objects.create(choice_name=option,poll=x,option_num=start).save()
			start += 1
		
		return x

	@classmethod
	def getPolls(cls,user):
		data = []
		for poll in Poll.objects.filter(constituency=user.constituency,closed=False).order_by('-vote_count', '-time_created'):
			data.append({
					'heading' : poll.heading,
					'description' : poll.description,
					'poll_id' : poll.poll_id,
					'options' : [ e.choice_name for e in Option.objects.filter(poll=self) ]

				})
		return data

	def getPollResult(self):
		count = self.vote_count or 1
		return  [ (e.choice_name,e.votes/count) for e in Option.objects.filter(poll=self) ]

	def vote(self,option_num):
		# PERFORM CHECK
		self.vote_count += 1
		
		p = Option.objects.get(option_num=option_num)
		p.votes += 1
		p.save()


	def __str__(self):
		return '%s'%(self.heading)


class Option(models.Model):
	option_num = models.PositiveIntegerField()
	choice_name = models.CharField(max_length=30)
	poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
	votes = models.PositiveIntegerField(default=0)

	indexes = [
		models.Index(fields=['poll',]),
	]

	def __str__(self):
		return '%s | %s'%(self.poll, self.choice_name)



class VoteCast(models.Model):
	VOTE_TYPES = ['issue','solution','poll']
	user_id = models.CharField(max_length=20)
	official = models.BooleanField(default=False)
	vote_type = models.PositiveSmallIntegerField()
	vote_id  = models.PositiveIntegerField()

	indexes = [
		models.Index(fields=['user_id',]),
	]

	@classmethod
	def isEligible(cls,user,vote_type,vote_id):
		vote_type=VoteCast.VOTE_TYPES.index(vote_type)
		official = isinstance(user,MLA)
		return not VoteCast.objects.filter(user_id=user.user_id,
			official=official,vote_type=vote_type,vote_id=vote_id).exists()



	@classmethod
	def cast(cls,user,vote_type,vote_id):
		vote_type=VoteCast.VOTE_TYPES.index(vote_type)
		official = isinstance(user,MLA)
		cls(
			user_id = user.user_id,
			official = official,
			vote_type = vote_type,
			vote_id = vote_id
		).save()





from users.models import User 

# create user
def createuser(n, e, p, pos):
	from users.models import User 
	u = User.objects.create_user(username=n,
	                                 email=e,
	                                 password=p)
	u.position = pos
	u.save()

# User.objects.all().exclude(username='admin').delete()
# name = ["Henry", "Martin", "Ben", "Steven", "Eric", "BugDeveloper", "BugManager", "BugProductOwner", "noDeveloper", "noManager"]
# for i in name:
# 	if i == "BugManager" or i == "noManager":
# 		createuser(i, 'leehenry908@gmail.com', '1234', '2')
# 	else:	
# 		createuser(i, 'leehenry908@gmail.com', '1234', '3')

createuser('SM', 'leehenry908@gmail.com', '1234', '2')

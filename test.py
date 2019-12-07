from users.models import User 
from project.models import Project
from sprintBacklog.models import Sprint, Task
from productBacklog.models import PBI

# create user
def createuser(n, e, p, pos):
	from users.models import User 
	u = User.objects.create_user(username=n,
	                                 email=e,
	                                 password=p)
	u.position = pos
	u.save()

# User.objects.all().exclude(username='admin').delete()
name = ["Henry", "Martin", "Ben", "Steven", "Eric", "BugDeveloper", "BugManager", "BugProductOwner", "noDeveloper", "noManager"]
# for i in name:
# 	if i == "BugManager" or i == "noManager":
# 		createuser(i, 'leehenry908@gmail.com', '1234', '2')
# 	else:	
# 		createuser(i, 'leehenry908@gmail.com', '1234', '3')


status = ["To Do", "Doing", "Done"]
#fill this in (pbi,sprint,task to be included in sprint 3) ##########
priority = [1, 2, 3, 4, 5]
title = ["log-in and log-out functionality", "Create new project", "Invite developer", "Invite manager", "Individual time-tracking"]
"""
	title, effort, owner, status
	template: ("taskA", 10, name[0], status[0])
	index for name : 0 - 3
"""
#ALL TO-Do
# task = [[ ("create user object for registration", 8, name[0], status[0]), ("create login system to grant access", 10, name[3], status[0]) ], # pbi 1
# 	[ ("interface for user to insert details to create project", 6, name[1], status[0]), ("permitted user can access project after project creation", 4, name[2], status[0]) ], # pbi 2
# 	[ ("send invitation email to selected developers", 5, name[2], status[0]), ("include invited developer to the project after confirmation", 3, name[1], status[0]) ], # pbi 3
# 	[ ("send invitation email to selected manager", 2, name[3], status[0]), ("include invited manager into porject after confirmation", 2, name[0], status[0]) ], # pbi 4
# 	[ ("access profile of developer", 4, name[0], status[0]), ("create a profile showing the details of workload of a developer", 6, name[0], status[0]) ] # pbi 5
#        ]

#middle of sprint
# task = [[ ("create user object for registration", 8, name[0], status[2]), ("create login system to grant access", 10, name[3], status[1]) ], # pbi 1
# 	[ ("interface for user to insert details to create project", 6, name[1], status[1]), ("permitted user can access project after project creation", 4, name[2], status[0]) ], # pbi 2
# 	[ ("send invitation email to selected developers", 5, name[2], status[2]), ("include invited developer to the project after confirmation", 3, name[1], status[1]) ], # pbi 3
# 	[ ("send invitation email to selected manager", 2, name[3], status[1]), ("include invited manager into porject after confirmation", 2, name[0], status[1]) ], # pbi 4
# 	[ ("access profile of developer", 4, name[0], status[0]), ("create a profile showing the details of workload of a developer", 6, name[0], status[1]) ] # pbi 5
#        ]
#all done
task = [[ ("create user object for registration", 8, name[0], status[2]), ("create login system to grant access", 10, name[3], status[2]) ], # pbi 1
	[ ("interface for user to insert details to create project", 6, name[1], status[2]), ("permitted user can access project after project creation", 4, name[2], status[2]) ], # pbi 2
	[ ("send invitation email to selected developers", 5, name[2], status[2]), ("include invited developer to the project after confirmation", 3, name[1], status[2]) ], # pbi 3
	[ ("send invitation email to selected manager", 2, name[3], status[2]), ("include invited manager into porject after confirmation", 2, name[0], status[2]) ], # pbi 4
	[ ("access profile of developer", 4, name[0], status[2]), ("create a profile showing the details of workload of a developer", 6, name[0], status[2]) ] # pbi 5
       ]

#####################################################################

ESP = 0 
details = "details"

pj = Project.objects.get(title="BackTrack")
sprint = Sprint.objects.get(title="Sprint3")
PBI.objects.filter(project=pj).delete()
Task.objects.filter(sprint=sprint).delete()
for i in range(len(title)):
	pbi = PBI.objects.create(	priority=priority[i],
								title=title[i],
								ESP=ESP,
								details=details,
								project=pj)
	pbi.sprint.add(sprint)
	pbi.save()
	for t in task[i]:
		Task.objects.create(title=t[0],
							effort=t[1],
							details=details,
							sprint=sprint,
							PBI=pbi,
							task_owner=User.objects.get(username=t[2]),
							status=t[3])





'''
Authors: Kenneth Bello and Hongshan Liu

Homework 3
'''

import math
import random
from collections import defaultdict
import operator

history = defaultdict(int)

#Manhattan Distance
def manhattan_dist(user1, user2):
	return (abs(user2[0]-user1[0])+ abs(user2[1]-user1[1]))

#kleinberg's 2 dimensional network structure
def network(j,k,u):

	grid = [[0,]*k for row in xrange(j)]
	alpha = 2

	neighbor = [[0,1],[1,0],[-1,0],[0,-1]]
	users = defaultdict(list)
	check_user = []

	#User network
	for user in xrange(u):
		x = random.randint(0,k-1)
		y = random.randint(0,j-1)
		while [x,y] in check_user:
			y = random.randint(0,j-1)
			x = random.randint(0,k-1)
		check_user.append([x,y])
		grid[x][y] += 1

		#short range neighbor
	for vUser in check_user:
		for n in neighbor:
			x_n_loc = (vUser[0] - n[0])
			y_n_loc = (vUser[1]- n[1])
			if (x_n_loc >= 0 and x_n_loc < k) and (y_n_loc >= 0 and y_n_loc < j) and grid[x_n_loc][y_n_loc] == 1:
				users[(vUser[0],vUser[1])].append([x_n_loc,y_n_loc])


		#long range neighbor
		max_y = max((j-vUser[1]-1),vUser[1])
		max_x = max((k-vUser[0]-1),vUser[0])
		mhd = max_x + max_y
		longR_user = []
		distance = math.ceil((random.random()**alpha) * mhd)
		if distance < 2:
			distance = 2

		for row in xrange(j):
			for col in xrange(k):
				if (manhattan_dist([vUser[0],vUser[1]],[col,row]) == distance) and grid[col][row] == 1:
					longR_user.append([col,row])
		
		if longR_user != []:
			users[(vUser[0],vUser[1])].append(random.choice(longR_user))


	for (k,v) in users.iteritems():
		for v in users[k]:
			history[(tuple(k),tuple(v))] = 0

	return users

def prefNetwork(j,k,u):

	grid = [[0,]*k for row in xrange(j)]
	alpha = 2

	neighbor = [[0,1],[1,0],[-1,0],[0,-1]]
	users = defaultdict(list)
	check_user = []
	num_edges = defaultdict(int)

	#User network
	for user in xrange(u):
		x = random.randint(0,k-1)
		y = random.randint(0,j-1)
		while [x,y] in check_user:
			y = random.randint(0,j-1)
			x = random.randint(0,k-1)
		check_user.append([x,y])
		grid[x][y] += 1

		#short range neighbor
	for vUser in check_user:
		for n in neighbor:
			x_n_loc = (vUser[0] - n[0])
			y_n_loc = (vUser[1]- n[1])
			if (x_n_loc >= 0 and x_n_loc < k) and (y_n_loc >= 0 and y_n_loc < j) and grid[x_n_loc][y_n_loc] == 1:
				users[(vUser[0],vUser[1])].append([x_n_loc,y_n_loc])


		#long range neighbor
		max_y = max((j-vUser[1]-1),vUser[1])
		max_x = max((k-vUser[0]-1),vUser[0])
		mhd = max_x + max_y
		longR_user = []
		distance = math.ceil((random.random()**alpha) * mhd)
		if distance < 2:
			distance = 2

		for row in xrange(j):
			for col in xrange(k):
				if (manhattan_dist([vUser[0],vUser[1]],[col,row]) == distance) and grid[col][row] == 1:
					longR_user.append([col,row])
		
		if longR_user != []:
			x = random.choice(longR_user)

			decision = random.randint(0,1)
			if len(num_edges) >=3 and decision == 0:
				edge_sort = sorted(num_edges.iteritems(), key = operator.itemgetter(1), reverse = True)[:3]
				long_user = random.choice(edge_sort)
				users[(vUser[0],vUser[1])].append(long_user[0])
				num_edges[long_user[0]] += 1

			else:
				users[(vUser[0],vUser[1])].append(tuple(x))
				num_edges[tuple(x)] += 1

	return users


def message(m, users, steps, send = None, rec = None, prev_sender = []):
	psender = prev_sender
	for msg in xrange(m):
		count = steps + 1
		if send == None and rec == None and prev_sender == []:
			sender = random.choice(users.keys())
			recipient = random.choice(users.keys())
			while recipient == sender:
				recipient = random.choice(users.keys())
			psender.append(sender)
			print "Sender: ", sender
			print "Recipient: ",recipient
		else:
			sender = send
			recipient = rec 
			psender.append(sender)

		send_n = users[sender]
		n_dict = {}
		min_d = 1000
		for n in send_n:
			if tuple(n) not in psender:
				n_dict[tuple(n)] = manhattan_dist(n, recipient)

		for (k,v) in n_dict.iteritems():
			min_d = min(min_d,v)

		close_n = ()
		for (k,v) in n_dict.iteritems():
			if v == min_d:
				close_n = k


		if recipient != close_n and close_n != ():
			return message(1, users, count, close_n, recipient, psender)
		elif close_n == ():
			print "Message failed. Dead End"
			return 0
		else:
			print "Message delivered!"
			return count

def weighted_connection(m, users, steps, send = None, rec = None, prev_sender = []):
	psender = prev_sender 
	for msg in xrange(m):
		count = steps + 1
		if send == None and rec == None and psender == []:
			sender = random.choice(users.keys())
			recipient = random.choice(users.keys())
			while recipient == sender:
				recipient = random.choice(users.keys())
			psender.append(sender)
			print "Sender: ", sender
			print "Recipient: ",recipient
		else:
			sender = send
			recipient = rec
			psender.append(sender)

		send_n = users[sender]
		n_dict = {}
		s_dict = {}
		min_d = 1000
		min_s = 1000
		max_history = 0
		for n in send_n:
			if tuple(n) not in psender:
				n_dict[tuple(n)] = manhattan_dist(n, recipient)

		for (k,v) in n_dict.iteritems():
			min_d = min(min_d,v)
			max_history = max(max_history, history[(sender,k)])
			s_dict[k] = min_d - max_history

		for (k,v) in s_dict.iteritems():
			min_s = min(min_s, v)

		close_n = ()
		for (k,v) in s_dict.iteritems():
			if v == min_s:
				close_n = k

		if recipient != close_n and close_n != ():
			return weighted_connection(1, users, count, close_n, recipient, psender)
		elif close_n == ():
			print "Message failed. Dead End"
			return 0
		else:
			print "Message delivered!"
			return count


def median(lists):
	med_list = sorted(lists)
	x = len(med_list)/2
	return med_list[x-1]

def mean(lists):
	x = 0
	for v in lists:
		x += v
	return x/(len(lists)-1)

def main():
	messages = 10
	j =10
	k =10

	"""
	-----------------Kleinberg's Model-------------------
	"""
	print "\n\n-----------------Kleinberg's Model-------------------\n"
	step_list = []
	#density 100%
	n = network(j,k,(j*k))
	#density 75%
	#n = network(j,k,((j*k)*(3/4)))
	#density 50%
	#n = network(j,k,(j*k/2))
	
	for m in xrange(messages):
		y = message(1,n,0,None,None,[])
		print y, "Steps!\n"
		step_list.append(y)

	print "\nStatistics:"
	print median(step_list), "median!"
	print mean(step_list), "mean!\n\n"

	"""
	------------------Pref Attachment---------------------
	"""
	print "\n\n------------------Pref Attachment---------------------\n"
	step_list1 = []
	#density 100%
	#pN = prefNetwork(j,k,(j*k)) all user
	#density 75%
	pN = prefNetwork(j,k,((j*k)*3/4))
	#density 50%
	#pN = prefNetwork(j,k,((j*k)/2)) 

	for m in xrange(messages):
		x = message(1,pN,0,None,None,[])
		print x, "Steps!\n"
		step_list1.append(x)

	print "\nStatistics:"
	print median(step_list1), "median!"
	print mean(step_list1), "mean!\n\n"
	


	"""
	PART 3
	"""

	print "\n\n---------------------weighted_connection---------------------\n"
	step_list2 = []
	step_list3 = []
	for wX in xrange(messages):
		wx = weighted_connection(1,n,0, None, None, [])
		print wx, "Steps!\n"
		step_list2.append(wx)

	print "\nKleinberg's Model"
	print "Statistics:"
	print median(step_list2), "median!"
	print mean(step_list2), "mean!\n\n"

	for wY in xrange(messages):
		wy = weighted_connection(1,pN,0, None, None, [])
		print wy, "Steps!\n"
		step_list3.append(wy)

	print "\nPref Attachment"
	print "Statistics:"
	print median(step_list3), "median!"
	print mean(step_list3), "mean!"

main()


###  CONFIGURATION ###

VERSION = '1.0.0'

USERAGEN = '''App: Ultimate Control
				Version: %s
				Description: Control Panel for Reddit. Read messages, reply to comments, swap accounts, etc.
				Known Issues: None
				Author: /u/Spedwards'''%VERSION



### /CONFIGURATION ###

import ctypes,getpass,html,os,re,warnings

from praw import *
r = Reddit(re.sub(r'\t+','',USERAGEN))

looping = True

USERNAME = None

commands = {
	'help': [
		['help','					List all the commands'],
		['help [command]','				Lists the syntax for the command']
	],
	'exit': [
		['exit','					Exit Ultimate Control']
	],
	'login': [
		['login','					Request username and password\n					then log in'],
		['login [username]','			Request password then log in'],
		['login [username] [password]','		Log into another account']
	],
	'unread': [ # requires login
		['unread','					Get all unread messages']
	],
	'reply': [
		['reply [id] [m/c]','			Request message input then send'],
		['reply [id] [m/c] [message]','		Send reply to comment/message']
	],
	'user': [
		['user [me/user] overview','			Get the user\'s comments'],
		['user [me/user] karma','			Get the user\'s karma'],
		['user [me/user] message','			Request subject and message input\n					then send'],
		['user [me/user] message [subject]','	Request message input then send'],
		['user [me/user] message [subject] [message]','	Send message'],
		['user available [username]','		See if username is taken'],
		['user create','				Request username and password\n					then create new account'],
		['user create [username]','			Request password then create account'],
		['user create [username] [password]','	Create new account']
	],
	'me': [
		['me name','					Get currently logged in username'],
		['me logged','				Is someone logged in?']
	],
	'shorthand': [
		['shorthand set [word] [command]','		Sets a shorthand for a command'],
		['shorthand rem [word]','			Removes a shorthand'],
		['shorthand get','				Get shorthands as string']
	],
	'clear': [
		['clear','					Clears the window']
	]
}

shorthands = {
	'help': ['?'],
	'clear': ['cls']
}

def title(x):
	if os.name == 'nt':
		ctypes.windll.kernel32.SetConsoleTitleW(x)
	else:
		import sys
		sys.stdout.write('\x1b]2;{}\x07'.format(x))

def out(x):
	print('...','%s\n'%x)

def cls():
	if os.name == 'nt':
		os.system('cls')
	else:
		os.system('clear')
	print('')

warnings.filterwarnings('ignore')

title('Ultimate Control v%s'%VERSION)

cls()
print('Initializing Ultimate Control v%s'%VERSION)

while looping:
	i = input(' $ ')
	args = i.split(' ')
	command = args[0]
	shorthand = False
	for z in shorthands:
		for x in shorthands[z]:
			if command == x:
				shorthand = True
				command = z
	if commands.get(command) is None and not shorthand:
		out('Invalid command')
		continue
	if command == 'help' or command == '?':							### HELP ###
		if len(args) == 1:
			for z in commands:
				for x in commands[z]:
					print(''.join(x))
			print('')
		elif len(args) == 2:
			z = args[1]
			if commands.get(z) is None:
				out('Invalid command')
				continue
			for x in commands[z]:
				print(''.join(x))
			print('')
		else:
			out('Too many arguments')
	elif command == 'exit':											### EXIT ###
		looping = False
	elif command == 'login':										### LOGIN ###
		if len(args) == 1:
			user = input('Username: ')
			pswd = getpass.getpass()
		elif len(args) == 2:
			user = args[1]
			pswd = getpass.getpass()
		elif len(args) == 3:
			user = args[1]
			pswd = args[2]
		elif len(args) > 3:
			out('Too many arguments')
			continue
		try:
			r.login(user,pswd)
			USERNAME = user
			out('Successfully logged in as %s'%USERNAME)
			title('Ultimate Control v%s - Logged in: %s'%(VERSION,USERNAME))
		except errors.InvalidUserPass as e:
			out('Invalid username or password')
	elif command == 'unread':										### UNREAD ###
		if USERNAME is None:
			out('Unread messages requires being logged in')
			continue
		un = r.get_unread()
		try:
			zzz = next(un)
		except StopIteration:
			out('No unread messages')
			continue
		for x in un:
			try:
				out('{}: {}\n'.format(x.id,html.unescape(re.sub('<[^<]+?>', '', html.unescape(x.body_html)))))
			except:
				out('Message contains unicode characters')
	elif command == 'reply':										### REPLY ###
		if len(args) < 3:
			out('Too few arguments\n{}\n{}'.format(commands['reply'][0][0],commands['reply'][0][1]))
			continue
		idType = 'c'
		if args[2].lower() == 'm':
			idType = 'm'
		if len(args) == 3:
			msg = input('Message: ')
			if idType=='c':
				if r.get_info(thing_id='t1_%s'%args[1]) is None:
					out('Invalid comment id')
					continue
				r.get_info(thing_id='t1_%s'%args[1]).reply(msg)
			else:
				try:
					m = r.get_message(args[1])
				except:
					out('Invalid message id')
					continue
				if m is None:
					out('Invalid message id')
					continue
				try:
					m.reply(msg)
					out('Reply sent')
				except:
					out('Error. Reply not sent')
		else:
			msg = args[3]
			if idType=='c':
				if r.get_info(thing_id='t1_%s'%args[1]) is None:
					out('Invalid comment id')
					continue
				back = r.get_info(thing_id='t1_%s'%args[1]).reply(msg)
				if back is None:
					out('Error. Reply not sent')
				else:
					out('Reply sent')
			else:
				try:
					m = r.get_message(args[1])
				except:
					out('Invalid message id')
					continue
				if m is None:
					out('Invalid message id')
					continue
				try:
					m.reply(msg)
					out('Reply sent')
				except:
					out('Error. Reply not sent')
	elif command == 'user':											### USER ###
		user = USERNAME
		if len(args) < 2:
			out('Too few arguments')
			continue
		if len(args) == 2:
			if args[1] != 'create':
				out('Invalid arguments')
				continue
			user = input('Username: ')
			if not r.is_username_available(user):
				out('{} is already taken'.format(user))
				continue
			pswd = getpass.getpass('Password for %s: '%user)
			try:
				r.create_redditor(user,pswd)
				out('User successfully created')
			except:
				out('Error. User not created')
			continue
		if len(args) >= 2:
			if args[1] == 'create' or args[1] == 'available':
				if args[1] == 'create':
					if len(args) == 3:
						user = args[2]
						pswd = None
					else:
						user = args[2]
						pswd = args[3]
					if not r.is_username_available(user):
						out('{} is already taken'.format(user))
						continue
					if pswd is None:
						pswd = getpass.getpass('Password for %s: ')
					try:
						r.create_redditor(user,pswd)
						out('User successfully created')
					except:
						out('Error. User not created')
				else:
					user = args[2]
					if r.is_username_available(user):
						out('Username is available')
					else:
						out('Username is not available')
				continue
			if args[1] != 'me':
				user = args[1]
			if r.is_username_available(user):
				out('{} does not exist'.format(user))
				continue
			u = r.get_redditor(user)
		if len(args) == 3:
			if args[2] == 'overview':
				i = 0
				o = u.get_overview()
				n = next(o)
				for i in range(5):
					if type(n) == objects.Comment:
						text = n.body
					else:
						text = n.selftext
						if text == '':
							continue
					out('%s: %s\n'%(n.id,text))
					n = next(o)
			elif args[2] == 'karma':
				out('{} - {}'.format(u.link_karma,u.comment_karma))
			elif args[2] == 'message':
				subject = input('Message subject: ')
				msg = input('Message: ')
				try:
					u.send_message(subject,msg)
					out('Message sent')
				except:
					out('Error. Message not sent')
			else:
				out('Incorrect arguments')
		elif len(args) == 4:
			msg = input('Message: ')
			try:
				u.send_message(args[3], msg)
				out('Message sent')
			except:
				out('Error. Message not sent')
		elif len(args) == 5:
			try:
				u.send_message(args[3],args[4])
				out('Message sent')
			except:
				out('Error. Message not sent')
		else:
			out('Too many arguments')
	elif command == 'me':											### ME ###
		if len(args) < 2:
			out('Too few arguments')
			continue
		if len(args) > 2:
			out('Too many arguments')
			continue
		if args[1] == 'name' or args[1] == 'logged':
			if USERNAME is None:
				out('No one is logged in')
			else:
				out('{} is currently logged in'.format(USERNAME))
	elif command == 'shorthand':									### SHORTHAND ###
		if len(args) < 3:
			out('Too few arguments')
			continue
		if len(args) > 4:
			out('Too many arguments')
			continue
		if args[1] == 'set':
			z = args[3]
			if commands.get(z) is None:
				out('{} is not a valid command'.format(z))
				continue
			taken = False
			for y in shorthands:
				for x in shorthands[y]:
					if x == args[2]:
						print('{} is already a shorthand for {}'.format(args[2],y))
						taken = True
						continue
					if taken: continue
				if taken: continue
			if taken: continue
			if shorthands.get(z) is None:
				shorthands[z] = [args[2]]
			else:
				shorthands[z].append(args[2])
			out('Shorthand created')
		elif args[1] == 'rem':
			rem = False
			for z in shorthands:
				for x in shorthands[z]:
					if x == args[2]:
						shorthands[z].remove(args[2])
						rem = True
						out('Shorthand removed')
						continue
					if rem: continue
				if rem: continue
			if rem: continue
			out('No shorthand found')
		else:
			out('Invalid arguments')
	elif command == 'clear' or command == 'cls':					### CLEAR ###
		cls()

import pytest
import json
from index import signin, login
from random import randint

def test_signin():
	i = str(randint(1,9))
	user = signin('user_test' + i,'user_test' + i)
	assert isinstance(user, dict)

	with open('./db/users.json', 'r') as users_file:
		users = json.load(users_file)
		new_users = users[:-1]
	
	with open('./db/users.json', 'w') as users_file:
		json.dump(new_users, users_file,indent=4)

def test_login():
	user = login('user','user')
	assert isinstance(user, dict)

pytest.main()
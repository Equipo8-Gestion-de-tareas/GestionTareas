import pytest
import json
from index import signin, login
from random import randint

def remove_last_user_added():
	with open('./db/users.json', 'r') as users_file:
		users = json.load(users_file)
		new_users = users[:-1]
	
	with open('./db/users.json', 'w') as users_file:
		json.dump(new_users, users_file,indent=4)

def test_correct_signin():
	i = str(randint(1,9))
	user = signin('user_test' + i,'user_test' + i)
	assert isinstance(user, dict)
	remove_last_user_added()

def test_signin_with_user_exists():
	signin('user_test', 'user_test')
	user = signin('user_test', 'user_test')
	assert user == -1
	remove_last_user_added()


def test_correct_login():
	user = login('user','user')
	assert isinstance(user, dict)

def test_login_with_user_not_exists():
	user = login('user_test','user_test')
	assert user == -1

def test_login_with_wrong_password():
	signin('user_test','user_test')
	user = login('user_test','user_test_password')
	assert user == -2
	remove_last_user_added()

pytest.main()
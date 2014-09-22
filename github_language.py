#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

  To use, complete your username below, and either provide
  your password, or generate an access token at 
  https://github.com/settings/applications#personal-access-tokens

"""

import requests, json
import sys
import os, os.path
from collections import defaultdict, Counter
import logging


GITHUB_USERNAME = 'skellystudios'
GITHUB_PASSWORD_OR_TOKEN = 'b80bb5b5bd8ddf6105711fea86c73b59bfd5c7ee'

auth = (GITHUB_USERNAME, GITHUB_PASSWORD_OR_TOKEN)


def main(args, help):
	try:
		username = args.username[0] #fine, as our CLI makes sure we've got the right number of args
		repos = get_repos(username)
		languages = count_repo_languages(repos)
	except:
		logging.error("Can't retrieve data for user %s - check your token/password is correct and you are connected to the internet." % username)
		print ""

	pick = pick_favourite_languages(languages)
	print pick 

def pick_favourite_languages(languages):
	
	if len(languages) < 1:
		logging.error("No repositories with tagged languages")
		return ""

	top_count = sorted(languages.values())[-1]
	favourites = [a for (a,b) in languages.items() if b == top_count]
	printable = ", ".join(favourites)
	return printable


def count_repo_languages(repos):
	total_languages = defaultdict(int)
	for repo in repos:
		languages_count = get_repo_languages(repo)
		for language in languages_count.keys():
			total_languages[language] += languages_count[language]
	return total_languages


def get_repos(username):
	github_url = "https://api.github.com/users/%s/repos" % username
	r = requests.get(github_url, auth=auth)
	return r.json()


def get_repo_languages(repo):
	languages_url = repo.get('languages_url')
	r = requests.get(languages_url, auth=auth)
	return r.json()


if __name__ == '__main__':
	import os, sys, select, argparse, fileinput
	parser = argparse.ArgumentParser(formatter_class=lambda prog: argparse.HelpFormatter(prog,max_help_position=30), description="A python CLI to find the a user's favourite github langauge.")
	parser.add_argument('username', nargs=1, help='github username')
	main(parser.parse_args(), parser.print_help)
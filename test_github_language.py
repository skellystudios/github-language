import github_language as ghl
import unittest
from httmock import urlmatch, HTTMock, all_requests
from testfixtures import LogCapture
from bunch import *

class TestTheThing(unittest.TestCase):

	def test_end_to_end(self):
		args = Bunch()
		args.username = ['username']
		with HTTMock(all_mock):
			out = ghl.main(args, None)
		self.assertEqual(out, "Ruby")

class TestMethods(unittest.TestCase):

	def test_pick_favourite(self):
		languages = dict({u'vbasic': 12, u'Ruby': 12345})
		output = ghl.pick_favourite_languages(languages)
		self.assertEqual(output,"Ruby") 

	def test_multiple_favourites(self):
		languages = dict({u'COBOL': 1968, u'FORTRAN': 1968})
		output = ghl.pick_favourite_languages(languages)
		self.assertTrue(output == "COBOL, FORTRAN" or output == "FORTRAN, COBOL") 

	def test_no_languages(self):
		with LogCapture() as l:
			languages = dict({})
			out = ghl.pick_favourite_languages(languages)
		l.check(('root', 'WARNING', 'No repositories with tagged languages'))
		self.assertEqual(out, "")


class TestWebCalls(unittest.TestCase):

	def test_get_repos(self):
		with HTTMock(github_repos_mock):
			repos = ghl.get_repos("username")
		
		self.assertEqual(repos[0].get("id"), 13651424)
		self.assertEqual(len(repos), 2)

	def test_get_languages(self):
		with HTTMock(github_languages_mock):
			test_repo = dict(languages_url="https://api.github.com/repos/username/repo1/languages")
			languages = ghl.get_repo_languages(test_repo)
		
		self.assertEqual(languages.get("Python"), 2279)
		self.assertEqual(len(languages.keys()), 3)


@urlmatch(netloc=r'(.*\.)?github\.com$')
def github_repos_mock(url, request):
		return repo_json

@urlmatch(netloc=r'(.*\.)?github\.com$', path=r'.*/languages$')
def github_languages_mock(url, request):
		return language_json

@all_requests
def all_mock(url, request):
		if "languages" in url.path: 
			return language_json
		else: 
			return repo_json

language_json = """
					{
	 					"Python": 2279,
	 					"Ruby": 2934,
	 					"Java": 1212
					}
					"""
repo_json = """
				[{ 
					"id": 13651424,
					"name": "repo1",
					"languages_url": "https://api.github.com/repos/username/repo1/languages"
				},
				{
					"id": 123456,
					"name": "repo2",
					"languages_url": "https://api.github.com/repos/username/repo2/languages"
				}]
				"""


if __name__ == '__main__':
	unittest.main()
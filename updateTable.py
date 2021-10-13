#!/usr/bin/env python

import os
import requests
import re
from pytablewriter import MarkdownTableWriter

# Script to update markdown table with links to all CTFLearn Challenges and write-ups, based on category


# Constants
excluded_paths = ['.git', 'resources', 'unsolved']
title_regex="<title>(.+?)</title>"
difficulty_regex='<span class="badge .*? bd-white">(.+?)</span>'
difficulty_score = dict(Easy=0, Medium=1, Hard=2)

# Given the challenge number and category, returns the contents of a markdown table row
def scrape_info(category, chal_no):

  url = "https://www.ctflearn.com/challenge/"+chal_no
  content =  requests.get(url).content
 
  # Extract challenge name from title format 
  # ' Challenge - challenge_name -  CTFlearn - CTF Practice - CTF Problems - CTF Challenges'
  title = re.findall(re.compile(title_regex), content)[0].split(' - ')[1]
  markdown_title = "[{}]({})".format(title, url)
  difficulty = re.findall(re.compile(difficulty_regex), content)[0]

  write_up_link = "[:link:]({}/{})".format(category, chal_no)
  
  return [chal_no, markdown_title,  write_up_link, difficulty]



if __name__=='__main__':

  # Copy README Intro
  open("README.md", "w").writelines(open("READMEintro.md").readlines())

  categories = dict.fromkeys(filter(lambda x: (os.path.isdir(x) and x not in excluded_paths), os.listdir('./')))

  for key in sorted(categories.keys()):
    print(key)
    categories[key] = []
    for chall in filter( lambda x: x != 'unsolved', os.listdir('./'+key)):
      categories[key].append(scrape_info(key, chall))
    writer = MarkdownTableWriter()
    
    # Generate Markdown Table
    # Sort based on difficulty, then challenge_no
    writer.headers=["No", "Title", "Solution", "Difficulty"]
    writer.value_matrix = sorted(categories[key], key = lambda x: (difficulty_score[x[3]], int(x[0])))
    table = writer.dumps()

    f=open("README.md", "a+")
    f.write("\n\n### {}\n\n".format(key.capitalize()))
    f.write("{}".format(table))


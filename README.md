*How to run project: "python3 app/cleaner/bnf_minute.py"


<!-- 
  *Use pip’s freeze command to generate a requirements.txt file for your project: If you save this in requirements.txt, then you can pip3 install -r requirements.txt. 
  *pip freeze saves all packages in the environment including those that you don’t use in your current project. (if you don’t have virtualenv)
  *pip freeze only saves the packages that are installed with pip install in your environment.
  *sometimes you just need to create requirements.txt for a new project without installing modules.
-->
1. pip3 freeze > requirements.txt
<!--  
*if you need custom then erase all data of requirement.txt file and go to step 2
*When if you’re going to share the project with the rest of the world you will need to install dependencies by running $pip install -r requirements.txt 
-->

2. pip3 install -r requirements.txt

3. "packages installed as follows"
  <!-- A tool that automatically formats Python code -->
  1. pip3 install autopep8 
 
  <!-- Beautiful Soup is a library that makes it easy to scrape information from web pages. It sits atop an HTML or XML parser, providing Pythonic idioms for iterating, searching, and modifying the parse tree. -->
  2. pip3 install beautifulsoup4

  3. pip3 install pandas

  <!-- Style Guide for Python Code -->
  4. pip3 install pep8

  <!-- 
  *Underscore.py is a python port of excellent javascript library underscore.js
  *From underscore page: Underscore.js is a utility-belt library for JavaScript that provides support for the usual functional suspects (each, map, reduce, filter...) without extending any core JavaScript objects. 
  -->
  5. pip3 install underscore.py

------

ORB NR Running Steps:

- `python3 -m app.backtest.orb_nr_optimise`

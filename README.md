totra
=====
*an unofficial TopTracker CLI helper*

Purpose
-------

[TopTracker](https://www.toptal.com/tracker) is great time tracking tool, but when
it comes to makes polls, reports etc. I find CLI tools much more productive then
clicking around web page.

The idea went from simple question: *how much hours I've worked i.e this week ?*

With TopTracker web page, to know such information I had to: login to web page, click on 
date range, export activities to csv, open spreadsheet software and import this csv,
 and then sum.
With this you can just:

`totra how_much_hours --workers="Andrzej Bargański" --from=Monday -l my@login.com -p mypassword`

...and in second you see result !  

Usage
-----
__*Notice:*__
*Application is still in planning area, commands, options etc. can change, and every* 
*TopTracker user is invited to post thoughts, wishes and participate in development*

```
   tottra activities [--format=<format>] [--projects=<projects>] [--workers=<workers>] --from=<from_date> [--to=<to_date>] [-l login] [-p password] [-o output_filename]
   tottra how_much_hours [--projects=<projects>] [--workers=<workers>] --from=<from_date> [--to=<to_date>] [-l login] [-p password]
   tottra -h | --help
   tottra --version
 
 Commands:
   activities                Output activities in --format.
   how_much_hours            Shows how much work hours are registered according to given parameters.
 
 Options:
   --format=<format>         Output format. Can be: json, excel. [default: json]
   --projects=<projects>     Projects names as coma separated list. Ex. 'Project 1' or 'Project 1,Project 2'
   --workers=<workers>       Workers as coma seprated list. Ex. 'Worker Name' or 'Worker Name 1, Worker Name 2'
   --from=<from_date>        Date as beginning of period for data retrieval. Format is: YYYY-mm-dd , ex: 2018-05-01
   --to=<to_date>            Date as end of period for data retrieval. Format is: YYYY-mm-dd , ex: 2018-05-01. [default: now].
   -o output_filename        Output filename to write data. Default is stdout (print on your screen) [default: stdout]
   -h --help                 Show this screen.
   --version                 Show version.
   -l login                  User login name.
   -p password               User password.
```

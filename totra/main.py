"""Unofficial TopTracker (https://www.toptal.com/tracker) helper

Usage:
  totra activities [--format=<format>] [--projects=<projects>] [--workers=<workers>] --from=<from_date> [--to=<to_date>] [-l login] [-p password] [-o output_filename]
  totra how_much_hours [--projects=<projects>] [--workers=<workers>] --from=<from_date> [--to=<to_date>] [-l login] [-p password]
  totra -h | --help
  totra --version

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
"""
from docopt import docopt
import totra

def __get_option_param(arguments, option_name, param_name=None):
    if not param_name:
        param_name = option_name
    return arguments['<{0}>'.format(param_name)].split(',') if arguments['{0}'.format(option_name)] else None


def __get_option_value_list(arguments, option_name):
    return arguments['{0}'.format(option_name)].split(',') if arguments['{0}'.format(option_name)] else None


def main():
    arguments = docopt(__doc__, version='TopTracker helper. Version: {0}'.format(totra.__version__))
    activities_command = arguments['activities']
    how_much_hours_command = arguments['how_much_hours']
    output_format = arguments['--format']
    projects = __get_option_value_list(arguments, '--projects')
    workers = __get_option_value_list(arguments, '--workers')
    from_date = arguments['--from']
    to_date = arguments['--to']
    login_name = arguments['-l']
    login_password = arguments['-p']
    output_filename = arguments['-o']

    if how_much_hours_command:
        data = totra.how_much_hours(login_name, login_password, workers=workers,
            projects=projects,  start_date=from_date, end_date=to_date)
        totra.save_output(data, output_filename)

    if activities_command:
        data = totra.report_activities(login_name, login_password, workers=workers,
                                             projects=projects,  start_date=from_date, end_date=to_date)
        data_in_requested_format = totra.format_activities(data, format=output_format)
        totra.save_output(data_in_requested_format, output_filename)


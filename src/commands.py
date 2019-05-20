import inspect, sys, click

from functions import get_commands

@click.command()
@click.option("--count", default=1, help="Number of greetings.")
@click.option("--name", prompt="Your name",
              help="The person to greet.")
def hello(count, name):
    '''
    Simple program that greets NAME for a total of COUNT times
    '''
    for _ in range(count):
        click.echo("Hello, %s!" % name)

@click.command()
def help():
    '''
    Help function will list available commands & display attached python documentation
    '''
    members = get_commands()
    for o in members:
        click.secho('- {}: {}'.format(o[0], o[1].__doc__ if o[1].__doc__ is not None else 'No documentation found'), fg='green')


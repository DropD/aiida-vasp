"""Run workchain submission tests."""
import os
import subprocess as sp

import click

OS_ENV = os.environ.copy()


def quicksetup():
    sp.call(
        [
            'sudo', 'verdi', 'quicksetup', '--non-interactive', '--email=a@b.c', '--first-name=A', '--last-name=B', '--institution=C',
            '--profile=quicksetup'
        ],
        env=OS_ENV)


@click.command()
def main():
    quicksetup()


if __name__ == '__main__':
    main()

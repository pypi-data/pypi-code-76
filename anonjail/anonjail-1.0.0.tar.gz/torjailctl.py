#!/usr/bin/env python3
# Torjailctl - Integrate Firejail sandboxing in the Linux desktop
# Copyright (C) 2015-2017 Rahiel Kasim (Shoutout to you mister Kasim :)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
import os
import os.path
import getpass
import re
from difflib import get_close_matches
from shutil import which
import click

firejail = which("firejail")
torjailctl = which("torjail")

TORJAIL_CMD = "Exec=gksudo torjail "
FIREJAIL_CMD = "Exec=firejail "

__version__ = "1.0.0"

if not firejail:
    click.secho("Firejail and Torjail must be installed!", fg="red")
    raise click.UsageError(message="Please install Firejail and Torjail")


profile_path = "/etc/firejail/"
application_path = "/usr/share/applications/"
symlink_path = "/usr/local/bin/"
config = "/etc/firejail/firejail.config"

profiles = [os.path.splitext(f)[0] for f in os.listdir(profile_path)]
applications = [os.path.splitext(f)[0] for f in os.listdir(application_path)]
installed = [p for p in profiles if p in applications]


@click.version_option()
@click.group()
def cli():
    pass

def get_config():
    """Get header and config."""
    header = "# list of enforced Firejail profiles\n"
    try:
        with open(config, "r") as f:
            conf = [l.strip() for l in f.readlines() if not l.startswith("#")]
    except FileNotFoundError:
        conf = []
    return header, conf


def write_config(programs, test, combine):
    """Write config to disk if necessary. Uses test to check if a program has to
    be added/removed from the config. Programs and conf are combined with
    combine.
    """
    header, conf = get_config()

    write = False
    for p in programs:
        if test(p, conf):
            write = True
            continue

    if write:
        lines = header + "\n".join(sorted(combine(programs, conf)))
        with open(config, "w") as f:
            f.writelines(lines)


def add_config(programs):
    """Add programs to config."""
    write_config(programs,
                 lambda program, conf: program not in conf,
                 lambda programs, conf: set(conf + programs))


def remove_config(programs):
    """Remove programs from config."""
    write_config(programs,
                 lambda program, conf: program in conf,
                 lambda programs, conf: set(conf) - set(programs))


def get_desktop(program):
    """Get path to program's desktop file."""
    path = os.path.join(application_path, program + ".desktop")
    if os.path.isfile(path):
        return path
    else:
        message = "Desktop file for %s does not exist." % program

        typo = get_close_matches(program, installed, n=1)
        if len(typo) > 0:
            message += "\n\nDid you mean %s?" % typo[0]

        raise click.ClickException(message)


def replace(filename, condition, transform):
    """Replace lines in filename for which condition is true with transform."""
    newfile = []
    with open(filename, "rb") as f:
        for line in f:
            if condition(line):
                newfile.append(transform(line))
            else:
                newfile.append(line)

    with open(filename, "wb") as f:
        f.writelines(newfile)


def get_programs(program, all_programs=False):
    """Return list of programs to enable / disable."""
    if all_programs:
        program = installed

    # Check if we have permission to modify global desktop files.
    if not os.access(get_desktop(installed[0]), os.W_OK):
        raise click.UsageError(
            message="Can't modify desktop files, please execute as root.")

    if len(program) == 0:
        raise click.ClickException("No program specified.")

    return list(program), [get_desktop(p) for p in program]


def symlink_enable(program):
    p = symlink_path + program
    if not os.path.exists(p):
        os.symlink(firejail, p)


def symlink_disable(program):
    p = symlink_path + program
    if os.path.exists(p):
        os.remove(p)


@cli.command(help="enable torjailctl for program")
@click.argument("program", type=click.STRING, nargs=-1)
@click.option("--all", "all_programs", is_flag=True, help="Enable Firejail for all supported programs.")
@click.option("--tor", "torify", is_flag=True, help="Enable Tor routing for the/all program(s)")
def enable(program, all_programs, torify=False, update_config=True):
    """Enable torjailctl for program. Program is a sequence of program names."""
    programs, desktop_files = get_programs(program, all_programs)  # root access after this line

    os.makedirs("/usr/local/bin", mode=0o775, exist_ok=True)
    for p in programs:
        symlink_enable(p)

    torified = TORJAIL_CMD.encode('UTF-8') if torify else FIREJAIL_CMD.encode('UTF-8')
    for d in desktop_files:
        replace(d,
                lambda l: l.startswith(b"Exec=") and (b"firejail" or "torjail"  not in l),
                lambda l: torified + l[l.find(b"=") + 1:])

    if update_config:
        add_config(programs)


@cli.command(help="disable torjailctl for program")
@click.argument("program", type=click.STRING, nargs=-1)
@click.option("--all", "all_programs", is_flag=True, help="Disable Firejail for all programs.")
def disable(program, all_programs):
    """Disable Firejail for program. Program is a sequence of program names."""
    programs, desktop_files = get_programs(program, all_programs)  # root access after this line

    for p in programs:
        symlink_disable(p)

    for d in desktop_files:
        replace(d,
                lambda line: line.startswith(b"Exec=firejail"),
                lambda line: b"Exec=" + line[14:])
        replace(d,
                lambda line: line.startswith(b"Exec=gksudo"),
                lambda line: b"Exec=" + line[19:])

    remove_config(programs)


@cli.command(help="show status of Firejail profiles")
def status():
    """Display status of available Firejail profiles."""
    symlinks = []
    try:
        for p in os.scandir(symlink_path):
            if p.is_symlink() and os.path.realpath(p.path) == firejail:
                symlinks.append(p.name)
    except FileNotFoundError:
        pass

    enabled = []
    disabled = []
    for p in installed:
        with open(get_desktop(p), "rb") as f:
            if (b"Exec=firejail" or b"Exec=torjail") in f.read():
                enabled.append(p)
            else:
                disabled.append(p)

    header, conf = get_config()
    update_disabled = [p for p in conf if (p not in enabled or p not in symlinks)]
    disabled = [p for p in disabled if p not in update_disabled]

    try:
        longest_name = max(conf, key=len)
    except ValueError:
        longest_name = None     # when the list is empty

    def pad(s, l):
        """Right-pad s so it's the same length as l."""
        return s + " " * (len(l) - len(s))

    is_enabled = lambda p, l: pad("yes", "symlink") if p in l else click.style(pad("no", "symlink"), fg="red")
    padding = "    "

    click.echo("{:<2} Firejail profiles are enabled".format(len(enabled)))
    if conf:
        click.secho("   " + pad("program", longest_name) + padding + "symlink" + padding + "desktop file", bold=True)
        for p in sorted(conf):
            click.echo("   " + pad(p, longest_name) + padding + is_enabled(p, symlinks) + padding + is_enabled(p, enabled))
    print()

    click.echo("{:<2} Firejail profiles are disabled and available".format(len(disabled)))
    for p in sorted(disabled):
        click.echo("   %s" % p)

    if len(update_disabled) > 0:
        click.secho("\n{:<2} Firejail profiles are disabled by updates".format(len(update_disabled)), fg="red")
        for p in sorted(update_disabled):
            click.echo("   %s" % p)
        click.echo("Please run: " + click.style("sudo torjailctl restore", bold=True))


@cli.command(help="restore Firejail profiles from config")
def restore():
    """Re-enable Firejail profiles for when desktop files get updated."""
    header, conf = get_config()

    # clean config from enabled programs removed from the system
    removed = [c for c in conf if c not in installed]
    remove_config(removed)
    [conf.remove(c) for c in removed]

    for p in removed:
        symlink_disable(p)

    if len(conf) > 0:
        enable.callback(conf, all_programs=False, update_config=False)


if __name__ == "__main__":
    cli()

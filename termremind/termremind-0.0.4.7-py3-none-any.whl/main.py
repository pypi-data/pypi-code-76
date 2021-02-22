# Base Py imports
import sys, random, os

# Imports from Pip
import colorama

# My own (using seeming self reference so that it can be found when installed w/ pip)
from termremind.data import dat
from termremind.conf import config


def getver():
    return "0.0.4.7"


VER = getver()

if sys.platform == "win32":
    s = "\\"  # damn microsoft lmao
else:
    s = "/"

CONF_PATH = os.path.expanduser("~") + s + ".config" + s + "remind"
REMINDERS_PATH = os.path.expanduser("~") + s + ".reminds" + s

RESET = "\x1b[0m"

colorama.init(autoreset=True)

mgr = dat(REMINDERS_PATH)
cnfmgr = config(CONF_PATH)

THEME_COLOR = cnfmgr.colorc()
LIST_COLORS = cnfmgr.dornd()

colors = [
    colorama.Fore.RED,
    colorama.Fore.GREEN,
    
    
    
    
    
    colorama.Fore.YELLOW,
    colorama.Fore.CYAN,
    colorama.Fore.MAGENTA,
]


def exitusage():
    help = (
        """
%REP%Remind%RES%: A simple cli tool for reminders.

%REP%Usage%RES%:
- remind      : Displays existing reminders
- remind help : Shows this page, and exits
- remind version : Prints version, and exits
- remind set <name> <detail> : Sets a reminder with specified details
- remind edit <name> <new_text> : Changes reminder text
- remind delete <name> : Removes a reminder with specified name
- remind reset : Removes all reminders (after confirmation)
- remind install : Automatically attempts to add itself to your shell startup file
                   (.bashrc or .zshrc depending on detected shell)
- remind config : Opens the config file in the program specified by $EDITOR

%REP%Formatting%RES%:
If you wrap text like "%bheeho%r", it will render the text "heeho" as bright text.

%REP%Notes%RES%:
- Remind's config is located at %CPTH%
- Reminders themselves are just plaintext files stored in %RPTH%
- "remind v" is an alias for "remind version"
- "remind s" is an alias for "remind set"
- "remind d" is an alias for "remind delete"

%REP%Version%RES%: """
        + VER
    )
    print(
        help.replace("%REP%", THEME_COLOR)
        .replace("%RES%", RESET)
        .replace("%CPTH%", CONF_PATH)
        .replace("%RPTH%", REMINDERS_PATH)
    )
    sys.exit(0)


def main():

    # Lol
    if sys.platform == "win32":
        print("Not technically supported on Windows yet.")
        win = True
        shell = "WIN"
    else:
        win = False
        shell = os.environ["SHELL"]

    if len(sys.argv) > 1:
        action = sys.argv[1]

        if action == "help":
            exitusage()
        elif action == "v" or action == "version":
            print(VER)
        elif action == "set" or action == "s":
            if len(sys.argv) > 3:
                mgr.setermreminder(sys.argv[2], sys.argv[3])
                print("Created your reminder.")
            else:
                print("Not enough info.")
                print("Usage: remind set <name> <text>")
        elif action == "delete" or action == "d":
            if len(sys.argv) > 2:
                mgr.delreminder(sys.argv[2])
                print("Reminder deleted.")
            else:
                print("Not enough info.")
                print("Usage: remind delete <name>")
        elif action == "reset":
            if input("Are you sure? (y/N) : ") == "y":
                for rname in mgr.listermreminders():
                    mgr.delreminder(rname)
                print("All reminders have been deleted.")
            else:
                print("No changes were made.")
        elif action == "install":
            if win:
                print("No can do on Windows.")
                exit(1)
            else:
                if "bash" in shell:
                    fn = ".bashrc"
                elif "zsh" in shell:
                    fn = ".zshrc"
                print(
                    "Your shell variable is `"
                    + shell
                    + "`. This means that your rc file is `~/"
                    + fn
                    + "`"
                )
                if input("Is this correct? (Y/n) : ") != "n":
                    with open(os.path.expanduser("~") + "/" + fn, "a") as f:
                        f.write("\n#Auto added by remind.\nremind")
                    print(
                        "Done. When you restart your shell, you should automatically see your reminders."
                    )
                else:
                    print("No changes made.")
        elif action == "config":
            if win:
                # Can't be assed to make a config value for windows editor preference
                # and best i can tell there's no such thing as %EDITOR% or similar
                os.system("notepad " + CONF_PATH)  # lmk if they remove notepad lmao
            else:
                os.system("$EDITOR " + CONF_PATH)
        elif action == "edit":
            if len(sys.argv) > 3:
                mgr.delreminder(sys.argv[2])
                mgr.setermreminder(sys.argv[2], sys.argv[3])
                print("Edited your reminder.")
            else:
                print("Not enough info.")
                print("Usage: remind edit <name> <new_text>")
        else:
            print("No such option: " + action)
            exitusage()
        sys.exit(0)

    else:  # no args passed
        print(THEME_COLOR + "Reminders:")
        if LIST_COLORS:
            rmds = mgr.listermreminders()
            if rmds != []:
                for rname in mgr.listermreminders():
                    print(
                        "- "
                        + random.choice(colors)
                        + rname
                        + RESET
                        + " : "
                        + mgr.getermreminder(rname)
                        .replace("%b", colorama.Style.BRIGHT)
                        .replace("%r", RESET)
                    )
            else:
                print(colors[0] + "No reminders found." + RESET)
        else:
            rmds = mgr.listermreminders()
            if rmds != []:
                for rname in mgr.listermreminders():
                    print("- " + rname + " : " + mgr.getermreminder(rname))
            else:
                print("No reminders found")
        sys.exit(0)


if __name__ == "__main__":
    main()

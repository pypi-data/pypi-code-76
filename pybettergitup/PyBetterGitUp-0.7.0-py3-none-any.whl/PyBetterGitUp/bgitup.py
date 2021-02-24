from PyGitUp.gitup import GitUp
import git
import os
import sys

__all__ = ['PyGetterGitUp']


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def warn(msg):
    print(f"{bcolors.WARNING}{msg}{bcolors.ENDC}")


def update(msg):
    print(f"{bcolors.OKGREEN}{msg}{bcolors.ENDC}")


class BGitUp():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    remoteDoesNotExist = "remote branch doesn't exist"
    missingRemoteBranches = []

    def parse_csv(self):
        reply = str(input(
            'Enter a comma seprated list of branch numbers that you want to keep: ')).lower().strip()
        values = [int(x.strip()) for x in reply.split(',')]
        for i in range(len(values)):
            self.missingRemoteBranches.pop(values[0] - 1)

        warn(
            f"\nUpdate list of branches to remove")
        for i in range(len(self.missingRemoteBranches)):
            warn(f"\t{i + 1}: {self.missingRemoteBranches[i].name}")

    def yes_or_no(self, question):
        reply = str(input(
            question+' (y/n) or (e) to edit the list: ')).lower().strip()
        if reply[0] == 'y':
            return True
        if reply[0] == 'n':
            return False
        if reply[0] == 'e':
            self.parse_csv()
            # make sure that is it wanted and that the list is not empty
            return ((len(self.missingRemoteBranches) > 0) and self.yes_or_no(question))
        else:
            return self.yes_or_no("Uhhhh... please enter ")

    def __init__(self):
        try:
            self.gitUp = GitUp()
        except:
            warn("Make sure you are in a git repository")
            sys.exit(1)

    def run(self):
        self.gitUp.run()

        # getting length of list of states
        states = self.gitUp.states

        # Look for any branches that are no longer connect to a remote origin
        # Iterating the index
        for i in range(len(states)):
            if states[i] == self.remoteDoesNotExist:
                branch = self.gitUp.branches[i]
                self.missingRemoteBranches.append(branch)

        missbranchesLength = len(self.missingRemoteBranches)
        if missbranchesLength > 0:
            branchPlural = "" if missbranchesLength == 1 else "es"
            thisPlural = "this" if missbranchesLength == 1 else "these"
            warn(
                f"\nBranch{branchPlural} found that no longer exist on the remote")
            for i in range(missbranchesLength):
                warn(f"\t{i + 1}: {self.missingRemoteBranches[i].name}")

            if (self.yes_or_no(f"Would you like to remove {thisPlural} branch{branchPlural}?") and (len(self.missingRemoteBranches) > 0)):
                # loop over each branch and delete it locally
                for i in range(len(self.missingRemoteBranches)):
                    update(f"\t deleting {self.missingRemoteBranches[i].name}")
                    git.Head.delete(
                        self.gitUp.repo, self.missingRemoteBranches[i].name, force=True)


def run():
    BGitUp().run()


if __name__ == "__main__":
    run()

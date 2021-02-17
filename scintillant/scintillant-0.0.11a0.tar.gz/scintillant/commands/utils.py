"""
General commands


"""


def print_help(search_for: str = None):
    print("Scintillant - a tool for quickly creating skills adapted to work "
          "with the 'Dialog' service - the central system of the "
          "Lilia chat bot.")

    print("** Commands **")
    print("--bottle - Download the latest skill template based on the "
          "Bottle framework\n"
          ">> snlt bottle\n"
          ">> snlt bottle my-first-skill")
    print("--testsuite - Create and start test suite for skills")
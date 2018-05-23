"""
    Given that this cookiecutter will run to scaffold a Python
    Lambda project and the user may not want to use the Makefile
    so we will remove it if that's the case.
"""

from __future__ import print_function

import os

TERMINATOR = "\x1b[0m"
INFO = "\x1b[1;33m [INFO]: "
SUCCESS = "\x1b[1;32m [SUCCESS]: "
HINT = "\x1b[3;33m"


def remove_optional_files():
    filenames = ["Makefile"]
    for file in filenames:
        if os.path.isfile(file):
            print(INFO + "Removing {} from project due to chosen options...".
                  format(file) + TERMINATOR)
            os.remove(file)

    return True


def main():

    project_name = '{{ cookiecutter.project_name }}'
    makefile_choice = '{{ cookiecutter.include_experimental_make }}'.lower()
    if makefile_choice == 'n':
        remove_optional_files()

    print(SUCCESS +
          "Project initialized successfully! You can now jump to {} folder".
          format(project_name) + TERMINATOR)
    print(INFO +
          "{}/README.md contains instructions on how to proceed.".
          format(project_name) + TERMINATOR)


if __name__ == '__main__':
    main()

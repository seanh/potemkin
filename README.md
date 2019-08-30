Potemkin
========

A pretend LMS for testing LTI apps.

## You will need

* [Make](https://www.gnu.org/software/make/)

* [Git](https://git-scm.com/)

* [pyenv](https://github.com/pyenv/pyenv)
  Follow the instructions in the pyenv README to install it.
  The Homebrew method works best on macOS.

### Clone the Git repo

    git clone https://github.com/hypothesis/potemkin.git

This will download the code into a `potemkin` directory in your current working
directory. You need to be in the `potemkin` directory from the remainder of the
installation process:

    cd potemkin

### Start the development server

    make dev

The first time you run `make dev` it might take a while to start because it'll
need to install the application dependencies and build the assets.

This will start the server on port 6543 (http://localhost:6543), reload the
application whenever changes are made to the source code, and restart it should
it crash for some reason.

**That's it!** You’ve finished setting up your Potemkin development
environment. Run `make help` to see all the commands that're available.

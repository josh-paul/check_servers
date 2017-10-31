Testing
=======

From the test directory run the test_servers.py script and leave running to serve as the test 
servers.

Then in another terminal, in the root directory of the repository, run tox. This will test the 
execution of the check_servers command against all versions of python supported as specified in 
the setup.py file.

Test environment setup:
Multiple versions of python are installed via pyenv (https://github.com/pyenv/pyenv).

Once all versions are installed, they need to be set to pyenv global command in order for tox 
to correctly detect them. Sample of the setup on my test system:
::

    $ pyenv global                                                                                                                   [15:25:53]
    2.7.13
    3.6.1
    3.5.3
    3.4.6
    3.3.6
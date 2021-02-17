import os, subprocess

class ShellCommandException(Exception):
    pass

def execute(cmd, throw_on_error=True, env=None, stream_output=False, cwd=None, cmd_stdin=None, **kwargs):
    """
    Runs a command as a child process.
    A convenience wrapper for running a command from a Python script.
    
    Arguments
    ---------
    cmd : list or string
      the command to run, as a list of strings
    throw_on_error : bool
     if true, raises an Exception if the exit code of the program is nonzero
    env : dict
      environment variables to be defined when execute the child process - {ENV_NAME: VALUE, ...}
    cwd :
      working directory for child process
    stream_output
      if true, does not capture standard output and error
      if false, captures these streams and returns them
    cmd_stdin : 
      if specified, passes the specified string as stdin to the child process.
    
    Note
    ----
    If stream_output is true, then only the exit code is returned. 
    If stream_output is false, then a tuple of the exit code, standard output and standard error is returned.
    """
    # update environment variables
    cmd_env = os.environ.copy()
    if env:
        cmd_env.update(env)

    # set stream output
    if stream_output:
        child = subprocess.Popen(cmd, env=cmd_env, cwd=cwd, universal_newlines=True, stdin=subprocess.PIPE, **kwargs)
        child.communicate(cmd_stdin)
        exit_code = child.wait()
        if throw_on_error and exit_code != 0:
            raise ShellCommandException("Non-zero exitcode: %s" % (exit_code))
        return exit_code
    else:
        child = subprocess.Popen(cmd, env=cmd_env, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd, universal_newlines=True, **kwargs)
        (stdout, stderr) = child.communicate(cmd_stdin)
        exit_code = child.wait()
        if throw_on_error and exit_code != 0:
            raise ShellCommandException("Non-zero exit code: %s\n\nSTDOUT:\n%s\n\nSTDERR:%s" % (exit_code, stdout, stderr))
        return exit_code, stdout, stderr

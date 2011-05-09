import sys, os, subprocess

def quote_first_command_arg( arg):
    """ 
    There's a bug in Windows when running an executable that's 
    located inside a path with a space in it.  This method handles 
    that case, or on non-Windows systems or an executable with no 
    spaces, it just leaves well enough alone. 
    """
    if (sys.platform!='win32'
        or ' ' not in arg):
        # Problem does not apply: 
        return arg
    try:
        import win32api
    except ImportError:
        raise ValueError(
            "The executable %r contains a space, and in order to "
            "handle this issue you must have the win32api module "
            "installed" % arg)
    arg = win32api.GetShortPathName(arg)
    return arg

def _turn_sigterm_into_systemexit():
    """
    Attempts to turn a SIGTERM exception into a SystemExit exception.
    """
    try:
        import signal
    except ImportError:
        return
    def handle_term(signo, frame):
        raise SystemExit
    signal.signal(signal.SIGTERM, handle_term)

def restart_with_monitor():
    while 1:
        args = [quote_first_command_arg(sys.executable)] + sys.argv
        new_environ = os.environ.copy()
        new_environ['_run'] = "1"
        proc = None
        try:
            try:
                _turn_sigterm_into_systemexit()
                proc = subprocess.Popen(args, env=new_environ)
                exit_code = proc.wait()
                proc = None
            except KeyboardInterrupt:
                print '^C caught in monitor process'
                return 1
        finally:
            if (proc is not None
                and hasattr(os, 'kill')):
                import signal
                try:
                    os.kill(proc.pid, signal.SIGTERM)
                except (OSError, IOError):
                    pass

        # Reloader always exits with code 3; but if we are
        # a monitor, any exit code will restart
        if exit_code != 3:
            return exit_code

def auto_reload(app):
    if os.environ.get("_run"):
        import reloader
        reloader.install()
        app()
    else:
        restart_with_monitor()


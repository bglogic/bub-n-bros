#! /usr/bin/env python

#
#  This script is used to start the server.
#  For command-line usage please run
#
#    python bubbob/bb.py --help
#

import sys, os

if __name__ == '__main__':
    LOCALDIR = sys.argv[0]
else:
    LOCALDIR = __file__
LOCALDIR = os.path.abspath(os.path.dirname(LOCALDIR))
sys.path.append(LOCALDIR)

def look_for_local_server(tries, verbose):
    # Look for a running local web server
    from common.hostchooser import find_servers
    servers = find_servers([('127.0.0.1', None)], tries=tries,
                           delay=0.5, verbose=verbose, port_needed=0)
    httpport = 'off'
    if servers:
        info, ping = servers.values()[0]
        infolst = info.split(':')
        if len(infolst) >= 3:
            httpport = infolst[2]
    try:
        httpport = int(httpport)
    except ValueError:
        return ''
    else:
        return 'http://127.0.0.1:%d/controlcenter.html' % httpport

def start_local_server():
    url = ''
    try:
        readpipe, writepipe = os.pipe()
    except:
        readpipe, writepipe = None
    if hasattr(os, 'fork') and hasattr(os, 'dup2'):
        if os.fork() == 0:
            # in the child process
            os.close(readpipe)
            sys.path.append(os.path.join(LOCALDIR, 'bubbob'))
            import bb, gamesrv, stdlog
            bb.BubBobGame.Quiet = 1
            logfile = stdlog.LogFile()
            bb.start_metaserver(writepipe, 0)
            if logfile:
                print >> logfile
                print "Logging to", logfile.filename
                fd = logfile.f.fileno()
                try:
                    # detach from parent
                    os.dup2(fd, 1)
                    os.dup2(fd, 2)
                    os.dup2(fd, 0)
                except OSError:
                    pass
                logfile.close()
            gamesrv.mainloop()
            sys.exit(0)
    else:
        MAINSCRIPT = os.path.abspath(os.path.join(LOCALDIR, 'bubbob', 'bb.py'))
        args = [sys.executable, MAINSCRIPT]
        if readpipe is not None:
            args.append('--pipeurlto=%d,%d' % (readpipe, writepipe))
        args.append('--quiet')
        os.spawnv(os.P_NOWAITO, args[0], args)
    if readpipe is not None:
        os.close(writepipe)
        while 1:
            try:
                t = os.read(readpipe, 128)
                if not t:
                    break
            except OSError:
                return ''
            url += t
        os.close(readpipe)
    return url


# main
url = look_for_local_server(tries=1, verbose=0)
if not url:
    url = start_local_server()
    if not url:
        # wait for up to 5 seconds for the server to start
        for i in range(10):
            url = look_for_local_server(tries=1, verbose=0)
            if url:
                break
        else:
            print >> sys.stderr, 'The local server is not starting, giving up.'
            sys.exit(1)

try:
    import webbrowser
    browser = webbrowser.get()
    name = getattr(browser, 'name', browser.__class__.__name__)
    print "Trying to open '%s' with '%s'..." % (url, name)
    browser.open(url)
except:
    exc, val, tb = sys.exc_info()
    print '-'*60
    print >> sys.stderr, "Failed to launch the web browser:"
    print >> sys.stderr, "  %s: %s" % (exc.__name__, val)
    print
    print "Sorry, I guess you have to go to the following URL manually:"
else:
    print "Done running '%s'." % name
    if not look_for_local_server(tries=1, verbose=0):
        # assume that browser.open() waited for the browser to finish
        # and that the server has been closed from the browser.
        raise SystemExit
    print
    print '-'*60
    print "If the browser fails to open the page automatically,"
    print "you will have to manually go to the following URL:"
print ' ', url
print '-'*60
print "Note that the server runs in the background. You have to use"
print "the 'Stop this program' link to cleanly stop it."
print "Normally, however, running this script multiple times should"
print "not create multiple servers in the background."

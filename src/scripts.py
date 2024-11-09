from subprocess import Popen, run


def dev():
    # Popen starts process in the background
    tw_watch_process = Popen(["pnpm", "tw_watch"])
    run(["poetry", "run", "python", "manage.py", "runserver"])
    tw_watch_process.terminate()

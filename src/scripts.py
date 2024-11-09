from pathlib import Path
from subprocess import Popen, run


def dev():
    file_path = Path(__file__)
    project_dir = file_path.parent.parent

    # Popen starts process in the background
    tw_watch_process = Popen(["pnpm", "tw_watch"])
    run(["poetry", "run", "python", f"{project_dir}/src/manage.py", "runserver"])
    tw_watch_process.terminate()

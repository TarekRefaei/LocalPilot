# backend/tests/e2e/test_act_mode_safety.py
import subprocess

import pytest


def run(cmd, cwd):
    r = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"cmd failed: {cmd}\nstdout:{r.stdout}\nstderr:{r.stderr}")
    return r.stdout.strip()


@pytest.mark.e2e
def test_act_mode_branch_and_rollback(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    run("git init -b main", repo)
    # Ensure commits work in CI by configuring user identity locally
    run("git config user.email 'localpilot@example.com'", repo)
    run("git config user.name 'LocalPilot'", repo)
    (repo / "hello.txt").write_text("hello\n")
    run("git add hello.txt", repo)
    run('git commit -m "init"', repo)

    # Simulate Act: create new branch, commit a change, then simulate failure and rollback
    branch = "localpilot/plan-test"
    run(f"git checkout -b {branch}", repo)
    (repo / "newfile.txt").write_text("some content")
    run("git add newfile.txt", repo)
    run('git commit -m "add newfile"', repo)

    # Simulate failure -> rollback to previous commit
    run("git reset --hard HEAD~1", repo)
    # Delete branch and return to main
    run("git checkout main", repo)
    run(f"git branch -D {branch}", repo)

    # newfile should not exist (rolled back)
    assert not (repo / "newfile.txt").exists()

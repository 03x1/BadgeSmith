# badgesmith - GitHub Badge Automation Toolkit
# Copyright (C) 2026 03x1 (https://github.com/03x1)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import subprocess
import time
import random
import string
import sys
import os

# ============================================================
#  CONFIGURATION — fill these in before running
# ============================================================

GITHUB_USERNAME = "YOUR_USERNAME"       # e.g. "octocat"
GITHUB_TOKEN    = "YOUR_GITHUB_TOKEN"   # e.g. "ghp_abc123..."
REPO_NAME       = "YOUR_REPO_NAME"      # must exist on your account
REPO_PATH       = r"YOUR_REPO_PATH"     # local path to your cloned repo, e.g. r"C:\Users\you\myrepo"
BASE_BRANCH     = "main"
PR_COUNT        = 100                   # number of PRs to create and merge
DELAY_SECONDS   = 15                    # seconds to wait between PRs (don't go below 10)

# ============================================================
#  Badge tiers (PRs merged)
#  🥉 Bronze →    2
#  🥈 Silver →   16
#  🥇 Gold   →  128
#  💎 Plat   → 1024
# ============================================================

# ============================================================
#  DO NOT EDIT BELOW THIS LINE
# ============================================================

def run(cmd, cwd=None):
    result = subprocess.run(
        cmd, cwd=cwd, shell=True,
        capture_output=True, text=True
    )
    return result

def random_suffix():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))

def set_git_credentials():
    remote_url = f"https://{GITHUB_USERNAME}:{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{REPO_NAME}.git"
    run(f'git remote set-url origin {remote_url}', cwd=REPO_PATH)

def sync_base():
    run(f'git checkout {BASE_BRANCH}', cwd=REPO_PATH)
    run(f'git pull origin {BASE_BRANCH}', cwd=REPO_PATH)

def create_branch(branch_name):
    run(f'git checkout {BASE_BRANCH}', cwd=REPO_PATH)
    run(f'git checkout -b {branch_name}', cwd=REPO_PATH)

def make_change(pr_number):
    readme_path = os.path.join(REPO_PATH, "README.md")
    with open(readme_path, "a", encoding="utf-8") as f:
        f.write(f"\n<!-- automated update #{pr_number} - {random_suffix()} -->")

def commit_and_push(branch_name, pr_number):
    run('git add README.md', cwd=REPO_PATH)
    run(f'git commit -m "automated update #{pr_number}"', cwd=REPO_PATH)
    result = run(f'git push origin {branch_name}', cwd=REPO_PATH)
    if result.returncode != 0:
        print(f"  ❌ Push failed: {result.stderr.strip()}")
        return False
    return True

def create_pr(branch_name, pr_number):
    result = run(
        f'gh pr create --title "Automated PR #{pr_number}" '
        f'--body "Automated pull request #{pr_number}" '
        f'--base {BASE_BRANCH} --head {branch_name}',
        cwd=REPO_PATH
    )
    if result.returncode != 0:
        print(f"  ❌ PR creation failed: {result.stderr.strip()}")
        return False
    print(f"  ✅ PR created")
    return True

def merge_pr(branch_name):
    result = run(
        f'gh pr merge {branch_name} --merge --delete-branch',
        cwd=REPO_PATH
    )
    if result.returncode != 0:
        print(f"  ❌ Merge failed: {result.stderr.strip()}")
        return False
    print(f"  ✅ PR merged")
    return True

def cleanup_local_branch(branch_name):
    run(f'git checkout {BASE_BRANCH}', cwd=REPO_PATH)
    run(f'git branch -D {branch_name}', cwd=REPO_PATH)

def main():
    print("=" * 50)
    print("  🦈 Pull Shark — badgesmith")
    print("=" * 50)
    print(f"  Repo  : {GITHUB_USERNAME}/{REPO_NAME}")
    print(f"  PRs   : {PR_COUNT}")
    print(f"  Delay : {DELAY_SECONDS}s between PRs")
    print("=" * 50)

    if "YOUR_" in GITHUB_USERNAME or "YOUR_" in GITHUB_TOKEN:
        print("\n❌ Please fill in GITHUB_USERNAME and GITHUB_TOKEN in the script first.")
        sys.exit(1)

    if not os.path.exists(REPO_PATH):
        print(f"\n❌ Repo path not found: {REPO_PATH}")
        sys.exit(1)

    print("\n🔧 Setting up credentials...")
    set_git_credentials()

    success = 0
    failed  = 0

    for i in range(1, PR_COUNT + 1):
        print(f"\n🔹 PR {i}/{PR_COUNT}")
        branch_name = f"auto-pr-{i}-{random_suffix()}"

        try:
            sync_base()
            create_branch(branch_name)
            make_change(i)

            if not commit_and_push(branch_name, i):
                failed += 1
                cleanup_local_branch(branch_name)
                continue

            time.sleep(3)

            if not create_pr(branch_name, i):
                failed += 1
                cleanup_local_branch(branch_name)
                continue

            time.sleep(3)

            if not merge_pr(branch_name):
                failed += 1
                cleanup_local_branch(branch_name)
                continue

            cleanup_local_branch(branch_name)
            success += 1

        except Exception as e:
            print(f"  ❌ Unexpected error: {e}")
            failed += 1
            try:
                cleanup_local_branch(branch_name)
            except:
                pass

        if i < PR_COUNT:
            print(f"  ⏳ Waiting {DELAY_SECONDS}s...")
            time.sleep(DELAY_SECONDS)

    print("\n" + "=" * 50)
    print(f"  🎉 Done!")
    print(f"  ✅ Successful : {success}")
    print(f"  ❌ Failed     : {failed}")
    print("=" * 50)
    print(f"\n  Check your badge at: https://github.com/{GITHUB_USERNAME}")
    print("=" * 50)

if __name__ == "__main__":
    main()

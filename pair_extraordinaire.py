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
import os
import sys

# ============================================================
#  CONFIGURATION — fill these in before running
# ============================================================

MAIN_USERNAME   = "YOUR_MAIN_USERNAME"      # your main GitHub username
MAIN_TOKEN      = "YOUR_MAIN_TOKEN"         # main account token (ghp_...)

SECOND_USERNAME = "YOUR_SECOND_USERNAME"    # second GitHub account username
SECOND_EMAIL    = "YOUR_SECOND_EMAIL"       # email associated with second account
SECOND_TOKEN    = "YOUR_SECOND_TOKEN"       # second account token (ghp_...)

REPO_NAME       = "YOUR_REPO_NAME"          # repo on your MAIN account
REPO_PATH       = r"YOUR_REPO_PATH"         # local path to your cloned repo
BASE_BRANCH     = "main"
PR_COUNT        = 50                        # 48 needed for Gold, 50 for buffer
DELAY_SECONDS   = 12                        # seconds to wait between PRs

# ============================================================
#  Badge tiers (co-authored PRs merged)
#  🥉 Bronze →  1
#  🥈 Silver → 10
#  🥇 Gold   → 24
#  💎 Plat   → 48
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
    remote_url = f"https://{MAIN_USERNAME}:{MAIN_TOKEN}@github.com/{MAIN_USERNAME}/{REPO_NAME}.git"
    run(f'git remote set-url origin {remote_url}', cwd=REPO_PATH)
    run(f'git config user.name "{MAIN_USERNAME}"', cwd=REPO_PATH)
    run(f'git config user.email "{MAIN_USERNAME}@users.noreply.github.com"', cwd=REPO_PATH)

def sync_base():
    run(f'git checkout {BASE_BRANCH}', cwd=REPO_PATH)
    run(f'git pull origin {BASE_BRANCH}', cwd=REPO_PATH)

def create_branch(branch_name):
    run(f'git checkout {BASE_BRANCH}', cwd=REPO_PATH)
    run(f'git checkout -b {branch_name}', cwd=REPO_PATH)

def make_change(pr_number):
    readme_path = os.path.join(REPO_PATH, "README.md")
    with open(readme_path, "a", encoding="utf-8") as f:
        f.write(f"\n<!-- pair update #{pr_number} - {random_suffix()} -->")

def write_commit_message(pr_number):
    """Write commit message to a temp file to handle Windows multiline correctly."""
    msg_path = os.path.join(REPO_PATH, ".git", "COMMIT_MSG_TEMP")
    # The blank line between title and trailer is REQUIRED by GitHub
    message = (
        f"pair update #{pr_number}\n"
        f"\n"
        f"Co-authored-by: {SECOND_USERNAME} <{SECOND_EMAIL}>\n"
    )
    with open(msg_path, "w", encoding="utf-8") as f:
        f.write(message)
    return msg_path

def commit_and_push(branch_name, pr_number):
    run('git add README.md', cwd=REPO_PATH)

    msg_path = write_commit_message(pr_number)
    result = run(f'git commit -F "{msg_path}"', cwd=REPO_PATH)

    if result.returncode != 0:
        print(f"  ❌ Commit failed: {result.stderr.strip()}")
        return False

    # Verify co-author trailer is present before pushing
    verify = run('git log -1 --pretty=%B', cwd=REPO_PATH)
    if "Co-authored-by" not in verify.stdout:
        print(f"  ⚠️  Warning: Co-authored-by not found in commit — aborting push")
        return False
    else:
        print(f"  ✅ Co-authored-by confirmed in commit")

    result = run(f'git push origin {branch_name}', cwd=REPO_PATH)
    if result.returncode != 0:
        print(f"  ❌ Push failed: {result.stderr.strip()}")
        return False

    return True

def create_pr(branch_name, pr_number):
    result = run(
        f'gh pr create --title "Pair PR #{pr_number}" '
        f'--body "Co-authored pull request #{pr_number}" '
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
    print("=" * 55)
    print("  🤝 Pair Extraordinaire — badgesmith")
    print("=" * 55)
    print(f"  Main account : {MAIN_USERNAME}")
    print(f"  Co-author    : {SECOND_USERNAME} <{SECOND_EMAIL}>")
    print(f"  Repo         : {MAIN_USERNAME}/{REPO_NAME}")
    print(f"  PRs          : {PR_COUNT}")
    print(f"  Delay        : {DELAY_SECONDS}s between PRs")
    print("=" * 55)

    if "YOUR_" in MAIN_TOKEN or "YOUR_" in SECOND_TOKEN:
        print("\n❌ Please fill in your tokens in the script first.")
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
        branch_name = f"pair-pr-{i}-{random_suffix()}"

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

    print("\n" + "=" * 55)
    print(f"  🎉 Done!")
    print(f"  ✅ Successful : {success}")
    print(f"  ❌ Failed     : {failed}")
    print("=" * 55)
    print(f"\n  Check your badge at: https://github.com/{MAIN_USERNAME}")
    print("=" * 55)

if __name__ == "__main__":
    main()

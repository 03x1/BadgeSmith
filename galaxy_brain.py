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

import requests
import time
import random
import sys

# ============================================================
#  CONFIGURATION — fill these in before running
# ============================================================

MAIN_USERNAME   = "YOUR_MAIN_USERNAME"      # your main GitHub username
MAIN_TOKEN      = "YOUR_MAIN_TOKEN"         # main account token (ghp_...)

SECOND_USERNAME = "YOUR_SECOND_USERNAME"    # second GitHub account username
SECOND_TOKEN    = "YOUR_SECOND_TOKEN"       # second account token (ghp_...)

REPO_NAME       = "YOUR_REPO_NAME"          # repo on your MAIN account (Discussions must be enabled)
DELAY_SECONDS   = 20                        # seconds between actions (increase to 25+ if rate limited)
TOTAL_ROUNDS    = 32                        # Q&A pairs to run (32 needed for Gold)

# ============================================================
#  Badge tiers (accepted discussion answers)
#  🥉 Bronze →  8
#  🥈 Silver → 16
#  🥇 Gold   → 32
# ============================================================

# ============================================================
#  Q&A BANK — questions posted by 2nd account, answered by main
# ============================================================

QA_PAIRS = [
    ("What is a variable in programming?", "A variable is a named storage location in memory that holds a value. It can be assigned, updated, and referenced throughout a program. For example in Python: `x = 5` creates a variable called x with the value 5."),
    ("What is the difference between a list and a tuple in Python?", "A list is mutable (can be changed after creation) and uses square brackets: `[1, 2, 3]`. A tuple is immutable (cannot be changed) and uses parentheses: `(1, 2, 3)`. Use tuples when data shouldn't change, lists when it should."),
    ("What is a function in programming?", "A function is a reusable block of code that performs a specific task. It can accept inputs (parameters) and return outputs. Functions help organize code and avoid repetition. In Python: `def greet(name): return f'Hello {name}'`"),
    ("What is Git and why is it used?", "Git is a version control system that tracks changes to files over time. It lets you save snapshots of your project, revert to previous states, and collaborate with others without overwriting each other's work."),
    ("What is the difference between == and === in JavaScript?", "`==` checks for equality with type coercion (e.g. `1 == '1'` is true). `===` checks for strict equality with no type coercion (e.g. `1 === '1'` is false). It's best practice to always use `===` to avoid unexpected behavior."),
    ("What is a loop in programming?", "A loop is a control structure that repeats a block of code multiple times. Common types are `for` loops (repeat a set number of times) and `while` loops (repeat until a condition is false). They're used to automate repetitive tasks."),
    ("What is an API?", "An API (Application Programming Interface) is a set of rules that allows different software applications to communicate with each other. For example, a weather app uses a weather API to fetch current temperature data from a remote server."),
    ("What is the difference between frontend and backend development?", "Frontend development deals with what users see and interact with in their browser (HTML, CSS, JavaScript). Backend development handles server-side logic, databases, and APIs that power the frontend. Full-stack developers work on both."),
    ("What is a class in object-oriented programming?", "A class is a blueprint for creating objects. It defines properties (attributes) and behaviors (methods) that objects of that class will have. For example, a `Car` class might have attributes like `color` and `speed`, and methods like `drive()`."),
    ("What is recursion?", "Recursion is when a function calls itself to solve a smaller version of the same problem. It needs a base case to stop. For example, calculating factorial: `def factorial(n): return 1 if n == 0 else n * factorial(n-1)`"),
    ("What is a database?", "A database is an organized collection of structured data stored electronically. It allows data to be easily accessed, managed, and updated. Common types are relational databases (like MySQL) which use tables, and NoSQL databases (like MongoDB) which use documents."),
    ("What is HTML?", "HTML (HyperText Markup Language) is the standard language for creating web pages. It uses tags to structure content — for example `<h1>` for headings, `<p>` for paragraphs, and `<a>` for links. It defines the structure but not the visual style of a page."),
    ("What is CSS used for?", "CSS (Cascading Style Sheets) is used to control the visual appearance of HTML elements — things like colors, fonts, spacing, and layout. It separates the design from the content, making it easier to maintain and update the look of a website."),
    ("What is a pull request?", "A pull request (PR) is a way to propose changes to a codebase on GitHub. You make changes on a separate branch, then open a PR to ask the repo owner to review and merge your changes into the main branch. It's a core part of collaborative development."),
    ("What is the difference between HTTP and HTTPS?", "HTTP (HyperText Transfer Protocol) transfers data between browser and server in plain text. HTTPS is the secure version — it encrypts data using SSL/TLS, protecting it from being intercepted. Always use HTTPS for sensitive information."),
    ("What is a boolean?", "A boolean is a data type that can only have two values: `True` or `False`. Booleans are used in conditions and logic — for example `if is_logged_in == True: show_dashboard()`. They're named after mathematician George Boole."),
    ("What is an array?", "An array is a data structure that stores multiple values in a single variable, accessed by index. For example in JavaScript: `let fruits = ['apple', 'banana', 'cherry']` — `fruits[0]` is 'apple'. Arrays are great for storing ordered collections of items."),
    ("What is JSON?", "JSON (JavaScript Object Notation) is a lightweight data format used to store and exchange data. It's human-readable and looks like: `{\"name\": \"Alex\", \"age\": 25}`. It's widely used for sending data between a server and a web application."),
    ("What is a compiler?", "A compiler translates source code written in a high-level language (like C++) into machine code that a computer can execute directly. This translation happens before the program runs. Languages like Python use an interpreter instead, which translates code line by line at runtime."),
    ("What is version control?", "Version control is a system that tracks changes to files over time, allowing you to recall specific versions later. It's essential for collaboration and backup. Git is the most popular version control system, and GitHub is the most popular platform for hosting Git repositories."),
    ("What is a framework in web development?", "A framework is a pre-built collection of code, tools, and conventions that provides a structure for building applications. For example, React is a frontend framework and Django is a backend framework. They speed up development by handling common tasks automatically."),
    ("What is the difference between null and undefined in JavaScript?", "`undefined` means a variable has been declared but not assigned a value. `null` is an explicit assignment meaning 'no value'. For example: `let x;` gives `undefined`, while `let y = null;` explicitly sets it to null."),
    ("What is a package manager?", "A package manager is a tool that automates installing, updating, and managing software libraries. npm is used for JavaScript, pip for Python, and apt for Linux. They save time by handling dependencies automatically instead of manually downloading files."),
    ("What is an IDE?", "An IDE (Integrated Development Environment) is a software application that provides tools for writing, testing, and debugging code all in one place. Popular IDEs include VS Code, PyCharm, and IntelliJ. They include features like syntax highlighting, autocomplete, and debuggers."),
    ("What is the difference between a stack and a queue?", "A stack follows LIFO (Last In First Out) — like a stack of plates, you add and remove from the top. A queue follows FIFO (First In First Out) — like a line of people, the first one in is the first one out. Both are fundamental data structures."),
    ("What is a REST API?", "A REST API is a web service that follows REST (Representational State Transfer) principles. It uses HTTP methods like GET (read), POST (create), PUT (update), and DELETE to perform operations on resources identified by URLs. Most modern web apps use REST APIs to communicate."),
    ("What is debugging?", "Debugging is the process of finding and fixing errors (bugs) in code. It involves reading error messages, adding print statements, and using debugger tools to step through code line by line. Good debugging skills are essential for every programmer."),
    ("What is inheritance in OOP?", "Inheritance is when a class (child) inherits properties and methods from another class (parent). It promotes code reuse. For example, a `Dog` class can inherit from an `Animal` class, getting its `eat()` and `sleep()` methods automatically while adding its own `bark()` method."),
    ("What is a binary search?", "Binary search is an efficient algorithm for finding an item in a sorted list. It works by repeatedly dividing the search range in half — checking the middle element and eliminating half the remaining items each time. It's much faster than linear search for large datasets."),
    ("What is cloud computing?", "Cloud computing means using remote servers hosted on the internet to store, manage, and process data instead of a local computer. Services like AWS, Google Cloud, and Azure let you rent computing power and storage on demand, scaling up or down as needed."),
    ("What is a merge conflict in Git?", "A merge conflict happens when two branches modify the same part of a file differently, and Git can't automatically decide which change to keep. You have to manually edit the file to resolve the conflict, choose which changes to keep, then commit the resolution."),
    ("What is Docker?", "Docker is a platform that packages applications and their dependencies into containers — lightweight, portable units that run consistently across any environment. It solves the 'works on my machine' problem by ensuring the app behaves the same in development and production."),
    ("What is a hash function?", "A hash function takes input data and returns a fixed-size string of characters (a hash). The same input always produces the same hash, but you can't reverse it to get the original data. Hash functions are used for password storage, data integrity checks, and hash tables."),
    ("What is an environment variable?", "An environment variable is a dynamic value stored in the operating system that programs can access at runtime. They're used to store configuration like API keys, database URLs, and secret tokens — keeping sensitive data out of source code."),
    ("What is a CDN?", "A CDN (Content Delivery Network) is a network of servers distributed around the world that deliver web content to users from the closest server. This reduces load times significantly. CDNs are commonly used to serve images, videos, and static files faster."),
]

# ============================================================
#  GITHUB GRAPHQL API HELPERS
# ============================================================

GITHUB_API = "https://api.github.com/graphql"

def graphql(token, query, variables=None):
    headers = {
        "Authorization": f"bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {"query": query, "variables": variables or {}}
    r = requests.post(GITHUB_API, json=payload, headers=headers)
    return r.json()

def get_repo_id(token):
    query = """
    query($owner: String!, $name: String!) {
      repository(owner: $owner, name: $name) {
        id
        discussionCategories(first: 10) {
          nodes { id name }
        }
      }
    }
    """
    result = graphql(token, query, {"owner": MAIN_USERNAME, "name": REPO_NAME})
    repo = result["data"]["repository"]
    repo_id = repo["id"]
    categories = repo["discussionCategories"]["nodes"]

    cat_id = None
    for c in categories:
        if "q&a" in c["name"].lower() or "question" in c["name"].lower():
            cat_id = c["id"]
            break
    if not cat_id:
        cat_id = categories[0]["id"]
        print(f"  ⚠️  No Q&A category found — using '{categories[0]['name']}'. Badge may not count!")

    return repo_id, cat_id

def post_discussion(token, repo_id, cat_id, title, body):
    query = """
    mutation($repoId: ID!, $catId: ID!, $title: String!, $body: String!) {
      createDiscussion(input: {
        repositoryId: $repoId,
        categoryId: $catId,
        title: $title,
        body: $body
      }) {
        discussion { id url }
      }
    }
    """
    result = graphql(token, query, {
        "repoId": repo_id,
        "catId": cat_id,
        "title": title,
        "body": body
    })
    disc = result["data"]["createDiscussion"]["discussion"]
    return disc["id"], disc["url"]

def post_comment(token, discussion_id, body):
    query = """
    mutation($discussionId: ID!, $body: String!) {
      addDiscussionComment(input: {
        discussionId: $discussionId,
        body: $body
      }) {
        comment { id }
      }
    }
    """
    result = graphql(token, query, {
        "discussionId": discussion_id,
        "body": body
    })
    return result["data"]["addDiscussionComment"]["comment"]["id"]

def mark_answer(token, comment_id):
    query = """
    mutation($commentId: ID!) {
      markDiscussionCommentAsAnswer(input: { id: $commentId }) {
        discussion { id }
      }
    }
    """
    result = graphql(token, query, {"commentId": comment_id})
    return "errors" not in result

# ============================================================
#  MAIN BOT
# ============================================================

def main():
    print("=" * 55)
    print("  🧠 Galaxy Brain — badgesmith")
    print("=" * 55)
    print(f"  Main account   : {MAIN_USERNAME}")
    print(f"  Second account : {SECOND_USERNAME}")
    print(f"  Repo           : {MAIN_USERNAME}/{REPO_NAME}")
    print(f"  Rounds         : {TOTAL_ROUNDS}")
    print(f"  Delay          : {DELAY_SECONDS}s between actions")
    print("=" * 55)

    if "YOUR_" in MAIN_TOKEN or "YOUR_" in SECOND_TOKEN:
        print("\n❌ Please fill in your tokens in the script first.")
        sys.exit(1)

    print("\n🔧 Fetching repo info...")
    try:
        repo_id, cat_id = get_repo_id(MAIN_TOKEN)
        print(f"  ✅ Repo found, category ready")
    except Exception as e:
        print(f"  ❌ Failed to get repo info: {e}")
        print("  Make sure Discussions is enabled and a Q&A category exists on your repo.")
        sys.exit(1)

    success = 0
    failed  = 0
    pairs   = QA_PAIRS.copy()
    random.shuffle(pairs)

    for i in range(1, TOTAL_ROUNDS + 1):
        qa = pairs[(i - 1) % len(pairs)]
        question, answer = qa

        print(f"\n🔹 Round {i}/{TOTAL_ROUNDS}")
        print(f"  Q: {question[:60]}...")

        try:
            disc_id, disc_url = post_discussion(
                SECOND_TOKEN, repo_id, cat_id,
                question, f"I have a question: {question}"
            )
            print(f"  ✅ Question posted")
            time.sleep(DELAY_SECONDS)

            comment_id = post_comment(MAIN_TOKEN, disc_id, answer)
            print(f"  ✅ Answer posted")
            time.sleep(DELAY_SECONDS)

            marked = mark_answer(SECOND_TOKEN, comment_id)
            if marked:
                print(f"  ✅ Answer marked as accepted")
                success += 1
            else:
                print(f"  ⚠️  Could not mark as accepted — ensure repo has a Q&A category")
                failed += 1

        except Exception as e:
            print(f"  ❌ Error: {e}")
            failed += 1

        if i < TOTAL_ROUNDS:
            print(f"  ⏳ Waiting {DELAY_SECONDS}s...")
            time.sleep(DELAY_SECONDS)

    print("\n" + "=" * 55)
    print(f"  🎉 Done!")
    print(f"  ✅ Accepted answers : {success}")
    print(f"  ❌ Failed           : {failed}")
    print("=" * 55)
    print(f"\n  Check your badge at: https://github.com/{MAIN_USERNAME}")
    print("=" * 55)

if __name__ == "__main__":
    main()

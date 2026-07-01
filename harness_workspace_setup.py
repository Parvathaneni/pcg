#!/usr/bin/env python3
"""
Harness Workspace Setup (from a Workspace Template)
===================================================

What this script does, in plain English:
  1. Reads two values from environment variables that Harness provides
     (the API key from the secret manager, and the account ID).
  2. Takes 5 details from the Harness pipeline (repo, branch, folder, app id, BU).
  3. Calls the Harness API to create a workspace FROM A WORKSPACE TEMPLATE.
     The template already defines the provisioner, connector, and base settings.
  4. Prints whether it worked.

How to run it:
  python harness_workspace_setup.py <repo> <branch> <folder> <app_id> <bu>

Example:
  python harness_workspace_setup.py my-org/infra main envs/prod APP-1234 Finance

Where the secrets come from (set these in your pipeline step before running):
  export HARNESS_API_KEY=<+secrets.getValue("harness_api_key")>
  export HARNESS_ACCOUNT_ID=<+account.identifier>
"""

import sys              # lets us read the values typed after the script name
import os               # lets us read environment variables
import requests         # lets us call the Harness API over the internet


# ============================================================
# STEP 1: Settings you can edit
# ============================================================

# These two come from environment variables that Harness sets for us.
# (The API key comes from the Harness secret manager — never hard-code it.)
API_KEY    = os.getenv("HARNESS_API_KEY")
ACCOUNT_ID = os.getenv("HARNESS_ACCOUNT_ID")

# These describe WHERE the workspace lives. Edit them for your project.
ORG_ID     = "your_org_id"          # e.g. "default"
PROJECT_ID = "your_project_id"      # e.g. "my_project"

# The WORKSPACE TEMPLATE to build from. The template already contains the
# provisioner type/version, connector, and the standard variables.
TEMPLATE_ID      = "your_template_id"   # the identifier of your workspace template
TEMPLATE_VERSION = "v1"                 # the template version label

# These describe the new workspace we are creating.
WORKSPACE_NAME = "apps-team-workspace"
WORKSPACE_ID   = "apps_team_workspace"   # no spaces allowed; use underscores


# ============================================================
# STEP 2: Read the 5 values sent by the Harness pipeline
# ============================================================
# When the pipeline runs the script, it types 5 values after the script name.
# sys.argv is a list of those typed words. sys.argv[0] is the script name,
# so the 5 values we want are sys.argv[1] through sys.argv[5].

if len(sys.argv) != 6:
    print("ERROR: Expected 5 values: <repo> <branch> <folder> <app_id> <bu>")
    sys.exit(1)   # stop the script with an error

repo   = sys.argv[1]
branch = sys.argv[2]
folder = sys.argv[3]
app_id = sys.argv[4]
bu     = sys.argv[5]


# ============================================================
# STEP 3: Make sure the secrets and settings are filled in
# ============================================================

if not API_KEY or not ACCOUNT_ID:
    print("ERROR: HARNESS_API_KEY or HARNESS_ACCOUNT_ID environment variable is not set.")
    print("       Make sure the pipeline exports them before running this script.")
    sys.exit(1)

if ORG_ID == "your_org_id" or PROJECT_ID == "your_project_id":
    print("ERROR: Please set ORG_ID and PROJECT_ID in STEP 1 of this script.")
    sys.exit(1)

if TEMPLATE_ID == "your_template_id":
    print("ERROR: Please set TEMPLATE_ID in STEP 1 of this script.")
    sys.exit(1)


# ============================================================
# STEP 4: Build the request and send it to Harness
# ============================================================

print(f"Creating workspace '{WORKSPACE_NAME}' from template '{TEMPLATE_ID}' ...")

# The web address (URL) we are sending the request to.
url = f"https://app.harness.io/gateway/iacm/api/orgs/{ORG_ID}/projects/{PROJECT_ID}/workspaces"

# Headers tell Harness who we are and what format we are sending.
headers = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json",
}

# Query parameters tell Harness which account/org/project this belongs to.
params = {
    "accountIdentifier": ACCOUNT_ID,
    "orgIdentifier": ORG_ID,
    "projectIdentifier": PROJECT_ID,
}

# The body says: create this workspace USING our template.
# The template supplies the provisioner + connector + base variables.
# We only pass the runtime details the pipeline gave us.
body = {
    "identifier": WORKSPACE_ID,
    "name": WORKSPACE_NAME,
    "description": "Workspace for the apps team.",
    "org": ORG_ID,
    "project": PROJECT_ID,

    # ---- Reference the workspace template ----
    "template": {
        "identifier": TEMPLATE_ID,
        "version_label": TEMPLATE_VERSION,
    },

    # ---- Repository details from the pipeline (override the template) ----
    "repository": repo,
    "repository_branch": branch,
    "repository_path": folder,

    # ---- The two variables the apps team supplies via the pipeline ----
    "terraform_variables": [
        {"key": "APP_ID", "value": app_id, "value_type": "string"},
        {"key": "BU",     "value": bu,     "value_type": "string"},
    ],
}

# Actually send the request to Harness.
response = requests.post(url, headers=headers, params=params, json=body, timeout=30)


# ============================================================
# STEP 5: Check what Harness said back
# ============================================================
# 200 or 201 = success.  409 = it already exists (also fine).  Anything else = a problem.

if response.status_code in (200, 201):
    print("SUCCESS: Workspace created from template.")
elif response.status_code == 409:
    print("OK: Workspace already exists — nothing to do.")
else:
    print(f"FAILED: Harness returned status {response.status_code}")
    print(response.text)
    sys.exit(1)

# Show a summary of what was set up.
print("")
print("  Workspace :", WORKSPACE_NAME)
print("  Template  :", TEMPLATE_ID, TEMPLATE_VERSION)
print("  Repo      :", repo)
print("  Branch    :", branch)
print("  Folder    :", folder)
print("  APP_ID    :", app_id)
print("  BU        :", bu)
print("")
print("Done. The pipeline can now apply the Terraform template.")

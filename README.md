# Git Batch Utility Command Line Interface

This python package is a CLI utility tool that helps you work faster with Github. 
It supports batch commands to cherry-pick / merge / pull / push to multiple branches at once safely.
Note: You must be in an environment that is already authenticated with a remote Git repository.


Usage:
```
pip install gitutils-cli

gitutils-merge
# Follow instructions on the prompt

gitutils-cherry-pick
# Follow instructions on the prompt
```



# Demo:
```
git:(DV-1563-backend-apis-for-client-p1) ✗ gitbatch_merge

This command safely batch merges changes from one branch to the next in order of input.
It also pushes each branch to remote.

It is helpful when:
- you have a chain of PRs where you need to need to consolidate the changes across all the branches
e.g. `master -> my-working-branch-p1 -> my-working-branch-p2 -> my-working-branch-p3`

- or simply you just want to merge from your personal branch to a shared branch and have it push
e.g. `master -> my-working-branch -> deployment-qa`


Please enter the first branch name or press ENTER for default of current branch: master
Please enter the next branch name or press ENTER to finish: DV-1563-backend-apis-for-client-p1
Please enter the next branch name or press ENTER to finish: foo
Branch foo does not exist. Skipping...
Please enter the next branch name or press ENTER to finish: DV-1563-backend-apis-for-client-p2
Please enter the next branch name or press ENTER to finish: DV-1563-backend-apis-for-client-p3
Please enter the next branch name or press ENTER to finish: DV-1563-backend-apis-for-client-p4
Please enter the next branch name or press ENTER to finish: DV-1563-backend-apis-for-client-p5
Branch DV-1563-backend-apis-for-client-p5 does not exist. Skipping...
Please enter the next branch name or press ENTER to finish:

Checking out branch: master...
...Checked out master
Pulling branch: master...
...Pulled master
Checking out branch: DV-1563-backend-apis-for-client-p1...
...Checked out DV-1563-backend-apis-for-client-p1
Pulling branch: DV-1563-backend-apis-for-client-p1...
...Pulled DV-1563-backend-apis-for-client-p1
Merging branch: master into branch: DV-1563-backend-apis-for-client-p1
...Merged branch: master into branch: DV-1563-backend-apis-for-client-p1
Pushing branch to remote: DV-1563-backend-apis-for-client-p1...
...Pushed to remote: DV-1563-backend-apis-for-client-p1
Checking out branch: DV-1563-backend-apis-for-client-p2...
...Checked out DV-1563-backend-apis-for-client-p2
Pulling branch: DV-1563-backend-apis-for-client-p2...
...Pulled DV-1563-backend-apis-for-client-p2
Merging branch: DV-1563-backend-apis-for-client-p1 into branch: DV-1563-backend-apis-for-client-p2
...Merged branch: DV-1563-backend-apis-for-client-p1 into branch: DV-1563-backend-apis-for-client-p2
Pushing branch to remote: DV-1563-backend-apis-for-client-p2...
...Pushed to remote: DV-1563-backend-apis-for-client-p2
Checking out branch: DV-1563-backend-apis-for-client-p3...
...Checked out DV-1563-backend-apis-for-client-p3
Pulling branch: DV-1563-backend-apis-for-client-p3...
...Pulled DV-1563-backend-apis-for-client-p3
Merging branch: DV-1563-backend-apis-for-client-p2 into branch: DV-1563-backend-apis-for-client-p3
...Merged branch: DV-1563-backend-apis-for-client-p2 into branch: DV-1563-backend-apis-for-client-p3
Pushing branch to remote: DV-1563-backend-apis-for-client-p3...
...Pushed to remote: DV-1563-backend-apis-for-client-p3
Checking out branch: DV-1563-backend-apis-for-client-p4...
...Checked out DV-1563-backend-apis-for-client-p4
Pulling branch: DV-1563-backend-apis-for-client-p4...
...Pulled DV-1563-backend-apis-for-client-p4
Merging branch: DV-1563-backend-apis-for-client-p3 into branch: DV-1563-backend-apis-for-client-p4
Conflict detected, skipping DV-1563-backend-apis-for-client-p4
Back to original branch: DV-1563-backend-apis-for-client-p1

There were conflicts with the following branches. Please manually resolve:
DV-1563-backend-apis-for-client-p4
```

# For Contributers
- Clone the repo and create a branch
- Create a virtualenv with Python >= 3.10.2
- Test a command locally with the -m (module) flag, for instance: `python -m cli.git_batch_merger`
- Run tests: `python -m unittest discover -s cli/tests`

## TODO:
- Handle conflicts dynamically
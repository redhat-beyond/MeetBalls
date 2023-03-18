# Contribution Guide

## Getting Started

### Prerequisites
Please make sure you have the following programs installed:
- [Python 3.9](https://www.python.org/downloads/)
- [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- [Virtual Box](https://www.virtualbox.org/wiki/Downloads)
- [Vagrant](https://www.vagrantup.com/downloads)

### Setting up
1. Clone your fork.
2. Create a new branch.
3. Open any terminal and navigate to the project directory.
4. Run the `vagrant up` command.

After the dependencies were installed and the VM initialized, you can proceed working on the project code.

## Development Process

### Commit Messages
- Separate subject from body with a blank line.
- Limit the subject line to 50 characters.
- Capitalize the subject line.
- Do not end subject line with a period.
- Use the imperative mood in the subject line.
- Wrap the body at 72 characters.
- Use the body to explain what and why vs. how.

For more information and examples, please refer to [this guide](https://cbea.ms/git-commit/#seven-rules).

### Issues
- The title must be clear, and describe what the issue is about. 
- The description of the issue must include a clear explanation about the reasons for doing the work. Also, it should be as small as possible.
- Status Labels(Optional):
  - Status/New - An issue that was just created, in addition unlabeled issues are considered new.
  - Status/Backlog - A issue that was discussed and accepted for work.
  - Status/In progress - An issue that is being worked on.

### Pull Requests
- The Pull Request should not break any of the existing functionality
- Description: the PR description should be as small as possible, and explain what changes have been made, and why.
- In addition, it is required to include the smallest possible amount of files and code logic in every PR.
- Each PR should include no more than 5 `commits`
- To submit a PR, it is mandatory to link it to a relevant issue.
This means that if there is no existing issue that relates to your PR, you must create one before you can submit your request.
Please refer to this 
[guide](https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue#linking-a-pull-request-to-an-issue-using-a-keyword)
for how to link a PR to an issue.
- The pull request will not undergo review until all tests have passed:
    1. A [flake8](https://www.flake8rules.com/) workflow to make sure the PR conforms to proper Python syntax and coding standards.
    2. Automatically checked by a CI system.
- Each pull request requires the approval of at least <ins>2 team members</ins> before merging.
- Each PR should [request reviewers](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/requesting-a-pull-request-review).
Reviewers should be people who are knowledgeable about the code you're modifying or related to the specific issue.
Please refer to this 
[guide](https://docs.github.com/en/issues/tracking-your-work-with-issues/assigning-issues-and-pull-requests-to-other-github-users) 
in order to assign users to PRs and issues.

### Issuing Pull Request
- Title: Make sure the title is short and descriptive enough.
- Body: Do not assume full familiarity with the story or work that has been done.
Imagine that the code reviewer is arriving in your team today without knowing what is going on, and even so, they should be able to understand the changes. 
- Comments: Add comments to the pull request itself. Comment on portions of the code that you think might need further explanation or are complex.
You can also tag people at specific portions of the pull request if you want feedback from them at that point, or you believe that that part concerns them.
- Tests: Make sure there is test coverage for all the code that was introduced. 
 
### Reviewing Pull Requests
- Each PR requires the approval of at least two team members. 
- Examine the PR carefully, and with respect to what it is supposed to achieve.
- If you want to request changes to specific lines in a file please use the "Start a review" button.
- If you want to request changes, mark your review as "Request changes" - please do not use a generic comment.
- Use polite, respectful and clear language when commenting on or reviewing a PR.
- If your PR recieved a request for changes or a comment, please notify the reviewer about your actions
(what changes you made, or if you don't think they're necessary - why you think so).
- Make sure there is test coverage to all the code that was introduced.
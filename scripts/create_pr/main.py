import os
from ghapi.all import GhApi

if __name__ == '__main__':
    base_branch = os.getenv('BASE_BRANCH')
    bot_token = os.getenv('AZURESDK_BOT_TOKEN')
    api = GhApi(owner='Azure', repo='azure-sdk-for-python', token=bot_token)
    pr_title = "auto pr(Do not merge)"
    pr_head = base_branch
    pr_base = 'main'
    pr_body = ""
    api.pulls.create(pr_title, pr_head, pr_base, pr_body)

import os
import logging
import subprocess
from functools import wraps
from typing import List, Any, Dict
from ghapi.all import GhApi

_LOG = logging.getLogger()


def return_origin_path(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        current_path = os.getcwd()
        result = func(*args, **kwargs)
        os.chdir(current_path)
        return result

    return wrapper


def log(cmd: str):
    _LOG.info('==' + cmd + ' ==\n')


def print_exec(cmd: str):
    log(cmd)
    subprocess.call(cmd, shell=True)


def print_exec_output(cmd: str) -> List[str]:
    log(cmd)
    return subprocess.getoutput(cmd).split('\n')


def print_check(cmd):
    log(cmd)
    subprocess.check_call(cmd, shell=True)

class CreatePr:
    """
    This class can generate SDK code, run live test and create RP
    """

    def __init__(self):
        self.base_branch = os.getenv('BASE_BRANCH')
        self.bot_token = os.getenv('AZURESDK_BOT_TOKEN')

    # @staticmethod
    # def checkout_branch(env_key: str, repo: str):
    #     env_var = os.getenv(env_key, "")
    #     usr = env_var.split(":")[0] or "Azure"
    #     branch = env_var.split(":")[-1] or "main"
    #     print_exec(f'git remote add {usr} https://github.com/{usr}/{repo}.git')
    #     print_check(f'git fetch {usr} {branch}')
    #     print_check(f'git checkout {usr}/{branch}')

    def create_pr(self):
        api = GhApi(owner='Azure', repo='azure-sdk-for-python', token=self.bot_token)
        pr_title = "auto pr(Do not merge)"
        pr_head = self.base_branch
        pr_base = 'main'
        pr_body = ""
        api.pulls.create(pr_title, pr_head, pr_base, pr_body)

    def run(self):
        # self.checkout_branch()
        self.create_pr()


if __name__ == '__main__':
    main_logger = logging.getLogger()
    logging.basicConfig()
    main_logger.setLevel(logging.INFO)

    instance = CreatePr()
    instance.run()

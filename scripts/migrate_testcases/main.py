import argparse
import logging
import random
import subprocess as sp
import os
import re
import time

DIREC_PREFIX = 'D:'
DIREC_NAME = 'dev'

# Replace
OLD_TESTCASE = 'AzureMgmtTestCase'
NEW_TESTCASR = 'AzureMgmtRecordedTestCase'
DECORATOR = '    @recorded_by_proxy\n'

PATH = ''
tests = []

_LOG = logging.getLogger()


def my_print(cmd):
    _LOG.info('==' + cmd + ' ==\n')


def print_exec(cmd, path=PATH):
    my_print(cmd)
    sp.call(cmd, shell=True, cwd=path)


def suspend(msg):
    userIn = input(f'==== {msg} (Enter to continue Or other+Enter to stop) ====\n')
    if len(userIn) > 0:
        raise Exception(f'==== Program is over in failure !!! ====')


def add_conftest(path: str):
    path_list = path.split('\\')
    if path_list[-1] != 'tests':
        raise Exception('Path is bad')

    with open(r'.\migrate_testcases\conftest.py', 'r+') as f:
        contest_content = f.read()

    new_content_path = path + '\\conftest.py'

    with open(new_content_path, 'w+') as f:
        f.write(contest_content)


def create_branch(path):
    service = re.findall('sdk\\\\(.*?)\\\\azure-mgmt-', path)[0]
    path = path.split(r'\{}'.format(service))[0]
    print_exec('git remote add azure https://github.com/Azure/azure-sdk-for-python.git', path)
    print_exec('git checkout . && git clean -fd', path)
    print_exec('git fetch azure main', path)
    print_exec('git checkout azure/main', path)
    time.sleep(5)
    date = time.localtime(time.time())
    branch = 'migrate-{}-toTestProxy-{:02d}{:02d}-{}'.format(service, date.tm_mon,date.tm_mday, random.randint(1000, 9999))

    print_exec(f'git branch -D {branch}', path)
    print_exec(f'git checkout -b {branch}', path)
    return service


def set_env_variables():
    txt_path = r'.\migrate_testcases\livetest_envvar.txt'
    mgmt_settings_real_path = r'.\migrate_testcases\mgmt_settings_real.py'
    target_path = r'.\azure-sdk-for-python\tools\azure-sdk-tools\devtools_testutils\mgmt_settings_real.py'
    with open(txt_path, 'r') as f:
        for line in f.readlines():
            key, value = line.split('=')
            os.environ[key] = value.strip('\n').strip(r'"')
    if not os.path.exists(target_path):
        with open(mgmt_settings_real_path, 'r') as f:
            content = f.read()
        with open(target_path, 'w+') as f:
            f.write(content)

def update_requirement(path):
    requirement_path = path.replace('tests', '')+'dev_requirements.txt'
    print(requirement_path)
    with open(requirement_path, 'a+') as f1:
        f1.seek(0, 0)
        if 'azure-identity' not in f1.read():
            f1.write('\n../../identity/azure-identity')


def prepare_env(path):
    above_path = path.replace("\\tests", "")
    print_exec('pip install -r dev_requirements.txt', above_path)
    print_exec('python setup.py install', above_path)


def add_certifi(env_name):
    cacert_path = env_name + r'\Lib\site-packages\certifi\cacert.pem'
    with open(cacert_path, 'a+') as f:
        f.seek(0, 0)
        if certification[-65:-28] not in f.read():
            f.write(certification)
            print("===========Added certification into cacert.pem==========")


def find_tests(path):
    cont = 0
    for root, dirs, files in os.walk(path):
        for filename in files:
            if re.findall('^test_(.*?).py$', filename) and 'azure-mgmt-' in root:
                tests.append(root + '\\' + filename)
                cont += 1

    print(f'=====Find {cont} tests=======')
    print(tests)
    return tests


def update_test(path):
    with open(path, 'r+') as f1:
        # for import recorded_by_proxy
        flag = 0
        new_lines = ''
        classname = ''
        '''
        Rules:
          1. change `AzureMgmtTestCase` to `AzureMgmtRecordedTestCase` and add `recorded_by_proxy`
          2. eg: change `MgmtResourceLocksTest` to `TestMgmtResourceLocks`
          3. change `def setUp(self):` to `def setup_method(self, method):`
          4. add `@recorded_by_proxy` above the `def test_xxxxx`
          5. change `assertXXXX methods` to `assert`  
        '''

        for line in f1:
            if OLD_TESTCASE in line:
                line = re.sub(OLD_TESTCASE, NEW_TESTCASR, line)
                if flag == 0:
                    line = line.strip('\n') + ', recorded_by_proxy\n'
                    flag += 1

            if 'class ' in line:
                classname = re.findall('class (.*?)Test\(', line)[0]
                line = re.sub(classname + 'Test', 'Test' + classname, line)
            if 'def setUp' in line:
                line = re.sub('setUp\(self\)', 'setup_method(self, method)', line)
            if f'super({classname}Test, self).setUp()' in line:
                continue
            if 'def test_' in line:
                line = DECORATOR + line
            if 'self.assert' in line:
                if 'assertGreater' in line:
                    line = re.sub('self.assertGreater\((.*),(.*)\)', r'assert \g<1> >=\g<2>', line)
                if 'assertTrue' in line:
                    line = re.sub('self.assertTrue\((.*)\)', r'assert \g<1>', line)
                if 'assertIsNotNone' in line:
                    line = re.sub('self.assertIsNotNone\((.*)\)', r'assert \g<1> is not None', line)
                if 'assertEqual' in line:
                    line = re.sub('self.assertEqual\((.*),(.*)\)', r'assert \g<1> ==\g<2>', line)
                if 'assertIn' in line:
                    line = re.sub('self.assertIn\((.*),(.*)\)', r'assert \g<1> in\g<2>', line)
                if 'assertIsNone' in line:
                    line = re.sub('self.assertIsNone\((.*)\)', r'assert \g<1> is None', line)
                if 'assertFalse' in line:
                    line = re.sub('self.assertFalse\((.*)\)', r'assert not \g<1>', line)
                if 'assertNotEqual' in line:
                    line = re.sub('self.assertNotEqual\((.*),(.*)\)', r'assert \g<1> !=\g<2>', line)
                if 'assertIsInstance' in line:
                    line = re.sub('self.assertIsInstance\((.*),(.*)\)', r'assert isinstance(\g<1>,\g<2>)', line)
                if 'assertRaises' in line:
                    line = re.sub('with self.assertRaises', r'with pytest.raises', line)
                if 'assertListEqual' in line:
                    line = re.sub('self.assertListEqual\((.*),(.*)\)', r'assert \g<1> ==\g<2>', line)
            if 'self.settings.SUBSCRIPTION_ID' in line:
                line = re.sub('self\.settings\.SUBSCRIPTION_ID', 'self.get_settings_value("SUBSCRIPTION_ID")', line)

            new_lines += line

    # print(new_lines)
    with open(path, 'w+') as f2:
        f2.write(new_lines)


def run_tests(path):
    print_exec('pytest ../tests', path)
    env_print(path)
    suspend('Test complete')


def delete_yamls(path):
    cont = 0
    for root, dirs, files in os.walk(path):
        for filename in files:
            if re.findall('^test_(.*?).yaml$', filename) and 'azure-mgmt-' in root:
                os.remove(root + '\\' + filename)
                cont += 1

    print(f'=====Delete {cont} yamls=======')


def update_ci_yaml(path):
    ci_path = path.split(r'\azure-mgmt-')[0]+'\\ci.yml'
    print(ci_path)
    new_lines = ''
    flag = 0
    with open(ci_path, 'r+') as f:
        if 'TestProxy' not in f.read():
            flag = 1
            f.seek(0, 0)
            for line in f:
                if 'ServiceDirectory' in line:
                    line += '    TestProxy: true\n'
                new_lines += line
    print(new_lines)
    if flag == 1:
        with open(ci_path, 'w+') as fw:
            fw.write(new_lines)


def commit_test(path):
    service_path = path.split(r'\azure-mgmt-')[0]
    print_exec('git add .', service_path)
    print_exec('git commit -m \"migrate tests\"', service_path)
    print_exec('git push -f origin HEAD', service_path)
    # suspend('Push complete')


def create_pr(service, path):
    print_exec('pip install ghapi', path)
    from ghapi.all import GhApi
    api = GhApi(owner='Azure', repo='azure-sdk-for-python', token=os.environ['GIT_TOKEN'])
    origin_url = sp.check_output('git remote get-url origin', cwd=path)
    branch = sp.check_output('git symbolic-ref --short -q HEAD', cwd=path)
    user_name = re.findall('/github.com/(.*?)/azure', origin_url.decode())[0]
    pr_title = f"Migrate {service} to testProxy (Do not merge)"
    pr_head = "{}:{}".format(user_name, branch.decode().strip('\n'))
    pr_base = 'main'
    pr_body = 'TestProxy'
    api.pulls.create(pr_title, pr_head, pr_base, pr_body)


def env_print(path):
    print('============== ENV Variable =================')
    print_exec('set AZURE_SUBSCRIPTION_ID', path)
    print_exec('set AZURE_TENANT_ID', path)
    print_exec('set AZURE_TEST_RUN_LIVE', path)



def get_name():
    idx = DIREC_PREFIX.rfind('\\')
    return DIREC_PREFIX[idx + 1:]

def main():
    # eg1: path = r'D:\dev2\azure-sdk-for-python\sdk\search\azure-mgmt-search\tests'
    DIREC_PREFIX = os.getcwd()
    DIREC_NAME = get_name()

    parser = argparse.ArgumentParser(
        description=r"""Setting, update, push automatically.
            usage examples:
            1. python .\migrate_testcases\main.py --path D:\dev3\azure-sdk-for-python\sdk\search\azure-mgmt-search\tests --env venv3 """,
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-p', '--path',
                        dest='path', help='service tests folder path')
    parser.add_argument('-e', '--env',
                        dest='env', help='python venv name')

    args = parser.parse_args()
    PATH = args.path
    ENV_NAME = args.env

    # prepare env
    SERVICE = create_branch(PATH)
    set_env_variables()
    update_requirement(PATH)
    prepare_env(PATH)
    add_certifi(ENV_NAME)
    add_conftest(PATH)

    # run test
    tests = find_tests(PATH)
    for test in tests:
        update_test(test)
    run_tests(PATH)
    delete_yamls(PATH)
    update_ci_yaml(PATH)
    commit_test(PATH)
    time.sleep(2)
    create_pr(SERVICE, PATH)
    env_print(PATH)


certification = '''
-----BEGIN CERTIFICATE-----
MIIDSDCCAjCgAwIBAgIUPMKpJ/j10eQrcQBNnkImIaOYHakwDQYJKoZIhvcNAQEL
BQAwFDESMBAGA1UEAwwJbG9jYWxob3N0MB4XDTIxMDgwNTAwMzU1NloXDTIyMDgw
NTAwMzU1NlowFDESMBAGA1UEAwwJbG9jYWxob3N0MIIBIjANBgkqhkiG9w0BAQEF
AAOCAQ8AMIIBCgKCAQEAxe/ZseXgOTVoF7uTjX5Leknk95jIoyGc+VlxA8BhzGOr
r4u6VNQZRCMq+svHY36tW4+u/xHNe2kvbwy2mnS8cFFLfst+94qBZVJDBxSGZ9I/
wekErNsjFsik4UrMvcC+ZlGPh7hb3f7tSx29tn1DIkAUXVnbZ6TT5s+mYRQpZ6fW
6kR3RNfc0A1IUM7Zs9yfNEr0O2H41P2HcLKoOPtvd7GvTQm9Ofh3srKvII+sZn/J
WH7r76oRQMX904mOMdryQwZLObsqX4dXIEbafKVSecB3PBVIhv8gVtJhcZbQP1pI
mMiWd6PHv46ZhGf7+cKnYUSa8Ia2t/wetK1wd00dFwIDAQABo4GRMIGOMA8GA1Ud
EwEB/wQFMAMBAf8wDgYDVR0PAQH/BAQDAgGmMBYGA1UdJQEB/wQMMAoGCCsGAQUF
BwMBMBcGA1UdEQEB/wQNMAuCCWxvY2FsaG9zdDA6BgorBgEEAYI3VAEBBCwMKkFT
UC5ORVQgQ29yZSBIVFRQUyBkZXZlbG9wbWVudCBjZXJ0aWZpY2F0ZTANBgkqhkiG
9w0BAQsFAAOCAQEAIj2VlBVcXGSly6KCBg6lgwFi+henWfSox77iuGAaAxDjN3jd
9lZahW4MPNLHKSrPRb4YNSLZ2jh7zdcttQrqd4qH65o1q56q5JrCmli99iIzY9Y8
RdYyxK4Zzr31wjpsyFiWQfqJTuSFUUg9uDDj0negwEZLIGlt7nr12wflt2+QOJtD
byMeSZLbB5dPzn341DK0qfJEJMMgL0XsPEVZ3TQ6Alc9zq5wI608C/mXnz3xJE05
UTYD8pRJJ/DyG0empvOVE8Sg93msHPquAbgqO9aqCpykgg/a8CFvI4wRdfvGEFlv
8XJKL8Y/PFsmFeO3axq3zUYKFVdc9Un4dFIaag==
-----END CERTIFICATE-----
'''

if __name__ == '__main__':
    main()

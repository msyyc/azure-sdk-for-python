# add actual value (begin)


SUBSCRIPTION_ID = ''
CLIENT_ID = ''
CLIENT_SECRET = ''
TENANT_ID = ''
GIT_TOKEN = ''
AZURE_TEST_RUN_LIVE = 'yes'

# add actual value (end)

def replace_func(line):
    return line.replace('{TENANT_ID}', TENANT_ID).replace('{CLIENT_ID}', CLIENT_ID).replace('{CLIENT_SECRET}',
                        CLIENT_SECRET).replace('{SUBSCRIPTION_ID}', SUBSCRIPTION_ID).replace('{GIT_TOKEN}',
                        GIT_TOKEN).replace('{AZURE_TEST_RUN_LIVE}', AZURE_TEST_RUN_LIVE)


# generate files needed for livetest
with open('livetest_envvar_.txt', 'r') as fine_in:
    in_con = fine_in.readlines()
for i in range(0, len(in_con)):
    in_con[i] = replace_func(in_con[i])
with open('livetest_envvar.txt', 'w') as fine_out:
    fine_out.writelines(in_con)

with open('mgmt_settings_real_.py', 'r') as fine_in:
    in_con = fine_in.readlines()
for i in range(0, len(in_con)):
    in_con[i] = replace_func(in_con[i])
with open('mgmt_settings_real.py', 'w') as fine_out:
    fine_out.writelines(in_con)

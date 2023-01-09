import os

import requests

# 平台
archs = ['x86_64', 'arm64', 'arm', 's390x', 'ppc64le']
# 获取 https://gitlab.com/gitlab-org/gitlab-runner/ 最新20个标签的 URL
# 250833：是项目 https://gitlab.com/gitlab-org/gitlab-runner/ 的 ID
tags_url = 'https://gitlab.com/api/v4/projects/250833/repository/tags'
# 从环境变量中获取参数
num = os.getenv("num")

resp = requests.get(tags_url)

resp_json = resp.json()

file_name = 'tags.sh'
if os.path.exists(file_name):
    os.remove(file_name)

file = open(file_name, 'w')

i = 0
for tag in resp_json:
    i = i + 1
    for arch in archs:
        msg = f"docker pull registry.gitlab.com/gitlab-org/gitlab-runner/gitlab-runner-helper:{arch}-{tag['name']}"
        print(msg)
        file.write(msg)
        file.write('\n')
    if num is not None and i >= num:
        break

file.write('\n')

i = 0
for tag in resp_json:
    i = i + 1
    for arch in archs:
        msg = f"docker tag registry.gitlab.com/gitlab-org/gitlab-runner/gitlab-runner-helper:{arch}-{tag['name']} $DOCKER_USERNAME/gitlab-runner-helper:{arch}-{tag['name']}"
        print(msg)
        file.write(msg)
        file.write('\n')
    if num is not None and i >= num:
        break

file.write('\n')

i = 0
for tag in resp_json:
    i = i + 1
    for arch in archs:
        msg = f"docker push $DOCKER_USERNAME/gitlab-runner-helper:{arch}-{tag['name']}"
        print(msg)
        file.write(msg)
        file.write('\n')
    if num is not None and i >= num:
        break

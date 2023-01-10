import os

import requests

# 平台
archs = ['x86_64', 'arm64', 'arm', 's390x', 'ppc64le']
# 获取 https://gitlab.com/gitlab-org/gitlab-runner/ 最新20个标签的 URL
# 获取项目ID：https://gitlab.com/api/v4/projects/gitlab-org%2Fgitlab-runner
# 250833：是项目 https://gitlab.com/gitlab-org/gitlab-runner/ 的 ID
# 参见议题：https://gitlab.com/xuxiaowei-com-cn/gitlab-runner-helper/-/issues/1
# tags_url = 'https://gitlab.com/api/v4/projects/gitlab-org%2Fgitlab-runner/repository/tags'
tags_url = 'https://gitlab.com/api/v4/projects/250833/repository/tags'
# 从环境变量中获取参数
num = os.getenv("num")
print(f'num={num}')
page = os.getenv("page")
print(f'page={page}')

if num is not None:
    num = int(num)
if page is not None:
    page = int(page)
    tags_url += f'?page={page}'

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
        image = f"registry.gitlab.com/gitlab-org/gitlab-runner/gitlab-runner-helper:{arch}-{tag['name']}"
        msg = f"docker pull {image} || echo '不存在：{image}'"
        print(msg)
        file.write(msg)
        file.write('\n')

        image = f"registry.gitlab.com/gitlab-org/gitlab-runner/gitlab-runner-helper:{arch}-{tag['commit']['short_id']}"
        msg = f"docker pull {image} || echo '不存在：{image}'"
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
        image = f"registry.gitlab.com/gitlab-org/gitlab-runner/gitlab-runner-helper:{arch}-{tag['name']}"
        msg = f"docker tag {image} $DOCKER_USERNAME/gitlab-runner-helper:{arch}-{tag['name']} || echo '打标签失败：{image}'"
        print(msg)
        file.write(msg)
        file.write('\n')

        image = f"registry.gitlab.com/gitlab-org/gitlab-runner/gitlab-runner-helper:{arch}-{tag['commit']['short_id']}"
        msg = f"docker tag {image} $DOCKER_USERNAME/gitlab-runner-helper:{arch}-{tag['commit']['short_id']} || echo '打标签失败：{image}'"
        print(msg)
        file.write(msg)
        file.write('\n')

    if num is not None and i >= num:
        break

images=$(docker images | grep $DOCKER_USERNAME/gitlab-runner-helper | awk '{print $1":"$2}')

for image in $images
do
  echo "准备推送：$image"
  docker push $image && echo "推送完成：$image"
done

#!/bin/bash

if [ -z "$1" ]; then
  echo "Usage: $0 '<commit message>'"
  echo "Exiting script."
  exit 1
fi 

commit_message="$1"

echo "Logging into OCI container registry..."
docker login iad.ocir.io

echo "Build new image of OCI function..."
docker build -t iad.ocir.io/idf9gv5rieyl/chrono-metrics-functions/chrono-function-metrics:latest . --no-cache

echo "Pushing image to OCI container registry..."
push_output=$(docker push iad.ocir.io/idf9gv5rieyl/chrono-metrics-functions/chrono-function-metrics:latest)

image_digest=$(echo "$push_output" | grep "digest: " | awk '{print $3}')
echo "Image digest: $image_digest"

# terraform_file="../functions.tf"
# sed -i '' "s|image_digest = \".*\"|image_digest = \"$image_digest\"|" $terraform_file

# echo "Updated Terrform file:"
# grep "image_digest = " $terraform_file

cd ..
git add .
git commit -m "$commit_message"
git push origin modify-oci-function

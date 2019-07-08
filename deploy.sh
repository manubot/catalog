#!/usr/bin/env bash

## deploy.sh: run during a Travis CI build to deploy output directory to the gh-pages branch on GitHub.
## References
## - https://github.com/manubot/rootstock/blob/ddb0288895cd5bc5dab117fb366c52216a717d0e/ci/deploy.sh
## - https://github.com/wp-cli/wp-cli/issues/3798

# Set options for extra caution & debugging
set -o errexit \
    -o nounset \
    -o pipefail

eval "$(ssh-agent -s)"
# Ensure command traces are disabled while dealing with the private key
[[ "$SHELLOPTS" =~ xtrace ]] && XTRACE_ON=1
[[ "${XTRACE_ON:-}" ]] && set +o xtrace && echo "xtrace disabled"
echo -e "$GITHUB_DEPLOY_PRIVATE_KEY" | ssh-add -
[[ "${XTRACE_ON:-}" ]] && set -o xtrace && echo "xtrace reenabled"

# Configure git
git config --global push.default simple
git config --global user.name "Travis CI"
git config --global user.email "travis@travis-ci.com"
git checkout "$TRAVIS_BRANCH"
git remote set-url origin "git@github.com:$TRAVIS_REPO_SLUG.git"

# Fetch and create gh-pages branch
# Travis does a shallow and single branch git clone
git remote set-branches --add origin gh-pages
git fetch origin gh-pages:gh-pages

commit_message="\
Generate catalog output on $(date --iso --utc)

built by $TRAVIS_JOB_WEB_URL
based on https://github.com/$TRAVIS_REPO_SLUG/commit/$TRAVIS_COMMIT

[skip ci]
"
# echo >&2 "$commit_message"

ghp-import \
  --push --no-jekyll \
  --message="$commit_message" \
  output


# Trigger CI of https://github.com/manubot/manubot.org to rebuild https://manubot.org/catalog/
# See https://github.com/manubot/manubot.org/issues/22
# Code based on https://github.com/plume-lib/trigger-travis/blob/e315da26ee7b961775985abe60238c10646f6392/trigger-travis.sh#L51-L70 (MIT Licensed)
TRAVIS_API_CALL_BODY="{
  \"request\": {
    \"branch\": \"master\",
    \"message\": \"Triggered by ${TRAVIS_JOB_WEB_URL:-local API call}\"
  }
}"

TRAVIS_API_RESPONSE_FILE="/tmp/travis-request-output-${BASHPID:-pid}.txt"

[[ "${XTRACE_ON:-}" ]] && set +o xtrace && echo "xtrace disabled"
curl --silent --request POST \
  --header "Content-Type: application/json" \
  --header "Accept: application/json" \
  --header "Travis-API-Version: 3" \
  --header "Authorization: token ${TRAVIS_ACCESS_TOKEN}" \
  --data "$TRAVIS_API_CALL_BODY" \
  https://api.travis-ci.com/repo/manubot%2Fmanubot.org/requests \
  | tee $TRAVIS_API_RESPONSE_FILE && echo
[[ "${XTRACE_ON:-}" ]] && set -o xtrace && echo "xtrace reenabled"

if grep --quiet --count '"@type": "error"' $TRAVIS_API_RESPONSE_FILE; then
  echo "Exiting with nonzero status code becaue Travis API returned an error"
  exit 1
fi

## Setting up `Commit-TimeLog` (ver Python, GitActions)

<div align='center'>
<img src='https://raw.githubusercontent.com/pozuhtuhv/service_ACTIVITY_TIMES/main/sample.png'>
</div>

## 0. Prerequisites
- Fork the repository, and proceed with the forked repository.

### 1. Generate Personal Access Token
1. Go to [Personal Access Token generation page](https://github.com/settings/tokens) on GitHub.
2. Click on "Generate new token."
3. Check the `repo` and `gists` permissions and set the expiration period.
4. Click "Generate token" to create the token.
5. Copy the generated token.

### 2. Create a Gist
1. Go to the [Gist](https://gist.github.com/) page and create a new Gist.
2. Fill in the remaining fields (title, content can be anything).
3. Click "Create public gist" to generate the Gist (create as public gist).
4. Copy the ID from the Gist URL.
   - Example: https://gist.github.com/yourname/************* (Copy the ************* part).

### 3. Add Secrets to Your Repository
1. Go to your repository's Settings -> Secrets and variables -> Actions.
2. Click on "New repository secret."
3. In the Name field, enter `ACCESS_TOKEN`, and paste the previously copied Personal Access Token.
4. Click "Add secret" to save.
5. Similarly, create a new secret with `GIST_ID` as the Name, and paste the Gist ID.
6. Click "Add secret" to save.
7. Lastly, add a secret with `USER_NAME` as the Name, and input your GitHub username.
8. Click "Add secret" to save.

### 4. Reference Documentation
- [Commit search] : https://docs.github.com/ko/search-github/searching-on-github/searching-commits
- [Search Rank] : https://docs.github.com/ko/rest/search/search?apiVersion=2022-11-28#ranking-search-results
- [Gist content update] : https://docs.github.com/ko/rest/reference/gists#update-a-gist-comment
- [Original Repo] : https://github.com/maxam2017/productive-box

## Thanks for reading!

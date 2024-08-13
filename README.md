# ai-whisper

openai-whisper

## 安装指南
确保使用的python 版本为3.10.x
```shell
pip install poetry
poetry config virtualenvs.in-project true
poetry env use python
poetry shell
poetry install --no-root
poetry run uvicorn app.main:app --reload --host 0.0.0.0
```
## 如果使用docker 与 docker-compose
```shell
docker-compose up -d --build 
```

## Add your files

- [ ] [Create](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#create-a-file) or [upload](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#upload-a-file) files
- [ ] [Add files using the command line](https://docs.gitlab.com/ee/gitlab-basics/add-file.html#add-a-file-using-the-command-line) or push an existing Git repository with the following command:

```
cd existing_repo
git remote add origin http://git.purvar.local/ai/ai-whisper.git
git branch -M main
git push -uf origin main
```
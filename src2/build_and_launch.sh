docker build -t hackathon-final-app .
docker run -p 8080:8080 --name hackathon-runner -d hackathon-final-app

# Проверь логи, чтобы убедиться, что все запустилось и ты видишь список моделей GigaChat:

docker logs hackathon-runner
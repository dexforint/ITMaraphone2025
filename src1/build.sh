cd src
docker build -t final .
docker run -p 8080:8080 --env GIGACHAT_TOKEN=YOUR_TOKEN final
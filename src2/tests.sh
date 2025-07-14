curl -X POST http://localhost:8080/inputs -H "Content-Type: application/json" -d '{"view": [[2,1,0],[0,3,1]]}'

curl -X POST http://localhost:8080/inputs -H "Content-Type: application/json" -d '{"view": [2,1,0,0,3,1]}'

curl -X POST http://localhost:8080/tasks -H "Content-Type: application/json" -d '{"type": "Question", "task": "Ты готов?"}'

curl -X PATCH http://localhost:8080/tasks/last -H "Content-Type: application/json" -d '{"result": "Ok"}'

curl -X PATCH http://localhost:8080/tasks/last -H "Content-Type: application/json" -d '{"result": "Fail"}'

curl -X POST http://localhost:8080/notifications -H "Content-Type: application/json" -d '{"type": "PreparationDone", "desc": "Ждем тебя в финале!"}'
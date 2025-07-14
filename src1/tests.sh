# 1
curl -X POST http://localhost:8080/inputs \
     -H "Content-Type: application/json" \
     -d '{"view": [[2,1,0],[0,3,1]]}'
# → 200 {"action":"Something"}

# 2
curl -X POST http://localhost:8080/inputs \
     -H "Content-Type: application/json" \
     -d '{"view": [2,1,0,0,3,1]}'
# → 400 {"action":"None"}

# 3
curl -X POST http://localhost:8080/tasks \
     -H "Content-Type: application/json" \
     -d '{"type":"Question","task":"Ты готов?"}'
# → 200 {"answer":"Да"}

# 4
curl -X PATCH http://localhost:8080/tasks/last \
     -H "Content-Type: application/json" \
     -d '{"result":"Ok"}'
# → 200

# 5 (почти сразу)
curl -X PATCH http://localhost:8080/tasks/last \
     -H "Content-Type: application/json" \
     -d '{"result":"Fail"}'
# → 404

# 6
curl -X POST http://localhost:8080/notifications \
     -H "Content-Type: application/json" \
     -d '{"type":"PreparationDone","desc":"Ждем тебя в финале!"}'
# → 200
cd src
python -m venv venv && . venv/bin/activate
pip install -r requirements.txt
export GIGACHAT_TOKEN="your_token_if_any"
uvicorn main:app --reload
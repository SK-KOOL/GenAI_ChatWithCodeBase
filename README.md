# GenAI_ChatWithCodeBase
User can Upload a git repository and user can interact with system and ask about the uploaded repository functionalities / technologies etc.

Project Dependencies - 
    Node.Js
    Python
    Ollama
    Mysql
    Angular(21) (Used for Frontend)

To Install Angular, Use below Command.

npm install -g @angular/cli


To Start the Project folow the steps.

Clone / download the Project.

install python 3.11

install ollama

pull ollama packages

ollama pull llama3 ollama pull deepseek-coder ollama pull codellama ollama pull nomic-embed-text

run ollama

inside backend folder from cmd, open virtual environment (venv) python -m venv venv

venv\Scripts\activate

install dependencies through backend\requirements.txt pip install -r requirements.txt

start backend through below command

uvicorn app.main:app --reload (API Docs : http://127.0.0.1:8000/docs)

open new tab and go to frontend folder

Install all node_modules Packages through below command

npm install

Then start front end

ng s --o (default port : 4200)

For Database, execute the Sample_Database.sql script file in your Mysql database.

Note : Update .env file inside Backend folder with your DB or other credentials.

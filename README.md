# chatbot
Chatbot utilizando modelagem bag of word.

Atividade proposta:
PP.3.13. Desenvolva um chabot, utilizando modelagem bag of words, que pode ser utilizado para 
auxiliar o usuário a navegar em uma aplicação web. Seu chabot pode ter uma interface via 
prompt de comando ou web. Ele deve ser capaz de responder a perguntas tais como "Como 
instalo um programa xyz?". Quando o usuário utiliza uma palavra tal como "sair" ou "quero sair" 
a aplicação deve ser encerrada ou o chatbot deve se despedir do usuário. 

Como rodar o projeto:

Clone o projeto:
```
    git clone https://github.com/igorpereira28/chatbot.git
```


Abra a pasta do backend, crie um ambiente virtual:
```
    cd chatbot/backend
    python -m venv venv
```

Acesse o ambiente virtual:
```
    venv/Scripts/activate
```

Instale as dependencias
```
    pip install -r requirements.txt
```

Rode o projeto
```
    python app.py
```

Acesse no navegador:
http://127.0.0.1:5000
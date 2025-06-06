import numpy as np
import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer

nltk.download("stopwords")
nltk.download('rslp')

class Chatbot:
    def __init__(self):
        self.exit_keywords = ["sair", "quero sair", "tchau", "adeus", "encerrar"]

        self.questions = [
            "como instalo o programa1",
            "como instalo o programa2",
            "como instalo o programa3",
            "como navegar na aplicação",
            "como faço login",
            "como altero minha senha",
            "como reconfigurar a senha",
            "como sair do sistema",
            "como enviar um relatório",
            "como editar meu perfil",
            "como cadastrar um novo usuário",
            "quais são os atalhos do sistema",
            "como acessar as configurações"
        ]

        self.answers = [
            "Para instalar o programa X, vá em 'Instalar X' na aba principal.",
            "Para instalar o programa Y, vá até configurações > aplicativos > instalar Y.",
            "Use o comando 'sudo apt install z' para instalar o programa Z.",
            "Utilize o menu lateral ou os atalhos no topo da tela para navegar.",
            "Clique em 'Entrar' no canto superior e digite seu login.",
            "Acesse seu perfil e clique em 'Alterar Senha'.",
            "Clique em 'Esqueci minha senha' na tela de login.",
            "Clique em 'Sair' no canto superior direito da aplicação.",
            "Clique em 'Relatórios' e depois em 'Novo Relatório'.",
            "Acesse 'Perfil' > 'Editar'.",
            "Em 'Usuários', clique em 'Novo Usuário' e preencha o formulário.",
            "Atalhos: Ctrl+S (salvar), Ctrl+F (buscar), Esc (voltar).",
            "Clique no ícone de engrenagem no canto superior para abrir as configurações."
        ]

        self.vectorizer = TfidfVectorizer(preprocessor=self.preprocess)
        self.vectorizer.fit(self.questions)

    def preprocess(self, text):
        # Remove pontuações, deixa tudo minúsculo, aplica stemmer e remove stopwords
        text = text.lower()
        text = re.sub(r"[{}]".format(string.punctuation), "", text)

        tokens = text.split()
        stop_words = set(stopwords.words("portuguese"))
        stemmer = RSLPStemmer()

        filtered = [stemmer.stem(w) for w in tokens if w not in stop_words]
        return " ".join(filtered)

    def get_response(self, user_input):
        if any(exit_word in user_input.lower() for exit_word in self.exit_keywords):
            return "Até logo! Encerrando o atendimento."

        user_vec = self.vectorizer.transform([user_input])
        known_vecs = self.vectorizer.transform(self.questions)

        sim_scores = cosine_similarity(user_vec, known_vecs)
        index = np.argmax(sim_scores)

        if sim_scores[0, index] < 0.3:
            return (
                "Desculpe, não entendi sua pergunta. Você pode tentar algo como:\n"
                "- Como faço login?\n"
                "- Como instalo o programa X?\n"
                "- Como alterar minha senha?\n"
                "- Quais os atalhos do sistema?"
            )
        return self.answers[index]

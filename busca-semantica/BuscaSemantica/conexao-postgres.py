# app.py
import psycopg2
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Conexão PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="senha123"
)
cursor = conn.cursor()

# Criar tabela (se não existir)
cursor.execute("""
CREATE TABLE IF NOT EXISTS textos (
    id SERIAL PRIMARY KEY,
    texto TEXT NOT NULL
)
""")
conn.commit()

# Textos para inserir
documentos = [
    "Receita de bolo de chocolate fofinho: bata ovos, açúcar e manteiga até formar um creme. Adicione farinha de trigo, chocolate em pó e fermento. Asse em forno médio e cubra com brigadeiro feito de leite condensado, chocolate e manteiga.",
    "Panqueca americana: misture farinha, leite, ovos e fermento até formar uma massa cremosa. Frite em frigideira antiaderente e sirva com maple syrup e frutas vermelhas.",
    "Arroz de forno com frango: refogue frango desfiado com cebola e alho, misture com arroz cozido, milho, ervilha e molho de tomate. Cubra com queijo e leve ao forno para gratinar.",
    "Salada Caesar: rasgue folhas de alface romana, adicione croutons, queijo parmesão e molho Caesar à base de anchova, alho, limão e mostarda.",
    "Lasanha de berinjela: grelhe fatias de berinjela, intercale com molho de tomate, queijo e leve ao forno até gratinar.",
    "Sopa de legumes caseira: cozinhe cenoura, batata, abobrinha e chuchu em caldo temperado com alho, cebola e salsinha. Bata parte da sopa no liquidificador para dar cremosidade.",
    "Risoto de cogumelos: refogue arroz arbóreo com cebola, adicione vinho branco e vá acrescentando caldo aos poucos. Adicione cogumelos refogados e finalize com manteiga e parmesão.",
    "Frango ao curry: frite pedaços de frango, adicione curry em pó, leite de coco e deixe cozinhar até engrossar. Sirva com arroz basmati.",
    "Torta de maçã: forre uma forma com massa folhada, recheie com maçãs fatiadas, açúcar e canela. Cubra com mais massa e leve ao forno até dourar.",
    "Espaguete ao alho e óleo: cozinhe o macarrão, frite alho fatiado em azeite e adicione o macarrão escorrido. Finalize com pimenta vermelha e salsinha.",
    "Quiche de alho-poró: prepare uma massa podre, recheie com alho-poró refogado e uma mistura de creme de leite, ovos e queijo. Asse até firmar.",
    "Hambúrguer artesanal: molde carne moída temperada, grelhe e sirva no pão com queijo cheddar, bacon crocante, alface e tomate.",
    "Mousse de maracujá: bata no liquidificador leite condensado, creme de leite e suco concentrado de maracujá. Leve à geladeira até firmar.",
    "Pão de queijo mineiro: misture polvilho azedo, leite quente, ovos e queijo meia cura ralado. Modele e asse até dourar.",
    "Crepioca: misture ovo com goma de tapioca e queijo, tempere com sal e ervas finas. Cozinhe na frigideira dos dois lados.",
    "Bife acebolado: tempere bifes com sal e alho, frite e reserve. Na mesma panela, refogue cebolas em rodelas. Sirva com arroz e feijão tropeiro.",
    "Bolinho de chuva: misture ovos, açúcar, leite e farinha. Frite colheradas da massa em óleo quente e passe no açúcar com canela.",
    "Caldo verde: cozinhe batatas, bata no liquidificador, volte à panela com couve fatiada e linguiça calabresa. Deixe ferver e sirva quente.",
    "Chili con carne: refogue carne moída, adicione feijão cozido, tomate, pimentão e especiarias como cominho e páprica. Cozinhe até engrossar.",
    "Brigadeiro tradicional: cozinhe leite condensado, chocolate em pó e manteiga até desgrudar da panela. Enrole e passe no granulado."
]

# Limpar tabela (opcional)
cursor.execute("DELETE FROM textos")
conn.commit()

# Inserir textos
for doc in documentos:
    cursor.execute("INSERT INTO textos (texto) VALUES (%s)", (doc,))
conn.commit()

# Buscar IDs e textos para gerar embeddings
cursor.execute("SELECT id, texto FROM textos ORDER BY id")
rows = cursor.fetchall()

# Modelo de embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")

texts = [row[1] for row in rows]
ids = [row[0] for row in rows]

# Gera embeddings normalizados
embeddings = model.encode(texts, normalize_embeddings=True).astype("float32")

# Cria índice FAISS
index = faiss.IndexFlatIP(embeddings.shape[1])
index.add(embeddings)

# Salva índice no disco
faiss.write_index(index, "faiss.index")

print("📦 Banco PostgreSQL e índice FAISS criados com sucesso!")

# Fecha conexão (pode deixar aberta se quiser continuar)
cursor.close()
conn.close()

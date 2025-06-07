# busca.py
import psycopg2
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Configuração da conexão PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="senha123"
)
cursor = conn.cursor()

# Carregar índice FAISS salvo no disco
index = faiss.read_index("faiss.index")

# Carregar modelo de embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")

# --- IMPORTANTE --- 
# Precisamos mapear o índice FAISS (posição no índice) para o ID do banco.
# Se você usou o script anterior, os IDs do banco começaram em 1, e FAISS indexa começando em 0.
# Vamos carregar essa correspondência da tabela textos e assumir ordem por id ASC:

cursor.execute("SELECT id FROM textos ORDER BY id")
db_ids = [row[0] for row in cursor.fetchall()]

faiss_to_db_id = {faiss_idx: db_id for faiss_idx, db_id in enumerate(db_ids)}

def buscar(query, top_k=3):
    # Gera embedding da consulta
    query_emb = model.encode([query], normalize_embeddings=True).astype('float32')
    
    # Busca no índice FAISS
    distances, indices = index.search(query_emb, top_k)
    
    resultados = []
    for faiss_idx in indices[0]:
        db_id = faiss_to_db_id.get(faiss_idx)
        if db_id is None:
            continue
        cursor.execute("SELECT texto FROM textos WHERE id = %s", (db_id,))
        row = cursor.fetchone()
        if row:
            resultados.append(row[0])
    return resultados

if __name__ == "__main__":
    consulta = input("🔍 Digite sua busca: ")
    resultados = buscar(consulta)
    print("\n🎯 Resultados mais similares:")
    for i, texto in enumerate(resultados, 1):
        print(f"{i}. {texto}")

    cursor.close()
    conn.close()

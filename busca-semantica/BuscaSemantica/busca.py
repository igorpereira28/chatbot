import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Documentos diretamente na memória
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

# Carregar modelo de embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")

# Gerar embeddings normalizados
embeddings = model.encode(documentos, normalize_embeddings=True).astype('float32')

# Criar índice FAISS
index = faiss.IndexFlatIP(embeddings.shape[1])
index.add(embeddings)

def buscar(query, top_k=3):
    query_emb = model.encode([query], normalize_embeddings=True).astype('float32')
    distances, indices = index.search(query_emb, top_k)

    resultados = []
    for idx in indices[0]:
        resultados.append(documentos[idx])
    return resultados

if __name__ == "__main__":
    while True:
        consulta = input("🔍 Digite sua busca (ou 'sair' para encerrar): ")
        if consulta.lower() == "sair":
            break
        resultados = buscar(consulta)
        print("\n🎯 Resultados mais similares:")
        for i, texto in enumerate(resultados, 1):
            print(f"{i}. {texto}")
        print()

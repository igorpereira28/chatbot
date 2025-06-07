import faiss

index = faiss.read_index("faiss.index")

print("Número de vetores no índice:", index.ntotal)
print("Dimensão dos vetores:", index.d)
print("Tipo do índice:", type(index))
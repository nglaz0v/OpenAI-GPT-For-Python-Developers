import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Задаём два вертора
A = np.array([2, 3, 5, 2, 6, 7, 9, 2, 3, 4])
B = np.array([3, 6, 3, 1, 0, 9, 2, 3, 4, 5])

# Выводим векторы на печать
print("Vector A: {}".format(A))
print("Vector B: {}".format(B))

# Вычисляем косинусное подобие
cosine = cosine_similarity([A], [B])

# Выводим результат на печать
print("Cosine Similarity: {}".format(cosine[0][0]))

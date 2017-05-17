import numpy as np


input = np.array([1, 0.5, 1])
weightMatrix = np.array([[0.73997433238661581, 0.41778693507322434, 0.34300899754418479],
                        [0.38354870601722446, 0.75787506474083055, 0.192847712986566],
                        [0.0087454565841450626, 0.98209095745444808, 0.538589353458299],
                        [0.18303558145791085, 0.20883517768645435, 0.814104061021518]])

res = np.dot(weightMatrix, input);
print(res)

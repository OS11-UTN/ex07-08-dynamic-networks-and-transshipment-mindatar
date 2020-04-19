import numpy as np
from scipy.optimize import linprog
from basic_utils import nn2na, get_usage_string, get_min_cut, get_selected_arcs

# IMPORT THE DATA:
# Primero trabajamos con la desiguldad <= notación A , siendo matrix 0 las, A_ub
# almacenes y la veentas.(demanda )

NN = np.array( [[0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])

# esta NI seria la ecuación de igualdad. Alacenamiento y demanda distintos de 0 A_eq

# DATA MANIPULATION:
#
NA, arc_idxs = nn2na(NN)

NAeq= NA.copy()
NAeq[:6, :]=0
NAub =NA.copy()
NAub[6:, :]= 0


C = np.array([100, 100, 200,200,150,150,150,150,200,200,100,100,100,150,200,200,150,100,100,150,200,200,150,100])

beq = np.array([20,30,10,40,30,10,0,0,0,0,0,0,0,0,0,0])
bub = np.array([0,0,0,0,0,0,0,0,0,0,-30,-40,-10,-20,-20,-20])
bounds = tuple([(0, None),(0, None),(0, None),(0, None),(0, None),(0, None),(0, None),(0, None),(0, None),(0, None),(0, None),(0, None),(0, None),(0, None),(0, None),(0, None),(0, None),(0, None),(0, None),(0, None),(0, None),(0, None),(0, None),(0, None)])
# Este es un vector y va por definición con [[]] como si fuese una matriz , asi lo acept Py.


# Tambien aunque es sólo un valor , va como vector.
# Parámetros de linprog.
# scipy.optimize.linprog(c, A_ub=None, b_ub=None, A_eq=None, b_eq=None, bounds=None, method=’interior-point’, callback=None, options=None, x0=None)
#
#c : es el vector de pesos o coeficientes de la funcion costo.
# A_ub: es la matriz de coeficientes para el sistema de restricciones “menos que”.
# b_u: es el vector de coeficientes libres en el sistema de ecuaciones.
# A_eq (opcional): es la matriz de coeficientes para el sistema de restricciones “igual que”.
# b_eq (opcional):es el vector de coeficientes libres en el sistema de ecuaciones de igualdad.
# bounds(opcional): lista de tuplas(min,max) para cada variable x
# method: cadena de texto del metodo a utilizar y tenemos 3 opciones
# ‘interior-point’ (en defecto)
# ‘revised simplex’ (recomendado)
# ‘simplex’ (obsoleto)
# x0: valores inciciales para inciar el proceso iterativo

# OPTIMIZE:
res = linprog(C,A_ub=NAub,b_ub=bub ,A_eq=NAeq, b_eq=beq, bounds=bounds, method='simplex' )

# GET THE SOLUTION:
selarcs = get_selected_arcs(arc_idxs,res.x )

print('## Results ## ')
print ('The row solution  will be :  ', res)

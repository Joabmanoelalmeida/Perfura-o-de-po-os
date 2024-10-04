import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

# Dados fornecidos
dados = {
    1200: 165,
    1250: 158,
    1300: 155,
    1350: 148,
    1400: 149,
    1450: 145,
    1500: 142,
    1550: 141,
    1600: 149,
    1650: 140,
    1700: 138,
    1750: 137,
    1800: 135,
    1850: 133,
    1900: 132,
    1950: 126,
    2000: 123,
    2050: 125,
    2100: 124,
    2150: 121,
    2200: 118,
    2250: 119,
    2300: 115,
    2350: 105,
    2400: 104,
    2450: 110,
    2500: 119,
    2550: 113,
    2600: 112,
    2650: 109,
    2700: 96,
    2750: 105,
    2800: 97,
    2850: 101,
    2900: 95,
    2950: 94,
    3000: 98,
    3050: 96,
    3100: 100,
    3150: 97,
}

# Ordenar as chaves (primeira coluna)
chaves = sorted(dados.keys())

# Calcular os intervalos entre valores consecutivos
intervalos = [chaves[i+1] - chaves[i] for i in range(len(chaves) - 1)]

# Contar a frequência de cada intervalo
frequencias = Counter(intervalos)

# Exibir o intervalo que se repete mais frequentemente
intervalo_mais_comum = frequencias.most_common(1)[0]

print(f"O intervalo que se repete com mais frequência é {intervalo_mais_comum[0]} metros, ocorrendo {intervalo_mais_comum[1]} vezes.")

# Parâmetros
a = 0.23
b = 0.25
Gn = 8.615  # Gradiente de referência
n = 2  

# Cálculo dos pb
pb = [a * (10**6 / deltaT)**b for deltaT in dados.values()]
pb = np.array(pb)
valores_coluna1 = list(dados.keys())
pbXdeltaD = pb*intervalo_mais_comum[0]*1.422
# Cálculo da soma acumulada de pb
pb_acumulado = np.cumsum(pbXdeltaD)
profundidades = np.array(valores_coluna1)
Gov = pb_acumulado/(0.1695*profundidades)



# Criação do gráfico para pb
plt.figure(figsize=(10, 6))
plt.plot(pb, profundidades, marker='o', label='pb')
plt.title('Relação de Gardner - Perfil de Densidade')
plt.xlabel('Densidade g/cm3', labelpad=15)
plt.ylabel('Profundidade (m)', labelpad=15)

# Configurações do eixo
plt.gca().invert_yaxis()  # Inverter o eixo Y
plt.gca().xaxis.set_ticks_position('top')  # Mover o eixo X para o topo

plt.grid()
plt.legend()
plt.show()



# Criação do gráfico para pb acumulado em função da profundidade
plt.figure(figsize=(10, 6))
plt.plot(pb_acumulado, profundidades, marker='s', color='g', label='pb acumulado')
plt.title('Pressão de sobrecarga')
plt.xlabel('Soma Acumulada de pb (g/cm3)', labelpad=15)
plt.ylabel('Profundidade (m)', labelpad=15)

# Configurações do eixo
plt.gca().invert_yaxis()  # Inverter o eixo Y

plt.grid()
plt.legend()
plt.show()

# Exibir os valores de pb acumulado
print("Valores de pb acumulado:")
for profundidade, pb_acum in zip(profundidades, pb_acumulado):
    print(f"Profundidade: {profundidade:.1f} m, pb acumulado: {pb_acum:.4f} lb/gal")



# Criação do gráfico para Gov em função da profundidade
plt.figure(figsize=(10, 6))
plt.plot(Gov, profundidades, marker='s', color='r', label='Gov')
plt.title('Gov em função da Profundidade')
plt.xlabel('Gov (N/m³)', labelpad=15)
plt.ylabel('Profundidade (m)', labelpad=15)

# Configurações do eixo
plt.gca().invert_yaxis()  # Inverter o eixo Y

plt.grid()
plt.legend()
plt.show()

# Exibir os valores de Gov
print("Valores de Gov:")
for profundidade, pb_val, gov_val in zip(profundidades, pb, Gov):
    print(f"Profundidade: {profundidade:.1f} m, pb: {pb_val:.4f} lb/gal, Gov: {gov_val:.4f} N/m³")
    



# Lista para armazenar os coeficientes angulares
coeficientes_angulares = []
deltaTn_values = []

# Calcular o coeficiente angular m para cada par consecutivo de profundidade e tempo
profundidades = sorted(dados.keys())
for i in range(len(profundidades) - 1):
    p1 = profundidades[i]
    p2 = profundidades[i + 1]
    t1 = dados[p1]
    t2 = dados[p2]
    
    # Cálculo do coeficiente angular m
    m = (np.log10(t2) - np.log10(t1)) / (p2 - p1)
    coeficientes_angulares.append((p1, p2, m))
    
     # Cálculo de deltaTn
    deltaTn = t1 * 10**(m * (p2 - p1))
    deltaTn_values.append((p1, p2, deltaTn))

# Exibir os coeficientes angulares
print("Coeficientes angulares entre as profundidades:")
for p1, p2, m in coeficientes_angulares:
    print(f"Entre {p1} m e {p2} m: m = {m:.6f}")
    
# Exibir os valores de deltaTn
print("\nValores de deltaTn entre as profundidades:")
for p1, p2, deltaTn in deltaTn_values:
    print(f"Entre {p1} m e {p2} m: deltaTn = {deltaTn:.4f}")
    

Gp_values = []
for (p1, p2, deltaTn), t1 in zip(deltaTn_values, dados.values()):
    Gp = Gov[int((p1-1200)/50)] - (Gov[int((p1-1200)/50)] - Gn) * (deltaTn / t1) ** n
    Gp_values.append((p1, p2, Gp))

# Exibir os valores de Gp
print("\nValores de Gp entre as profundidades:")
for (p1, p2, Gp) in Gp_values:
    print(f"Entre {p1} m e {p2} m: Gp = {Gp:.4f} N/m³")
    
# Preparar os dados para o gráfico
profundidades_gp = [p1 for p1, p2, Gp in Gp_values]
gp_values = [Gp for p1, p2, Gp in Gp_values]

# Criação do gráfico para Gp em função da profundidade
plt.figure(figsize=(10, 6))
plt.plot(gp_values, profundidades_gp, marker='o', color='purple', label='Gp')
plt.title('Gp em função da Profundidade')
plt.xlabel('Gp (N/m³)', labelpad=15)
plt.ylabel('Profundidade (m)', labelpad=15)

# Configurações do eixo
plt.gca().invert_yaxis()  # Inverter o eixo Y

plt.grid()
plt.legend()
plt.show()





# Criação do gráfico para Gov e Gp em função da profundidade
plt.figure(figsize=(10, 6))

# Plotando Gov
plt.plot(Gov, profundidades, marker='s', color='r', label='Gov')

# Plotando Gp
plt.plot(gp_values, profundidades_gp, marker='o', color='purple', label='Gp')

# Configurações do gráfico
plt.title('Gov e Gp em função da Profundidade')
plt.xlabel('Valores (N/m³)', labelpad=15)
plt.ylabel('Profundidade (m)', labelpad=15)
plt.gca().invert_yaxis()  # Inverter o eixo Y
plt.grid()
plt.legend()
plt.show()



# Defina o valor de K (substitua pelo valor desejado)
K = 0.5  # Exemplo de valor

# Calcular Gf usando a fórmula Gf = Gp + K * (Gov - Gp)
Gf_values = []
for (p1, p2, Gp) in Gp_values:
    Gov_at_p1 = Gov[int((p1 - 1200) / 50)]  # Obtenha o valor de Gov correspondente
    Gf = Gp + K * (Gov_at_p1 - Gp)
    Gf_values.append((p1, p2, Gf))

# Exibir os valores de Gf
print("\nValores de Gf entre as profundidades:")
for (p1, p2, Gf) in Gf_values:
    print(f"Entre {p1} m e {p2} m: Gf = {Gf:.4f} N/m³")

# Preparar os dados para o gráfico
profundidades_gf = [p1 for p1, p2, Gf in Gf_values]
gf_values = [Gf for p1, p2, Gf in Gf_values]

# Criação do gráfico para Gf em função da profundidade
plt.figure(figsize=(10, 6))
plt.plot(gf_values, profundidades_gf, marker='^', color='blue', label='Gf')
plt.title('Gf em função da Profundidade')
plt.xlabel('Gf (N/m³)', labelpad=15)
plt.ylabel('Profundidade (m)', labelpad=15)

# Configurações do eixo
plt.gca().invert_yaxis()  # Inverter o eixo Y

plt.grid()
plt.legend()
plt.show()



# Criação do gráfico para Gov, Gp e Gf em função da profundidade
plt.figure(figsize=(10, 6))

# Plotando Gov
plt.plot(Gov, profundidades, marker='s', color='r', label='Gov')

# Plotando Gp
plt.plot(gp_values, profundidades_gp, marker='o', color='purple', label='Gp')

# Plotando Gf
plt.plot(gf_values, profundidades_gf, marker='^', color='blue', label='Gf')

# Configurações do gráfico
plt.title('Gov, Gp e Gf em função da Profundidade')
plt.xlabel('Valores (N/m³)', labelpad=15)
plt.ylabel('Profundidade (m)', labelpad=15)
plt.gca().invert_yaxis()  # Inverter o eixo Y
plt.grid()
plt.legend()
plt.show()


































#letrae)
# Definindo K para o cálculo de Gf
K = 0.5  # Você pode alterar este valor conforme necessário

# Cálculo de Gf usando a fórmula Gf = Gp + K * (Gov - Gp)
Gf_values = []
for (p1, p2, Gp) in Gp_values:
    Gov_at_p1 = Gov[int((p1 - 1200) / 50)]  # Obtenha o valor de Gov correspondente
    Gf = Gp + K * (Gov_at_p1 - Gp)
    Gf_values.append((p1, p2, Gf))

# Preparar os dados para os gráficos
profundidades_gf = [p1 for p1, p2, Gf in Gf_values]
gf_values = [Gf for p1, p2, Gf in Gf_values]

# Criar o gráfico para Gov, Gp e Gf em função da profundidade
plt.figure(figsize=(10, 6))

# Plotando Gov
plt.plot(Gov, profundidades, marker='s', color='r', label='Gov')

# Plotando Gp
plt.plot(gp_values, profundidades_gp, marker='o', color='purple', label='Gp')

# Plotando Gf
plt.plot(gf_values, profundidades_gf, marker='^', color='blue', label='Gf')

# Definindo a janela operacional
for i in range(len(profundidades_gp)-1):
    plt.fill_betweenx(profundidades_gp[i:i+2], gp_values[i], gf_values[i], color='grey', alpha=0.3)

# Configurações do gráfico
plt.title('Janela Operacional: Gov, Gp e Gf em função da Profundidade')
plt.xlabel('Valores (N/m³)', labelpad=15)
plt.ylabel('Profundidade (m)', labelpad=15)
plt.gca().invert_yaxis()  # Inverter o eixo Y
plt.grid()
plt.legend()
plt.show()
import numpy as np
import matplotlib.pyplot as plt

Q = 400     # Vazão (gal/min)
D_broca = 8.5 
lâmina_de_agua = 1500  # m
taxa_penetração_media = 15  # m/h
L = 3400  # m
m_fluido = 9  # lb/gal 
m_cascalho = 2.7  # g/cm³ 
L_sapata = 2700 #m
pressao_porosa = 6200  #psi
Dp = 0.3 #in
Cr = 1.6
Q_bomba = 250 #gal/min
D_tubo_P = 4.5 #in
m_agua = 8.33 #lb/gal

dados = {
    'Rotacoes (N, rpm)': [3, 6, 100, 200, 300, 600],
    'Deflexão (teta, graus)': [2, 3, 19, 30, 40, 67]
}

def rotacao(rotacao):
    if rotacao in dados['Rotacoes (N, rpm)']:
        index = dados['Rotacoes (N, rpm)'].index(rotacao)
        return dados['Deflexão (teta, graus)'][index]
    else:
        return "Rotação não encontrada."
    
Np = 3.32 * np.log10(rotacao(600) / rotacao(300))
Kp = 1.067 * (rotacao(600) / 1022**Np)
print(f"Índice de Comportamento: {Np}, Consistência no interior da coluna: {Kp}")

Na = 0.5 * np.log10(rotacao(300) / rotacao(3))
Ka = 1.067 * (rotacao(300) / 511**Na)
print(f"Índice de Comportamento no anular: {Na}, Consistência no anular da coluna: {Ka}")

dados = [
    {'Trecho': 1, 'Comprimento': 3180, 'Di1': 4.276, 'Di2': None, 'Do': None, 'Número': None, 'ID': None},
    {'Trecho': 2, 'Comprimento': 80, 'Di1': 3, 'Di2': None, 'Do': None, 'Número': None, 'ID': None},
    {'Trecho': 3, 'Comprimento': 140, 'Di1': 2.8125, 'Di2': None, 'Do': None, 'Número': None, 'ID': None},
    {'Trecho': 4, 'Comprimento': 0, 'Di1': None, 'Di2': None, 'Do': None, 'Número': 3, 'ID': 1.5},
    {'Trecho': 5, 'Comprimento': 140, 'Di1': None, 'Di2': 6.25, 'Do': 8.5, 'Número': None, 'ID': None},
    {'Trecho': 6, 'Comprimento': 80, 'Di1': None, 'Di2': 5, 'Do': 8.5, 'Número': None, 'ID': None},
    {'Trecho': 7, 'Comprimento': 480, 'Di1': None, 'Di2': 5, 'Do': 8.5, 'Número': None, 'ID': None},
    {'Trecho': 8, 'Comprimento': 1200, 'Di1': None, 'Di2': 5, 'Do': 8.535, 'Número': None, 'ID': None},
    {'Trecho': 9, 'Comprimento': 1500, 'Di1': None, 'Di2': 5, 'Do': 19.75, 'Número': None, 'ID': None}
]

def buscar_valor(trecho, campo):
    for dado in dados:
        if dado['Trecho'] == trecho:
            return dado.get(campo, "Campo não encontrado.")
    return "Trecho não encontrado."

velocidade1_3 = {}
for i in range(1, 4):
    di = buscar_valor(i, 'Di1') 
    if di is not None and di != 0:  
        resultado = 24.51 * Q / (di ** 2)
        velocidade1_3[i] = resultado
    else:
        velocidade1_3[i] = "Di1 não disponível ou igual a zero."

for trecho, velocidade in velocidade1_3.items():
    print(f"Velocidade média para o trecho {trecho}: {velocidade}")

id_trecho_4 = buscar_valor(4, 'ID')   
if id_trecho_4 is not None and id_trecho_4 != 0:  
    velocidade_trecho_4 = 24.51 * Q / (id_trecho_4 ** 2) 
else:
    velocidade_trecho_4 = "Di1 não disponível ou igual a zero."
print(f"Velocidade média para o trecho 4 (usando ID): {velocidade_trecho_4}")

velocidade5_9 = {}
for i in range(5, 10):
    do = buscar_valor(i, 'Do') 
    di = buscar_valor(i, 'Di2') 
    if do is not None and di is not None and (do**2 - di**2) != 0:  
        resultado = 24.51 * Q / (do**2 - di**2)
        velocidade5_9[i] = resultado
    else:
        velocidade5_9[i] = "Do ou Di não disponível ou cálculo inválido."

for trecho, velocidade in velocidade5_9.items():
    print(f"Velocidade média para o trecho {trecho}: {velocidade}")
    
velocidade_critica1_3 = {}
for i in range(1, 4):
    di1 = buscar_valor(i, 'Di1')
    if di1 is not None and di1 != 0:  
        velocidade_critica = (
            1.969 * 
            ((5 * (3470 - 1370 * Np) * Kp) / m_fluido) ** (1 / (2 * Np)) *
            ((3 * Np + 1) / (1.27 * di1 * Np)) ** (Np / (2 - Np)))
        velocidade_critica1_3[i] = velocidade_critica
    else:
        velocidade_critica1_3[i] = "Di1 não disponível ou igual a zero."

for trecho, velocidades_critica in velocidade_critica1_3.items():
    print(f"Velocidade crítica para o trecho {trecho}: {velocidades_critica}")
    
velocidade_critica5_9 = {}
for i in range(5, 10):
    do = buscar_valor(i, 'Do')
    di = buscar_valor(i, 'Di2')
    
    if do is not None and di is not None and (do - di) != 0:  
        velocidade_critica = (
            1.969 * 
            (((4.08 * (3470 - 1370 * Na) * Ka) / m_fluido) ** (1 / (2 - Na))) *
            (((2 * Na + 1) / (0.64 * (do - di) * Na)) ** (Na / (2 - Na)))
        )
        velocidade_critica5_9[i] = velocidade_critica
    else:
        velocidade_critica5_9[i] = "Do ou Di não disponível ou cálculo inválido."

for trecho, velocidades_critica in velocidade_critica5_9.items():
    print(f"Velocidade crítica para o trecho {trecho}: {velocidades_critica}")
    
for i in range(1, 10):
    if i in velocidade1_3:
        velocidade_media = velocidade1_3[i]
    elif i in velocidade5_9:
        velocidade_media = velocidade5_9[i]
    else:
        velocidade_media = "Não disponível"
    
    if i in velocidade_critica1_3:
        velocidade_critica = velocidade_critica1_3[i] if i <= 3 else None
    elif i in velocidade_critica5_9:
        velocidade_critica = velocidade_critica5_9[i] if i >= 5 else None
    else:
        velocidade_critica = "Não disponível"

    # Comparar velocidades
    if isinstance(velocidade_media, (int, float)) and isinstance(velocidade_critica, (int, float)):
        if velocidade_media < velocidade_critica:
            estado = "Laminar"
        else:
            estado = "Turbulento"
    else:
        estado = "Turbulento para Broca ou Dados insuficientes para comparação"

    print(f"Trecho {i}: Velocidade média = {velocidade_media}, Velocidade crítica = {velocidade_critica}, Estado: {estado}")
    

deltaP_trechos_1_3 = {}
for i in range(1, 4):
    if i in velocidade1_3:
        velocidade_media = velocidade1_3[i]
    elif i in velocidade5_9:
        velocidade_media = velocidade5_9[i]
    else:
        velocidade_media = None

    if i <= 3:
        di1_value = buscar_valor(i, 'Di1')
        comprimento = buscar_valor(i, 'Comprimento')
        if di1_value is not None and di1_value != 0 and velocidade_media is not None:
            deltaP = (
                (((np.log10(Np) + 2.5) * m_fluido * (velocidade_media ** 2) * comprimento) /  #8.45 água 
                (4645029 * di1_value)) *
                ((19.36 * Kp * ((0.4 * velocidade_media * (3 * Np + 1) / (di1_value * Np)) /
                (8.45 * velocidade_media ** 2)) ** ((1.4 - np.log10(Np)) / 7)))
            )
            deltaP_trechos_1_3[i] = deltaP
        else:
            deltaP_trechos_1_3[i] = "Dados insuficientes para cálculo."
    else:
        deltaP_trechos_1_3[i] = "Não aplicável para este trecho."
for trecho, deltaP in deltaP_trechos_1_3.items():
    print(f"Delta P para o trecho {trecho}: {deltaP}")

trecho_4_deltaP = {}
i = 4  # Trecho 4
ID_value = buscar_valor(i, 'ID')

if ID_value is not None and ID_value != 0:
    deltaP_trecho_4 = (156 * m_fluido * Q ** 2) / (((24/ID_value) ** 2)*3) ** 2
    trecho_4_deltaP[i] = deltaP_trecho_4
else:
    trecho_4_deltaP[i] = "ID não disponível ou igual a zero."

for trecho, deltaP in trecho_4_deltaP.items():
    print(f"Delta P para o trecho {trecho}: {deltaP}")
    
deltaP_trechos_5_9 = {}
for i in range(5, 10):
    do = buscar_valor(i, 'Do')
    di2 = buscar_valor(i, 'Di2')
    comprimento = buscar_valor(i, 'Comprimento')
    velocidade_media = velocidade5_9[i] if i in velocidade5_9 else 0 

    if do is not None and di2 is not None and comprimento is not None and (do - di2) != 0:
        deltaP = (
            (Ka * comprimento / (300 * (do - di2))) *
            ((0.8 * velocidade_media * (2 * Na + 1)) / ((do - di2) * Na) ** Na)
        )
        deltaP_trechos_5_9[i] = deltaP
    else:
        deltaP_trechos_5_9[i] = "Do, Di2 ou comprimento não disponível ou cálculo inválido."

for trecho, deltaP in deltaP_trechos_5_9.items():
    print(f"Delta P para o trecho {trecho}: {deltaP}")
    
soma_total_deltaP = 0
for deltaP in deltaP_trechos_1_3.values():
    if isinstance(deltaP, (int, float)):
        soma_total_deltaP += deltaP

for deltaP in trecho_4_deltaP.values():
    if isinstance(deltaP, (int, float)):
        soma_total_deltaP += deltaP

for deltaP in deltaP_trechos_5_9.values():
    if isinstance(deltaP, (int, float)):
        soma_total_deltaP += deltaP
print(f"Soma total de Delta P: {soma_total_deltaP}")


Q_cascalho = 0.7*taxa_penetração_media*D_broca**2/314
Q_anular = Q_cascalho + Q
print(Q_anular)

m_anular = (Q*m_fluido+Q_cascalho*8.34*m_cascalho)/Q_anular
print(f"O peso específico no anular: {m_anular}")

delta_P_hidrostatico = 0.17*(m_anular-m_fluido)*L
print(f"O Delta P hidrostático: {delta_P_hidrostatico}")

P_bengala = soma_total_deltaP + delta_P_hidrostatico
print(f"A pressão no tubo de bengala vale: {P_bengala}")


soma_total_deltaP_anular = 0
for deltaP in deltaP_trechos_5_9.values():
    if isinstance(deltaP, (int, float)):
        soma_total_deltaP_anular += deltaP
        
P_dinamica_no_fundo = 0.17*m_anular*L + soma_total_deltaP_anular
print(f"A pressão dinâmica no fundo do poço: {P_dinamica_no_fundo}")


Ecd_fundo = P_dinamica_no_fundo/(0.17*L)
print(f"ECD no fundo do poço: {Ecd_fundo}")


soma_total_deltaP_sapata = 0
for trecho, deltaP in deltaP_trechos_5_9.items():
    if trecho in [8, 9] and isinstance(deltaP, (int, float)):
        soma_total_deltaP_sapata += deltaP
P_dinamica_na_sapata = 0.17*m_anular*L_sapata + soma_total_deltaP_sapata
print(f"A pressão dinâmica na sapata: {P_dinamica_na_sapata}")

Ecd_sapata = P_dinamica_na_sapata/(0.17*L_sapata)
print(f"ECD no fundo na sapata: {Ecd_sapata}")



Vs = 113.4*np.sqrt(Dp*(m_cascalho* 8.34 - m_agua)/(Cr*m_agua))
print(f"A velocidade e eficiência de remoção dos sólidos com os dados de poço: {Vs} ft/min")

V_media = 24.51*Q_bomba/(D_broca**2 - D_tubo_P**2)
print(f"A velocidade média do fluxo no anular: {V_media} ft/min")

Vr = V_media - Vs
print(f"A velocidade de remoção dos sólidos: {Vr} ft/min")

ER = 100*Vr/V_media
print(f"A eficiência de remoção será: {ER}%")



peso_especifico_minimo = pressao_porosa / L*3.28084   #3.28084 m to pés
print(f"Peso específico mínimo do fluido de perfuração: {peso_especifico_minimo:.2f} psi")








# Listas para armazenar Q e ECD
valores_Q = []
valores_ECD_fundo = []
valores_ECD_sapata = []
for Q in range(200, 801, 100):
    print(f"\nCálculos para Q = {Q} gal/min\n")
    
    velocidade1_3 = {}
    for i in range(1, 4):
        di = buscar_valor(i, 'Di1') 
        if di is not None and di != 0:  
            resultado = 24.51 * Q / (di ** 2)
            velocidade1_3[i] = resultado
        else:
            velocidade1_3[i] = "Di1 não disponível ou igual a zero."

    for trecho, velocidade in velocidade1_3.items():
        print(f"Velocidade média para o trecho {trecho}: {velocidade}")

    id_trecho_4 = buscar_valor(4, 'ID')   
    if id_trecho_4 is not None and id_trecho_4 != 0:  
        velocidade_trecho_4 = 24.51 * Q / (id_trecho_4 ** 2) 
    else:
        velocidade_trecho_4 = "Di1 não disponível ou igual a zero."
    print(f"Velocidade média para o trecho 4 (usando ID): {velocidade_trecho_4}")

    velocidade5_9 = {}
    for i in range(5, 10):
        do = buscar_valor(i, 'Do') 
        di = buscar_valor(i, 'Di2') 
        if do is not None and di is not None and (do**2 - di**2) != 0:  
            resultado = 24.51 * Q / (do**2 - di**2)
            velocidade5_9[i] = resultado
        else:
            velocidade5_9[i] = "Do ou Di não disponível ou cálculo inválido."

    for trecho, velocidade in velocidade5_9.items():
        print(f"Velocidade média para o trecho {trecho}: {velocidade}")
        
    velocidade_critica1_3 = {}
    for i in range(1, 4):
        di1 = buscar_valor(i, 'Di1')
        if di1 is not None and di1 != 0:  
            velocidade_critica = (
                1.969 * 
                ((5 * (3470 - 1370 * Np) * Kp) / m_fluido) ** (1 / (2 * Np)) *
                ((3 * Np + 1) / (1.27 * di1 * Np)) ** (Np / (2 - Np)))
            velocidade_critica1_3[i] = velocidade_critica
        else:
            velocidade_critica1_3[i] = "Di1 não disponível ou igual a zero."

    for trecho, velocidades_critica in velocidade_critica1_3.items():
        print(f"Velocidade crítica para o trecho {trecho}: {velocidades_critica}")
        
    velocidade_critica5_9 = {}
    for i in range(5, 10):
        do = buscar_valor(i, 'Do')
        di = buscar_valor(i, 'Di2')
        
        if do is not None and di is not None and (do - di) != 0:  
            velocidade_critica = (
                1.969 * 
                (((4.08 * (3470 - 1370 * Na) * Ka) / m_fluido) ** (1 / (2 - Na))) *
                (((2 * Na + 1) / (0.64 * (do - di) * Na)) ** (Na / (2 - Na)))
            )
            velocidade_critica5_9[i] = velocidade_critica
        else:
            velocidade_critica5_9[i] = "Do ou Di não disponível ou cálculo inválido."

    for trecho, velocidades_critica in velocidade_critica5_9.items():
        print(f"Velocidade crítica para o trecho {trecho}: {velocidades_critica}")
        
    for i in range(1, 10):
        if i in velocidade1_3:
            velocidade_media = velocidade1_3[i]
        elif i in velocidade5_9:
            velocidade_media = velocidade5_9[i]
        else:
            velocidade_media = "Não disponível"
        
        if i in velocidade_critica1_3:
            velocidade_critica = velocidade_critica1_3[i] if i <= 3 else None
        elif i in velocidade_critica5_9:
            velocidade_critica = velocidade_critica5_9[i] if i >= 5 else None
        else:
            velocidade_critica = "Não disponível"

        # Comparar velocidades
        if isinstance(velocidade_media, (int, float)) and isinstance(velocidade_critica, (int, float)):
            if velocidade_media < velocidade_critica:
                estado = "Laminar"
            else:
                estado = "Turbulento"
        else:
            estado = "Turbulento para Broca ou Dados insuficientes para comparação"

        print(f"Trecho {i}: Velocidade média = {velocidade_media}, Velocidade crítica = {velocidade_critica}, Estado: {estado}")
        

    deltaP_trechos_1_3 = {}
    for i in range(1, 4):
        if i in velocidade1_3:
            velocidade_media = velocidade1_3[i]
        elif i in velocidade5_9:
            velocidade_media = velocidade5_9[i]
        else:
            velocidade_media = None

        if i <= 3:
            di1_value = buscar_valor(i, 'Di1')
            comprimento = buscar_valor(i, 'Comprimento')
            if di1_value is not None and di1_value != 0 and velocidade_media is not None:
                deltaP = (
                    (((np.log10(Np) + 2.5) * m_fluido * (velocidade_media ** 2) * comprimento) /  #8.45 água 
                    (4645029 * di1_value)) *
                    ((19.36 * Kp * ((0.4 * velocidade_media * (3 * Np + 1) / (di1_value * Np)) /
                    (8.45 * velocidade_media ** 2)) ** ((1.4 - np.log10(Np)) / 7)))
                )
                deltaP_trechos_1_3[i] = deltaP
            else:
                deltaP_trechos_1_3[i] = "Dados insuficientes para cálculo."
        else:
            deltaP_trechos_1_3[i] = "Não aplicável para este trecho."
    for trecho, deltaP in deltaP_trechos_1_3.items():
        print(f"Delta P para o trecho {trecho}: {deltaP}")

    trecho_4_deltaP = {}
    i = 4  # Trecho 4
    ID_value = buscar_valor(i, 'ID')

    if ID_value is not None and ID_value != 0:
        deltaP_trecho_4 = (156 * m_fluido * Q ** 2) / (((24/ID_value) ** 2)*3) ** 2
        trecho_4_deltaP[i] = deltaP_trecho_4
    else:
        trecho_4_deltaP[i] = "ID não disponível ou igual a zero."

    for trecho, deltaP in trecho_4_deltaP.items():
        print(f"Delta P para o trecho {trecho}: {deltaP}")
        
    deltaP_trechos_5_9 = {}
    for i in range(5, 10):
        do = buscar_valor(i, 'Do')
        di2 = buscar_valor(i, 'Di2')
        comprimento = buscar_valor(i, 'Comprimento')
        velocidade_media = velocidade5_9[i] if i in velocidade5_9 else 0 

        if do is not None and di2 is not None and comprimento is not None and (do - di2) != 0:
            deltaP = (
                (Ka * comprimento / (300 * (do - di2))) *
                ((0.8 * velocidade_media * (2 * Na + 1)) / ((do - di2) * Na) ** Na)
            )
            deltaP_trechos_5_9[i] = deltaP
        else:
            deltaP_trechos_5_9[i] = "Do, Di2 ou comprimento não disponível ou cálculo inválido."

    for trecho, deltaP in deltaP_trechos_5_9.items():
        print(f"Delta P para o trecho {trecho}: {deltaP}")
        
    soma_total_deltaP = 0
    for deltaP in deltaP_trechos_1_3.values():
        if isinstance(deltaP, (int, float)):
            soma_total_deltaP += deltaP

    for deltaP in trecho_4_deltaP.values():
        if isinstance(deltaP, (int, float)):
            soma_total_deltaP += deltaP

    for deltaP in deltaP_trechos_5_9.values():
        if isinstance(deltaP, (int, float)):
            soma_total_deltaP += deltaP
    print(f"Soma total de Delta P: {soma_total_deltaP}")


    Q_cascalho = 0.7*taxa_penetração_media*D_broca**2/314
    Q_anular = Q_cascalho + Q
    print(Q_anular)

    m_anular = (Q*m_fluido+Q_cascalho*8.34*m_cascalho)/Q_anular
    print(f"O peso específico no anular: {m_anular}")

    delta_P_hidrostatico = 0.17*(m_anular-m_fluido)*L
    print(f"O Delta P hidrostático: {delta_P_hidrostatico}")

    P_bengala = soma_total_deltaP + delta_P_hidrostatico
    print(f"A pressão no tubo de bengala vale: {P_bengala}")


    soma_total_deltaP_anular = 0
    for deltaP in deltaP_trechos_5_9.values():
        if isinstance(deltaP, (int, float)):
            soma_total_deltaP_anular += deltaP
            
    P_dinamica_no_fundo = 0.17*m_anular*L + soma_total_deltaP_anular
    print(f"A pressão dinâmica no fundo do poço: {P_dinamica_no_fundo}")


    Ecd_fundo = P_dinamica_no_fundo/(0.17*L)
    print(f"ECD no fundo do poço: {Ecd_fundo}")


    soma_total_deltaP_sapata = 0
    for trecho, deltaP in deltaP_trechos_5_9.items():
        if trecho in [8, 9] and isinstance(deltaP, (int, float)):
            soma_total_deltaP_sapata += deltaP
    P_dinamica_na_sapata = 0.17*m_anular*L_sapata + soma_total_deltaP_sapata
    print(f"A pressão dinâmica na sapata: {P_dinamica_na_sapata}")

    Ecd_sapata = P_dinamica_na_sapata/(0.17*L_sapata)
    print(f"ECD no fundo na sapata: {Ecd_sapata}")



    Vs = 113.4*np.sqrt(Dp*(m_cascalho* 8.34 - m_agua)/(Cr*m_agua))
    print(f"A velocidade e eficiência de remoção dos sólidos com os dados de poço: {Vs} ft/min")

    V_media = 24.51*Q_bomba/(D_broca**2 - D_tubo_P**2)
    print(f"A velocidade média do fluxo no anular: {V_media} ft/min")

    Vr = V_media - Vs
    print(f"A velocidade de remoção dos sólidos: {Vr} ft/min")

    ER = 100*Vr/V_media
    print(f"A eficiência de remoção será: {ER}%")



    peso_especifico_minimo = pressao_porosa / L*3.28084   #3.28084 m to pés
    print(f"Peso específico mínimo do fluido de perfuração: {peso_especifico_minimo:.2f} psi")
    
    # Adicione o valor de Q e ECD calculado para o fundo
    valores_Q.append(Q)
    valores_ECD_fundo.append(Ecd_fundo)

    # Adicione o valor de Q e ECD calculado para a sapata
    valores_ECD_sapata.append(Ecd_sapata)
    
# Após todos os cálculos, plote os ECDs
plt.figure(figsize=(10, 6))
plt.plot(valores_Q, valores_ECD_fundo, marker='o', label='ECD no fundo do poço')
plt.plot(valores_Q, valores_ECD_sapata, marker='x', label='ECD na sapata')
plt.title('ECD em função de Q')
plt.xlabel('Fluxo (Q) [gal/min]')
plt.ylabel('ECD [ppg]')
plt.grid()
plt.legend()
plt.show()













valores_m_fluido = []
valores_ECD_fundo = []
valores_ECD_sapata = []
for m_fluido in range(8, 15, 1):
    print(f"\nCálculos para m_fluido = {m_fluido} gal/min\n")
    
    velocidade1_3 = {}
    for i in range(1, 4):
        di = buscar_valor(i, 'Di1') 
        if di is not None and di != 0:  
            resultado = 24.51 * Q / (di ** 2)
            velocidade1_3[i] = resultado
        else:
            velocidade1_3[i] = "Di1 não disponível ou igual a zero."

    for trecho, velocidade in velocidade1_3.items():
        print(f"Velocidade média para o trecho {trecho}: {velocidade}")

    id_trecho_4 = buscar_valor(4, 'ID')   
    if id_trecho_4 is not None and id_trecho_4 != 0:  
        velocidade_trecho_4 = 24.51 * Q / (id_trecho_4 ** 2) 
    else:
        velocidade_trecho_4 = "Di1 não disponível ou igual a zero."
    print(f"Velocidade média para o trecho 4 (usando ID): {velocidade_trecho_4}")

    velocidade5_9 = {}
    for i in range(5, 10):
        do = buscar_valor(i, 'Do') 
        di = buscar_valor(i, 'Di2') 
        if do is not None and di is not None and (do**2 - di**2) != 0:  
            resultado = 24.51 * Q / (do**2 - di**2)
            velocidade5_9[i] = resultado
        else:
            velocidade5_9[i] = "Do ou Di não disponível ou cálculo inválido."

    for trecho, velocidade in velocidade5_9.items():
        print(f"Velocidade média para o trecho {trecho}: {velocidade}")
        
    velocidade_critica1_3 = {}
    for i in range(1, 4):
        di1 = buscar_valor(i, 'Di1')
        if di1 is not None and di1 != 0:  
            velocidade_critica = (
                1.969 * 
                ((5 * (3470 - 1370 * Np) * Kp) / m_fluido) ** (1 / (2 * Np)) *
                ((3 * Np + 1) / (1.27 * di1 * Np)) ** (Np / (2 - Np)))
            velocidade_critica1_3[i] = velocidade_critica
        else:
            velocidade_critica1_3[i] = "Di1 não disponível ou igual a zero."

    for trecho, velocidades_critica in velocidade_critica1_3.items():
        print(f"Velocidade crítica para o trecho {trecho}: {velocidades_critica}")
        
    velocidade_critica5_9 = {}
    for i in range(5, 10):
        do = buscar_valor(i, 'Do')
        di = buscar_valor(i, 'Di2')
        
        if do is not None and di is not None and (do - di) != 0:  
            velocidade_critica = (
                1.969 * 
                (((4.08 * (3470 - 1370 * Na) * Ka) / m_fluido) ** (1 / (2 - Na))) *
                (((2 * Na + 1) / (0.64 * (do - di) * Na)) ** (Na / (2 - Na)))
            )
            velocidade_critica5_9[i] = velocidade_critica
        else:
            velocidade_critica5_9[i] = "Do ou Di não disponível ou cálculo inválido."

    for trecho, velocidades_critica in velocidade_critica5_9.items():
        print(f"Velocidade crítica para o trecho {trecho}: {velocidades_critica}")
        
    for i in range(1, 10):
        if i in velocidade1_3:
            velocidade_media = velocidade1_3[i]
        elif i in velocidade5_9:
            velocidade_media = velocidade5_9[i]
        else:
            velocidade_media = "Não disponível"
        
        if i in velocidade_critica1_3:
            velocidade_critica = velocidade_critica1_3[i] if i <= 3 else None
        elif i in velocidade_critica5_9:
            velocidade_critica = velocidade_critica5_9[i] if i >= 5 else None
        else:
            velocidade_critica = "Não disponível"

        # Comparar velocidades
        if isinstance(velocidade_media, (int, float)) and isinstance(velocidade_critica, (int, float)):
            if velocidade_media < velocidade_critica:
                estado = "Laminar"
            else:
                estado = "Turbulento"
        else:
            estado = "Turbulento para Broca ou Dados insuficientes para comparação"

        print(f"Trecho {i}: Velocidade média = {velocidade_media}, Velocidade crítica = {velocidade_critica}, Estado: {estado}")
        

    deltaP_trechos_1_3 = {}
    for i in range(1, 4):
        if i in velocidade1_3:
            velocidade_media = velocidade1_3[i]
        elif i in velocidade5_9:
            velocidade_media = velocidade5_9[i]
        else:
            velocidade_media = None

        if i <= 3:
            di1_value = buscar_valor(i, 'Di1')
            comprimento = buscar_valor(i, 'Comprimento')
            if di1_value is not None and di1_value != 0 and velocidade_media is not None:
                deltaP = (
                    (((np.log10(Np) + 2.5) * m_fluido * (velocidade_media ** 2) * comprimento) /  #8.45 água 
                    (4645029 * di1_value)) *
                    ((19.36 * Kp * ((0.4 * velocidade_media * (3 * Np + 1) / (di1_value * Np)) /
                    (8.45 * velocidade_media ** 2)) ** ((1.4 - np.log10(Np)) / 7)))
                )
                deltaP_trechos_1_3[i] = deltaP
            else:
                deltaP_trechos_1_3[i] = "Dados insuficientes para cálculo."
        else:
            deltaP_trechos_1_3[i] = "Não aplicável para este trecho."
    for trecho, deltaP in deltaP_trechos_1_3.items():
        print(f"Delta P para o trecho {trecho}: {deltaP}")

    trecho_4_deltaP = {}
    i = 4  # Trecho 4
    ID_value = buscar_valor(i, 'ID')

    if ID_value is not None and ID_value != 0:
        deltaP_trecho_4 = (156 * m_fluido * Q ** 2) / (((24/ID_value) ** 2)*3) ** 2
        trecho_4_deltaP[i] = deltaP_trecho_4
    else:
        trecho_4_deltaP[i] = "ID não disponível ou igual a zero."

    for trecho, deltaP in trecho_4_deltaP.items():
        print(f"Delta P para o trecho {trecho}: {deltaP}")
        
    deltaP_trechos_5_9 = {}
    for i in range(5, 10):
        do = buscar_valor(i, 'Do')
        di2 = buscar_valor(i, 'Di2')
        comprimento = buscar_valor(i, 'Comprimento')
        velocidade_media = velocidade5_9[i] if i in velocidade5_9 else 0 

        if do is not None and di2 is not None and comprimento is not None and (do - di2) != 0:
            deltaP = (
                (Ka * comprimento / (300 * (do - di2))) *
                ((0.8 * velocidade_media * (2 * Na + 1)) / ((do - di2) * Na) ** Na)
            )
            deltaP_trechos_5_9[i] = deltaP
        else:
            deltaP_trechos_5_9[i] = "Do, Di2 ou comprimento não disponível ou cálculo inválido."

    for trecho, deltaP in deltaP_trechos_5_9.items():
        print(f"Delta P para o trecho {trecho}: {deltaP}")
        
    soma_total_deltaP = 0
    for deltaP in deltaP_trechos_1_3.values():
        if isinstance(deltaP, (int, float)):
            soma_total_deltaP += deltaP

    for deltaP in trecho_4_deltaP.values():
        if isinstance(deltaP, (int, float)):
            soma_total_deltaP += deltaP

    for deltaP in deltaP_trechos_5_9.values():
        if isinstance(deltaP, (int, float)):
            soma_total_deltaP += deltaP
    print(f"Soma total de Delta P: {soma_total_deltaP}")


    Q_cascalho = 0.7*taxa_penetração_media*D_broca**2/314
    Q_anular = Q_cascalho + Q
    print(Q_anular)

    m_anular = (Q*m_fluido+Q_cascalho*8.34*m_cascalho)/Q_anular
    print(f"O peso específico no anular: {m_anular}")

    delta_P_hidrostatico = 0.17*(m_anular-m_fluido)*L
    print(f"O Delta P hidrostático: {delta_P_hidrostatico}")

    P_bengala = soma_total_deltaP + delta_P_hidrostatico
    print(f"A pressão no tubo de bengala vale: {P_bengala}")


    soma_total_deltaP_anular = 0
    for deltaP in deltaP_trechos_5_9.values():
        if isinstance(deltaP, (int, float)):
            soma_total_deltaP_anular += deltaP
            
    P_dinamica_no_fundo = 0.17*m_anular*L + soma_total_deltaP_anular
    print(f"A pressão dinâmica no fundo do poço: {P_dinamica_no_fundo}")


    Ecd_fundo = P_dinamica_no_fundo/(0.17*L)
    print(f"ECD no fundo do poço: {Ecd_fundo}")


    soma_total_deltaP_sapata = 0
    for trecho, deltaP in deltaP_trechos_5_9.items():
        if trecho in [8, 9] and isinstance(deltaP, (int, float)):
            soma_total_deltaP_sapata += deltaP
    P_dinamica_na_sapata = 0.17*m_anular*L_sapata + soma_total_deltaP_sapata
    print(f"A pressão dinâmica na sapata: {P_dinamica_na_sapata}")

    Ecd_sapata = P_dinamica_na_sapata/(0.17*L_sapata)
    print(f"ECD no fundo na sapata: {Ecd_sapata}")



    Vs = 113.4*np.sqrt(Dp*(m_cascalho* 8.34 - m_agua)/(Cr*m_agua))
    print(f"A velocidade e eficiência de remoção dos sólidos com os dados de poço: {Vs} ft/min")

    V_media = 24.51*Q_bomba/(D_broca**2 - D_tubo_P**2)
    print(f"A velocidade média do fluxo no anular: {V_media} ft/min")

    Vr = V_media - Vs
    print(f"A velocidade de remoção dos sólidos: {Vr} ft/min")

    ER = 100*Vr/V_media
    print(f"A eficiência de remoção será: {ER}%")



    peso_especifico_minimo = pressao_porosa / L*3.28084   #3.28084 m to pés
    print(f"Peso específico mínimo do fluido de perfuração: {peso_especifico_minimo:.2f} psi")
    
    # Adicione o valor de Q e ECD calculado para o fundo
    valores_Q.append(Q)
    valores_ECD_fundo.append(Ecd_fundo)

    # Adicione o valor de Q e ECD calculado para a sapata
    valores_ECD_sapata.append(Ecd_sapata)
    
    m_fluido_values = list(range(8, 15))
    
    # Plotando os gráficos
plt.figure(figsize=(12, 6))

# Gráfico para ECD no fundo
plt.subplot(1, 2, 1)
plt.plot(m_fluido_values, valores_ECD_fundo, marker='o', color='b', label='ECD Fundo')
plt.title('ECD no Fundo vs m_fluido')
plt.xlabel('m_fluido (kg/m³)')
plt.ylabel('ECD (psi)')
plt.xticks(m_fluido_values)
plt.grid()
plt.legend()

# Gráfico para ECD na sapata
plt.subplot(1, 2, 2)
plt.plot(m_fluido_values, valores_ECD_sapata, marker='o', color='r', label='ECD Sapata')
plt.title('ECD na Sapata vs m_fluido')
plt.xlabel('m_fluido (kg/m³)')
plt.ylabel('ECD (psi)')
plt.xticks(m_fluido_values)
plt.grid()
plt.legend()
plt.show()






'''valores_taxa_penetração_media = []
valores_ECD_fundo = []
valores_ECD_sapata = []
for taxa_penetração_media in range(10, 41, 10):
    print(f"\nCálculos para taxa_penetração_media = {taxa_penetração_media} gal/min\n")
    
    velocidade1_3 = {}
    for i in range(1, 4):
        di = buscar_valor(i, 'Di1') 
        if di is not None and di != 0:  
            resultado = 24.51 * Q / (di ** 2)
            velocidade1_3[i] = resultado
        else:
            velocidade1_3[i] = "Di1 não disponível ou igual a zero."

    for trecho, velocidade in velocidade1_3.items():
        print(f"Velocidade média para o trecho {trecho}: {velocidade}")

    id_trecho_4 = buscar_valor(4, 'ID')   
    if id_trecho_4 is not None and id_trecho_4 != 0:  
        velocidade_trecho_4 = 24.51 * Q / (id_trecho_4 ** 2) 
    else:
        velocidade_trecho_4 = "Di1 não disponível ou igual a zero."
    print(f"Velocidade média para o trecho 4 (usando ID): {velocidade_trecho_4}")

    velocidade5_9 = {}
    for i in range(5, 10):
        do = buscar_valor(i, 'Do') 
        di = buscar_valor(i, 'Di2') 
        if do is not None and di is not None and (do**2 - di**2) != 0:  
            resultado = 24.51 * Q / (do**2 - di**2)
            velocidade5_9[i] = resultado
        else:
            velocidade5_9[i] = "Do ou Di não disponível ou cálculo inválido."

    for trecho, velocidade in velocidade5_9.items():
        print(f"Velocidade média para o trecho {trecho}: {velocidade}")
        
    velocidade_critica1_3 = {}
    for i in range(1, 4):
        di1 = buscar_valor(i, 'Di1')
        if di1 is not None and di1 != 0:  
            velocidade_critica = (
                1.969 * 
                ((5 * (3470 - 1370 * Np) * Kp) / m_fluido) ** (1 / (2 * Np)) *
                ((3 * Np + 1) / (1.27 * di1 * Np)) ** (Np / (2 - Np)))
            velocidade_critica1_3[i] = velocidade_critica
        else:
            velocidade_critica1_3[i] = "Di1 não disponível ou igual a zero."

    for trecho, velocidades_critica in velocidade_critica1_3.items():
        print(f"Velocidade crítica para o trecho {trecho}: {velocidades_critica}")
        
    velocidade_critica5_9 = {}
    for i in range(5, 10):
        do = buscar_valor(i, 'Do')
        di = buscar_valor(i, 'Di2')
        
        if do is not None and di is not None and (do - di) != 0:  
            velocidade_critica = (
                1.969 * 
                (((4.08 * (3470 - 1370 * Na) * Ka) / m_fluido) ** (1 / (2 - Na))) *
                (((2 * Na + 1) / (0.64 * (do - di) * Na)) ** (Na / (2 - Na)))
            )
            velocidade_critica5_9[i] = velocidade_critica
        else:
            velocidade_critica5_9[i] = "Do ou Di não disponível ou cálculo inválido."

    for trecho, velocidades_critica in velocidade_critica5_9.items():
        print(f"Velocidade crítica para o trecho {trecho}: {velocidades_critica}")
        
    for i in range(1, 10):
        if i in velocidade1_3:
            velocidade_media = velocidade1_3[i]
        elif i in velocidade5_9:
            velocidade_media = velocidade5_9[i]
        else:
            velocidade_media = "Não disponível"
        
        if i in velocidade_critica1_3:
            velocidade_critica = velocidade_critica1_3[i] if i <= 3 else None
        elif i in velocidade_critica5_9:
            velocidade_critica = velocidade_critica5_9[i] if i >= 5 else None
        else:
            velocidade_critica = "Não disponível"

        # Comparar velocidades
        if isinstance(velocidade_media, (int, float)) and isinstance(velocidade_critica, (int, float)):
            if velocidade_media < velocidade_critica:
                estado = "Laminar"
            else:
                estado = "Turbulento"
        else:
            estado = "Turbulento para Broca ou Dados insuficientes para comparação"

        print(f"Trecho {i}: Velocidade média = {velocidade_media}, Velocidade crítica = {velocidade_critica}, Estado: {estado}")
        

    deltaP_trechos_1_3 = {}
    for i in range(1, 4):
        if i in velocidade1_3:
            velocidade_media = velocidade1_3[i]
        elif i in velocidade5_9:
            velocidade_media = velocidade5_9[i]
        else:
            velocidade_media = None

        if i <= 3:
            di1_value = buscar_valor(i, 'Di1')
            comprimento = buscar_valor(i, 'Comprimento')
            if di1_value is not None and di1_value != 0 and velocidade_media is not None:
                deltaP = (
                    (((np.log10(Np) + 2.5) * m_fluido * (velocidade_media ** 2) * comprimento) /  #8.45 água 
                    (4645029 * di1_value)) *
                    ((19.36 * Kp * ((0.4 * velocidade_media * (3 * Np + 1) / (di1_value * Np)) /
                    (8.45 * velocidade_media ** 2)) ** ((1.4 - np.log10(Np)) / 7)))
                )
                deltaP_trechos_1_3[i] = deltaP
            else:
                deltaP_trechos_1_3[i] = "Dados insuficientes para cálculo."
        else:
            deltaP_trechos_1_3[i] = "Não aplicável para este trecho."
    for trecho, deltaP in deltaP_trechos_1_3.items():
        print(f"Delta P para o trecho {trecho}: {deltaP}")

    trecho_4_deltaP = {}
    i = 4  # Trecho 4
    ID_value = buscar_valor(i, 'ID')

    if ID_value is not None and ID_value != 0:
        deltaP_trecho_4 = (156 * m_fluido * Q ** 2) / (((24/ID_value) ** 2)*3) ** 2
        trecho_4_deltaP[i] = deltaP_trecho_4
    else:
        trecho_4_deltaP[i] = "ID não disponível ou igual a zero."

    for trecho, deltaP in trecho_4_deltaP.items():
        print(f"Delta P para o trecho {trecho}: {deltaP}")
        
    deltaP_trechos_5_9 = {}
    for i in range(5, 10):
        do = buscar_valor(i, 'Do')
        di2 = buscar_valor(i, 'Di2')
        comprimento = buscar_valor(i, 'Comprimento')
        velocidade_media = velocidade5_9[i] if i in velocidade5_9 else 0 

        if do is not None and di2 is not None and comprimento is not None and (do - di2) != 0:
            deltaP = (
                (Ka * comprimento / (300 * (do - di2))) *
                ((0.8 * velocidade_media * (2 * Na + 1)) / ((do - di2) * Na) ** Na)
            )
            deltaP_trechos_5_9[i] = deltaP
        else:
            deltaP_trechos_5_9[i] = "Do, Di2 ou comprimento não disponível ou cálculo inválido."

    for trecho, deltaP in deltaP_trechos_5_9.items():
        print(f"Delta P para o trecho {trecho}: {deltaP}")
        
    soma_total_deltaP = 0
    for deltaP in deltaP_trechos_1_3.values():
        if isinstance(deltaP, (int, float)):
            soma_total_deltaP += deltaP

    for deltaP in trecho_4_deltaP.values():
        if isinstance(deltaP, (int, float)):
            soma_total_deltaP += deltaP

    for deltaP in deltaP_trechos_5_9.values():
        if isinstance(deltaP, (int, float)):
            soma_total_deltaP += deltaP
    print(f"Soma total de Delta P: {soma_total_deltaP}")


    Q_cascalho = 0.7*taxa_penetração_media*D_broca**2/314
    Q_anular = Q_cascalho + Q
    print(Q_anular)

    m_anular = (Q*m_fluido+Q_cascalho*8.34*m_cascalho)/Q_anular
    print(f"O peso específico no anular: {m_anular}")

    delta_P_hidrostatico = 0.17*(m_anular-m_fluido)*L
    print(f"O Delta P hidrostático: {delta_P_hidrostatico}")

    P_bengala = soma_total_deltaP + delta_P_hidrostatico
    print(f"A pressão no tubo de bengala vale: {P_bengala}")


    soma_total_deltaP_anular = 0
    for deltaP in deltaP_trechos_5_9.values():
        if isinstance(deltaP, (int, float)):
            soma_total_deltaP_anular += deltaP
            
    P_dinamica_no_fundo = 0.17*m_anular*L + soma_total_deltaP_anular
    print(f"A pressão dinâmica no fundo do poço: {P_dinamica_no_fundo}")


    Ecd_fundo = P_dinamica_no_fundo/(0.17*L)
    print(f"ECD no fundo do poço: {Ecd_fundo}")


    soma_total_deltaP_sapata = 0
    for trecho, deltaP in deltaP_trechos_5_9.items():
        if trecho in [8, 9] and isinstance(deltaP, (int, float)):
            soma_total_deltaP_sapata += deltaP
    P_dinamica_na_sapata = 0.17*m_anular*L_sapata + soma_total_deltaP_sapata
    print(f"A pressão dinâmica na sapata: {P_dinamica_na_sapata}")

    Ecd_sapata = P_dinamica_na_sapata/(0.17*L_sapata)
    print(f"ECD no fundo na sapata: {Ecd_sapata}")



    Vs = 113.4*np.sqrt(Dp*(m_cascalho* 8.34 - m_agua)/(Cr*m_agua))
    print(f"A velocidade e eficiência de remoção dos sólidos com os dados de poço: {Vs} ft/min")

    V_media = 24.51*Q_bomba/(D_broca**2 - D_tubo_P**2)
    print(f"A velocidade média do fluxo no anular: {V_media} ft/min")

    Vr = V_media - Vs
    print(f"A velocidade de remoção dos sólidos: {Vr} ft/min")

    ER = 100*Vr/V_media
    print(f"A eficiência de remoção será: {ER}%")



    peso_especifico_minimo = pressao_porosa / L*3.28084   #3.28084 m to pés
    print(f"Peso específico mínimo do fluido de perfuração: {peso_especifico_minimo:.2f} psi")
    
    # Adicione o valor de Q e ECD calculado para o fundo
    valores_Q.append(Q)
    valores_ECD_fundo.append(Ecd_fundo)

    # Adicione o valor de Q e ECD calculado para a sapata
    valores_ECD_sapata.append(Ecd_sapata)'''
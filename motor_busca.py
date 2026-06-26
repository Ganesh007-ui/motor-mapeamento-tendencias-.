from collections import Counter

# 1. SIMULAÇÃO DE DADOS RECEBIDOS DAS APIS (Google, Logs do Celular, etc.)
historico_buscas_usuario = [
    {"termo": "como pagar conta de luz atrasada", "categoria": "Serviços Públicos", "urgencia": True},
    {"termo": "reserva de mesa restaurante centro", "categoria": "Reservas", "urgencia": False},
    {"termo": "onibus para o trabalho rota mais rapida", "categoria": "Rotas e Mapas", "urgencia": True},
    {"termo": "segunda via fatura de agua", "categoria": "Serviços Públicos", "urgencia": False},
    {"termo": "pagamento pix parcelado", "categoria": "Pagamentos", "urgencia": False},
    {"termo": "transito na paulista agora", "categoria": "Rotas e Mapas", "urgencia": True},
    {"termo": "como parcelar debito de IPVA", "categoria": "Serviços Públicos", "urgencia": True},
]

# 2. FUNÇÃO QUE PROCESSA AS DORES E ENTENDE O ALGORITMO
def analisar_dores_usuario(historico):
    print("--- Processando dados do Motor de Busca em Tempo Real ---")
    
    categorias_procuradas = []
    termos_urgentes = []
    
    for busca in historico:
        categorias_procuradas.append(busca["categoria"])
        if busca["urgencia"]:
            termos_urgentes.append(busca["termo"])
            
    contador_categorias = Counter(categorias_procuradas)
    dor_principal, frequencia = contador_categorias.most_common(1)[0]
    
    return dor_principal, frequencia, termos_urgentes

# 3. EXECUTANDO O MOTOR
dor_detectada, vezes, urgencias = analisar_dores_usuario(historico_buscas_usuario)

# 4. A REGRA DE NEGÓCIO: RESOLVENDO A DOR DO CLIENTE
print("\n================ RESULTADO DO ALGORITMO ================")
print(f"💡 Diagnóstico: A maior dor atual do cliente é: **{dor_detectada}** (Interagiu {vezes} vezes)")
print(f"🚨 Alertas de Urgência detectados: {urgencias}")
print("========================================================")

print("\n⚡ [AÇÃO DO APP]: Alterando a interface para o usuário...")
if dor_detectada == "Serviços Públicos":
    print("👉 Atalho destacado na Home: 'Pagar Contas e Emitir 2ª Via de Impostos/Contas'.")
elif dor_detectada == "Rotas e Mapas":
    print("👉 Atalho destacado na Home: 'Traçar rota rápida para seus destinos frequentes'.")
else:
    print("👉 Atalho destacado na Home: 'Serviços Gerais de Pagamento'.")

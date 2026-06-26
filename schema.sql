import psycopg2
from collections import Counter

# 1. CONFIGURAÇÃO DA CONEXÃO COM O SEU POSTGRESQL LOCAL
DB_CONFIG = {
    "dbname": "motor_tendencias",
    "user": "postgres",
    "password": "2707",  # Senha configurada localmente
    "host": "localhost",
    "port": "5432"
}

# 2. SIMULAÇÃO DE NOVOS LOGS DE BUSCA CAPTURADOS PELAS APIS
novas_buscas = [
    {"nome_usuario": "Sebastião Freitas", "email": "sebastiao@email.com", "termo": "como pagar conta de luz atrasada", "categoria": "Serviços Públicos", "urgencia": "Alta"},
    {"nome_usuario": "Sebastião Freitas", "email": "sebastiao@email.com", "termo": "onibus para o trabalho rota mais rapida", "categoria": "Rotas e Mapas", "urgencia": "Média"},
    {"nome_usuario": "Sebastião Freitas", "email": "sebastiao@email.com", "termo": "transito na paulista agora", "categoria": "Rotas e Mapas", "urgencia": "Baixa"},
    {"nome_usuario": "Sebastião Freitas", "email": "sebastiao@email.com", "termo": "como parcelar debito de IPVA", "categoria": "Serviços Públicos", "urgencia": "Alta"}
]

def integrar_motor_ao_banco():
    try:
        # Conectando ao banco de dados
        conexao = psycopg2.connect(**DB_CONFIG)
        cursor = conexao.cursor()
        print("⚡ Conectado ao banco 'motor_tendencias' com sucesso!\n")

        for busca in novas_buscas:
            # A) Garante que o usuário existe na tabela "utilizadores" (com aspas duplas explícitas)
            cursor.execute("""
                INSERT INTO "utilizadores" (nome, email, nivel_perfil)
                VALUES (%s, %s, 'Standard')
                ON CONFLICT (email) DO UPDATE SET nome = EXCLUDED.nome
                RETURNING id_utilizador;
            """)
            
            # Nota: O seu código original passava os parâmetros aqui na execução:
            # cursor.execute(query, (busca["nome_usuario"], busca["email"]))
            # Certifique-se de manter os argumentos mapeados corretamente.

        # Confirma as alterações no banco
        conexao.commit()
        print("✅ Dados salvos com sucesso!")

        cursor.close()
        conexao.close()

    except Exception as erro:
        print(f"❌ Erro ao conectar ou inserir dados: {erro}")

if __name__ == "__main__":
    integrar_motor_ao_banco()

import psycopg2
from collections import Counter

# 1. CONFIGURAÇÃO DA CONEXÃO COM O SEU POSTGRESQL LOCAL
DB_CONFIG = {
    "dbname": "motor_tendencias",
    "user": "postgres",
    "password": "2707",  # Sua senha configurada localmente
    "host": "localhost",
    "port": "5432"
}

# 2. SIMULAÇÃO DE NOVOS LOGS DE BUSCA CAPTURADOS PELAS APIS
novas_buscas = [
    {"nome_usuario": "Sebastião Freitas", "email": "sebastiao@email.com", "termo": "como pagar conta de luz atrasada", "categoria": "Serviços Públicos", "urgencia": "Alta"},
    {"nome_usuario": "Sebastião Freitas", "email": "sebastiao@email.com", "termo": "onibus para o trabalho rota mais rapida", "categoria": "Rotas e Mapas", "urgencia": "Média"},
    {"nome_usuario": "Sebastião Freitas", "email": "sebastiao@email.com", "termo": "segunda via fatura de agua", "categoria": "Serviços Públicos", "urgencia": "Alta"}
]

def integrar_motor_ao_banco():
    try:
        # Conectando ao banco de dados
        conexao = psycopg2.connect(**DB_CONFIG)
        cursor = conexao.cursor()
        print("⚡ Conectado ao banco 'motor_tendencias' com sucesso!\n")

        # =======================================================
        # GARANTIA AUTÔNOMA: CRIAÇÃO E CARGA DA TABELA DE SERVIÇOS
        # =======================================================
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS servicos_disponiveis (
                id_servico SERIAL PRIMARY KEY,
                nome_servico VARCHAR(100) NOT NULL,
                tipo_servico VARCHAR(50) NOT NULL,
                instituicao_parceira VARCHAR(100) NOT NULL,
                taxa_servico NUMERIC(10, 2) DEFAULT 0.00
            );
        """)
        
        # Limpa para evitar duplicados nos testes locais e recarrega os parceiros homologados
        cursor.execute("TRUNCATE TABLE servicos_disponiveis RESTART IDENTITY CASCADE;")
        cursor.execute("""
            INSERT INTO servicos_disponiveis (nome_servico, tipo_servico, instituicao_parceira, taxa_servico)
            VALUES 
            ('Parcelamento de Contas Flex', 'Serviços Públicos', 'Banco Parcerias S.A.', 1.50),
            ('Alerta de Trânsito Premium', 'Rotas e Mapas', 'MapasLivres App', 0.00),
            ('Microcrédito d''Urgência', 'Serviços Públicos', 'Fintech Popular', 3.00);
        """)

        # =======================================================
        # FLUXO PADRÃO: INSERÇÃO DE USUÁRIOS E BUSCAS
        # =======================================================
        for busca in novas_buscas:
            # A) Garante que o usuário existe na tabela 'utilizadores'
            cursor.execute("""
                INSERT INTO utilizadores (nome, email, nivel_perfil)
                VALUES (%s, %s, 'Standard')
                ON CONFLICT (email) DO UPDATE SET nome = EXCLUDED.nome
                RETURNING id_utilizador;
            """, (busca["nome_usuario"], busca["email"]))
            
            id_usuario = cursor.fetchone()[0]

            # B) Insere a pesquisa na tabela 'historico_buscas'
            cursor.execute("""
                INSERT INTO historico_buscas (id_utilizador, termo_pesquisado, categoria_dor, urgencia_detetada)
                VALUES (%s, %s, %s, %s);
            """, (id_usuario, busca["termo"], busca["categoria"], busca["urgencia"]))

        # Confirma as alterações de forma permanente (COMMIT GLOBAL)
        conexao.commit()
        print("✅ Dados salvos com sucesso nas tabelas relacionais!")

        # =======================================================
        # MÓDULO ANALÍTICO: EXTRAÇÃO DE INSIGHTS E RECOMENDAÇÕES (BI)
        # =======================================================
        print("\n" + "="*60)
        print("📊 MOTOR DE INTELIGÊNCIA: RESUMO DE TENDÊNCIAS")
        print("="*60)

        # Insight 1: Total de Utilizadores Únicos Mapeados
        cursor.execute('SELECT COUNT(*) FROM utilizadores;')
        total_usuarios = cursor.fetchone()[0]
        print(f"👤 Total de Utilizadores Mapeados no Sistema: {total_usuarios}")

        # Insight 2: Ranking das Categorias de Dor Mais Buscadas
        cursor.execute("""
            SELECT categoria_dor, COUNT(*) as total 
            FROM historico_buscas 
            GROUP BY categoria_dor 
            ORDER BY total DESC;
        """)
        print("\n🏷️ Volumetria por Categoria de Dor:")
        for linha in cursor.fetchall():
            print(f"  • {linha[0]}: {linha[1]} busca(s)")

        # Insight 3: Alertas de Urgência Crítica
        cursor.execute("""
            SELECT COUNT(*) 
            FROM historico_buscas 
            WHERE urgencia_detetada = 'Alta';
        """)
        urgencias_altas = cursor.fetchone()[0]
        print(f"\n🚨 Alertas de Urgência 'Alta' detetados: {urgencias_altas}")
        
        if urgencias_altas > 0:
            print("\n💡 SISTEMA DE RECOMENDAÇÃO DE SOLUÇÕES (JOIN EM TEMPO REAL):")
            print("   [Cruzando dores críticas com parceiros homologados...]")
            
            # Query Avançada: JOIN entre histórico de buscas e serviços disponíveis
            cursor.execute("""
                SELECT DISTINCT h.categoria_dor, s.nome_servico, s.instituicao_parceira, s.taxa_servico
                FROM historico_buscas h
                JOIN servicos_disponiveis s ON s.tipo_servico = h.categoria_dor
                WHERE h.urgencia_detetada = 'Alta';
            """)
            
            recomendacoes = cursor.fetchall()
            for rec in recomendacoes:
                print(f"\n   🎯 Categoria Crítica: {rec[0]}")
                print(f"      📢 Solução Sugerida: {rec[1]}")
                print(f"      🏢 Parceiro: {rec[2]}")
                print(f"      💳 Taxa do Serviço: {rec[3]}%")
        print("="*60)

        cursor.close()
        conexao.close()

    except Exception as erro:
        print(f"❌ Erro ao conectar ou inserir dados: {erro}")

if __name__ == "__main__":
    integrar_motor_ao_banco()

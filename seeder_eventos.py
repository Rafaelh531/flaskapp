import psycopg2
import random

def populate_database_with_events(host, database, user, password, table_name, num_records, num_armadilhas):
    """
    Popula um banco de dados PostgreSQL com registros aleatórios para uma tabela com colunas id, id_armadilha, score, temp e umidade.

    Args:
        host (str): Endereço do servidor PostgreSQL.
        database (str): Nome do banco de dados.
        user (str): Usuário do banco de dados.
        password (str): Senha do usuário.
        table_name (str): Nome da tabela a ser populada.
        num_records (int): Número de registros a serem inseridos.
        num_armadilhas (int): Número de armadilhas disponíveis.
    """
    try:
        # Conectando ao banco de dados
        conn = psycopg2.connect(host=host, database=database, user=user, password=password)
        cursor = conn.cursor()

        # Gerar e inserir registros aleatórios
        for record_id in range(1, num_records + 1):
            id_armadilha = random.randint(1, num_armadilhas)  # ID da armadilha (entre 1 e num_armadilhas)
            score = round(random.uniform(0, 1), 2)  # Score entre 0 e 1
            temp = round(random.uniform(15, 40), 1)  # Temperatura entre 15 e 40 graus Celsius
            umidade = round(random.uniform(30, 90), 1)  # Umidade entre 30% e 90%

            query = f"""INSERT INTO {table_name} (id, id_armadilha, score, temp, umidade) VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(query, (record_id, id_armadilha, score, temp, umidade))

        # Confirmar as alterações no banco de dados
        conn.commit()
        print(f"{num_records} registros inseridos com sucesso na tabela '{table_name}'.")

    except psycopg2.Error as e:
        print(f"Erro ao acessar o banco de dados: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Exemplo de uso:
populate_database_with_events('dpg-ctg5u0hopnds73dllme0-a.oregon-postgres.render.com', 'mosquitodb', "mosquitodb_user", 'j5uG5nEkVlPhEIIaG4ggrVavmBM2oNyz', 'eventos', 200, 10)
import psycopg2
import random

def populate_database(host, database, user, password, table_name, num_records):
    """
    Popula um banco de dados PostgreSQL com registros aleatórios para uma tabela com colunas id, latitude e longitude.

    Args:
        host (str): Endereço do servidor PostgreSQL.
        database (str): Nome do banco de dados.
        user (str): Usuário do banco de dados.
        password (str): Senha do usuário.
        table_name (str): Nome da tabela a ser populada.
        num_records (int): Número de registros a serem inseridos.
    """
    try:
        # Conectando ao banco de dados
        conn = psycopg2.connect(host=host, database=database, user=user, password=password)
        cursor = conn.cursor()

        # Deletar todos os dados da tabela
        cursor.execute(f"TRUNCATE TABLE {table_name} RESTART IDENTITY")

        # Gerar e inserir registros aleatórios
        for record_id in range(1, num_records + 1):
            latitude = random.uniform(-25.5852, -25.4521)  # Faixa aproximada de latitude para Foz do Iguaçu
            longitude = random.uniform(-54.6266, -54.4357)  # Faixa aproximada de longitude para Foz do Iguaçu

            query = f"""INSERT INTO {table_name} (id, latitude, longitude) VALUES (%s, %s, %s)"""
            cursor.execute(query, (record_id, latitude, longitude))

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
populate_database('dpg-ctg5u0hopnds73dllme0-a.oregon-postgres.render.com', 'mosquitodb', "mosquitodb_user", 'j5uG5nEkVlPhEIIaG4ggrVavmBM2oNyz', 'armadilhas', 50)

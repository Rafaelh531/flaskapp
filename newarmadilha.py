import psycopg2
import random


def add_record(host, database, user, password, table_name, record_id, latitude, longitude):
    """
    Adiciona um único registro ao banco de dados PostgreSQL.

    Args:
        host (str): Endereço do servidor PostgreSQL.
        database (str): Nome do banco de dados.
        user (str): Usuário do banco de dados.
        password (str): Senha do usuário.
        table_name (str): Nome da tabela a ser populada.
        record_id (int): ID do registro a ser inserido.
        latitude (float): Latitude do registro.
        longitude (float): Longitude do registro.
    """
    try:
        # Conectando ao banco de dados
        conn = psycopg2.connect(host=host, database=database, user=user, password=password)
        cursor = conn.cursor()

        # Inserir um único registro
        query = f"""INSERT INTO {table_name} (id, latitude, longitude) VALUES (%s, %s, %s)"""
        cursor.execute(query, (record_id, latitude, longitude))

        # Confirmar as alterações no banco de dados
        conn.commit()
        print(f"Registro {record_id} inserido com sucesso na tabela '{table_name}'.")

    except psycopg2.Error as e:
        print(f"Erro ao acessar o banco de dados: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Exemplo de uso:
add_record('dpg-ctg5u0hopnds73dllme0-a.oregon-postgres.render.com', 'mosquitodb', "mosquitodb_user", 'j5uG5nEkVlPhEIIaG4ggrVavmBM2oNyz', 'armadilhas', 5, -25.5000, -54.5000)
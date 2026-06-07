from cassandra.cluster import Cluster


class DatabaseCassandra:
    def __init__(self):
        cluster = Cluster(['cassandra'])
        self.session = cluster.connect()

        self.session.execute("""
            CREATE KEYSPACE IF NOT EXISTS night_city
            WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}
        """)

        self.session.set_keyspace("night_city")

        self.session.execute("""
            CREATE TABLE IF NOT EXISTS entities (
                entity_type TEXT,
                pk          TEXT,
                PRIMARY KEY (entity_type, pk)
            )
        """)

    def create(self, entity_type, pk):
        """Insere um registro de tipo + pk."""
        self.session.execute(
            "INSERT INTO entities (entity_type, pk) VALUES (%s, %s)",
            (entity_type, pk)
        )

    def read(self, entity_type, pk):
        """Busca um registro pelo tipo e pk. Retorna dict ou None."""
        row = self.session.execute(
            "SELECT entity_type, pk FROM entities WHERE entity_type = %s AND pk = %s",
            (entity_type, pk)
        ).one()
        return {"entity_type": row.entity_type, "pk": row.pk} if row else None

    def read_all(self, entity_type):
        """Retorna todos os registros de um tipo."""
        rows = self.session.execute(
            "SELECT entity_type, pk FROM entities WHERE entity_type = %s",
            (entity_type,)
        )
        return [{"entity_type": row.entity_type, "pk": row.pk} for row in rows]

    def delete(self, entity_type, pk):
        """Remove um registro pelo tipo e pk."""
        self.session.execute(
            "DELETE FROM entities WHERE entity_type = %s AND pk = %s",
            (entity_type, pk)
        )

    def drop_all(self):
        """Apaga todos os registros da tabela."""
        self.session.execute("TRUNCATE entities")
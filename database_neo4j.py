from neo4j import GraphDatabase

class DatabaseNeo4j:
    def __init__(self):
        self.driver = GraphDatabase.driver("bolt://neo4j:7687")

    def close(self):
        """Fecha a conexão com o banco."""
        self.driver.close()

    def create(self, entity_type, entity):
        """
        Cria um nó no grafo com o tipo e os campos pk e name.
        entity_type: label do nó (ex: 'cyberware', 'ripperdoc', 'client')
        entity: dict com ao menos 'pk' e 'name'
        """
        with self.driver.session() as session:
            session.run(
                f"CREATE (:{entity_type} {{pk: $pk, name: $name}})",
                pk=entity["pk"],
                name=entity["name"]
            )

    def read(self, entity_type, entity_id):
        """Busca um nó pelo pk e retorna seus campos."""
        with self.driver.session() as session:
            result = session.run(
                f"MATCH (n:{entity_type} {{pk: $pk}}) RETURN n",
                pk=entity_id
            )
            record = result.single()
            return dict(record["n"]) if record else None

    def connect_cyberware_ripperdoc(self, cyberware_pk, ripperdoc_pk):
        """
        Cria a relação: (ripperdoc)-[:SELLS]->(cyberware)
        Indica que um ripperdoc oferece/vende determinado cyberware.
        """
        with self.driver.session() as session:
            session.run(
                """
                MATCH (c:cyberware {pk: $cyberware_pk})
                MATCH (r:ripperdoc  {pk: $ripperdoc_pk})
                MERGE (r)-[:SELLS]->(c)
                """,
                cyberware_pk=cyberware_pk,
                ripperdoc_pk=ripperdoc_pk
            )

    def connect_cyberware_ripperdoc_client(self, cyberware_pk, ripperdoc_pk, client_pk):
        """
        Cria a relação: (client)-[:BOUGHT {via_ripperdoc}]->(cyberware)
        Registra que um cliente comprou um cyberware através de um ripperdoc.
        """
        with self.driver.session() as session:
            session.run(
                """
                MATCH (c:cyberware {pk: $cyberware_pk})
                MATCH (r:ripperdoc  {pk: $ripperdoc_pk})
                MATCH (cl:client    {pk: $client_pk})
                MERGE (cl)-[:BOUGHT {via_ripperdoc: r.pk}]->(c)
                """,
                cyberware_pk=cyberware_pk,
                ripperdoc_pk=ripperdoc_pk,
                client_pk=client_pk
            )

    def read_cyberwares_by_ripperdoc(self, ripperdoc_pk):
        """Retorna todos os cyberwares vendidos por um ripperdoc."""
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (r:ripperdoc {pk: $ripperdoc_pk})-[:SELLS]->(c:cyberware)
                RETURN c
                """,
                ripperdoc_pk=ripperdoc_pk
            )
            return [dict(record["c"]) for record in result]

    def read_clients_by_cyberware(self, cyberware_pk):
        """Retorna todos os clientes que compraram determinado cyberware."""
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (cl:client)-[:BOUGHT]->(c:cyberware {pk: $cyberware_pk})
                RETURN cl
                """,
                cyberware_pk=cyberware_pk
            )
            return [dict(record["cl"]) for record in result]
        
    def drop_all(self):
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
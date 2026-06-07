from database_mongodb import DatabaseMongo
from database_neo4j import DatabaseNeo4j
from database_cassandra import DatabaseCassandra

dbmongo = DatabaseMongo()
dbneo4j = DatabaseNeo4j()
dbcassandra = DatabaseCassandra()

# ── Helpers de exibição ───────────────────────────────────────────────────────

def print_divider():
    print("-" * 40)

def print_entity(label, data):
    """Imprime os campos de um documento/nó formatado."""
    print(f"\n  [{label}]")
    for key, value in data.items():
        if key != "_id":
            print(f"    {key}: {value}")

def print_list(label, items):
    if not items:
        print(f"  Nenhum {label} encontrado.\n")
        return
    for item in items:
        print_entity(label, item)
    print()


# ── Criação de entidades (MongoDB + nó no Neo4j) ──────────────────────────────

def create_cyberware():
    name   = input("Name: ")
    corp   = input("Provider: ")
    pk     = input("Primary Key: ")
    price  = input("Base Price: ")
    part   = input("Body Part: ")
    danger = input("Danger Level: ")

    cyberware = {
        "pk":           pk,
        "name":         name,
        "corp":         corp,
        "price":        price,
        "body_part":    part,
        "danger_level": danger
    }

    dbmongo.create("cyberware", cyberware)
    dbneo4j.create("cyberware", {"pk": pk, "name": name})
    dbcassandra.create("cyberware", pk)
    print(f"[✓] Cyberware '{name}' registrado com sucesso.\n")


def create_ripperdoc():
    name   = input("Name: ")
    pk     = input("Primary Key: ")
    region = input("Working Region: ")
    price  = input("Base Price: ")

    ripperdoc = {
        "pk":         pk,
        "name":       name,
        "region":     region,
        "base_price": price
    }

    dbmongo.create("ripperdoc", ripperdoc)
    dbneo4j.create("ripperdoc", {"pk": pk, "name": name})
    dbcassandra.create("ripperdoc", pk)
    print(f"[✓] Ripperdoc '{name}' registrado com sucesso.\n")


def create_client():
    name      = input("Name: ")
    pk        = input("Primary Key: ")
    tolerance = input("Psycho Tolerance: ")

    client = {
        "pk":               pk,
        "name":             name,
        "psycho_tolerance": tolerance
    }

    dbmongo.create("client", client)
    dbneo4j.create("client", {"pk": pk, "name": name})
    dbcassandra.create("client", pk)
    print(f"[✓] Cliente '{name}' registrado com sucesso.\n")


# ── Conexões entre entidades (Neo4j) ─────────────────────────────────────────

def connect_cyberware_ripperdoc():
    """Registra que um ripperdoc oferece determinado cyberware."""
    cyberware_pk = input("Cyberware Primary Key: ")
    ripperdoc_pk = input("Ripperdoc Primary Key: ")

    cw = dbmongo.read("cyberware", cyberware_pk)
    rd = dbmongo.read("ripperdoc", ripperdoc_pk)

    if not cw:
        print(f"[✗] Cyberware com pk '{cyberware_pk}' não encontrado.\n")
        return
    if not rd:
        print(f"[✗] Ripperdoc com pk '{ripperdoc_pk}' não encontrado.\n")
        return

    dbneo4j.connect_cyberware_ripperdoc(cyberware_pk, ripperdoc_pk)
    print(f"[✓] Relação criada: Ripperdoc '{rd['name']}' -[:SELLS]-> Cyberware '{cw['name']}'\n")


def connect_cyberware_ripperdoc_client():
    """Registra que um cliente comprou um cyberware via ripperdoc."""
    cyberware_pk = input("Cyberware Primary Key: ")
    ripperdoc_pk = input("Ripperdoc Primary Key: ")
    client_pk    = input("Client Primary Key: ")

    cw = dbmongo.read("cyberware", cyberware_pk)
    rd = dbmongo.read("ripperdoc", ripperdoc_pk)
    cl = dbmongo.read("client",    client_pk)

    if not cw:
        print(f"[✗] Cyberware com pk '{cyberware_pk}' não encontrado.\n")
        return
    if not rd:
        print(f"[✗] Ripperdoc com pk '{ripperdoc_pk}' não encontrado.\n")
        return
    if not cl:
        print(f"[✗] Cliente com pk '{client_pk}' não encontrado.\n")
        return

    dbneo4j.connect_cyberware_ripperdoc_client(cyberware_pk, ripperdoc_pk, client_pk)
    print(
        f"[✓] Relação criada: Cliente '{cl['name']}' "
        f"-[:BOUGHT via '{rd['name']}']-> Cyberware '{cw['name']}'\n"
    )


# ── Leitura de entidades (MongoDB) ────────────────────────────────────────────

def read_cyberware():
    print("\n  1- Buscar por PK")
    print("  2- Listar todos")
    sub = input("  Opção: ").strip()

    if sub == "1":
        pk = input("  Primary Key: ")
        result = dbmongo.read("cyberware", pk)
        if result:
            print_entity("Cyberware", result)
        else:
            print(f"  [✗] Cyberware '{pk}' não encontrado.\n")

    elif sub == "2":
        results = dbmongo.read_all("cyberware")
        print_divider()
        print_list("Cyberware", results)

    else:
        print("  [!] Opção inválida.\n")


def read_ripperdoc():
    print("\n  1- Buscar por PK")
    print("  2- Listar todos")
    sub = input("  Opção: ").strip()

    if sub == "1":
        pk = input("  Primary Key: ")
        result = dbmongo.read("ripperdoc", pk)
        if result:
            print_entity("Ripperdoc", result)
        else:
            print(f"  [✗] Ripperdoc '{pk}' não encontrado.\n")

    elif sub == "2":
        results = dbmongo.read_all("ripperdoc")
        print_divider()
        print_list("Ripperdoc", results)

    else:
        print("  [!] Opção inválida.\n")


def read_client():
    print("\n  1- Buscar por PK")
    print("  2- Listar todos")
    sub = input("  Opção: ").strip()

    if sub == "1":
        pk = input("  Primary Key: ")
        result = dbmongo.read("client", pk)
        if result:
            print_entity("Client", result)
        else:
            print(f"  [✗] Cliente '{pk}' não encontrado.\n")

    elif sub == "2":
        results = dbmongo.read_all("client")
        print_divider()
        print_list("Client", results)

    else:
        print("  [!] Opção inválida.\n")


# ── Leitura de relacionamentos (Neo4j) ────────────────────────────────────────

def read_cyberwares_by_ripperdoc():
    """Quais cyberwares um ripperdoc vende?"""
    pk = input("  Ripperdoc Primary Key: ")
    rd = dbmongo.read("ripperdoc", pk)
    if not rd:
        print(f"  [✗] Ripperdoc '{pk}' não encontrado.\n")
        return

    results = dbneo4j.read_cyberwares_by_ripperdoc(pk)
    print_divider()
    print(f"  Cyberwares vendidos por '{rd['name']}':")
    print_list("Cyberware", results)


def read_clients_by_cyberware():
    """Quais clientes compraram determinado cyberware?"""
    pk = input("  Cyberware Primary Key: ")
    cw = dbmongo.read("cyberware", pk)
    if not cw:
        print(f"  [✗] Cyberware '{pk}' não encontrado.\n")
        return

    results = dbneo4j.read_clients_by_cyberware(pk)

    # Enriquece com dados completos do MongoDB
    enriched = []
    for node in results:
        full = dbmongo.read("client", node["pk"])
        enriched.append(full if full else node)

    print_divider()
    print(f"  Clientes que compraram '{cw['name']}':")
    print_list("Client", enriched)

# ── Leitura de chaves primárias (Cassandra) ───────────────────────────────────

def count_cyberwares():
    cyberwares = dbcassandra.read_all("cyberware")
    number = len(cyberwares)
    print(f"O sistema possui {number} cyberwares cadastrados: ")
    for item in cyberwares:
        print(item["pk"])

def count_ripperdocs():
    ripperdocs = dbcassandra.read_all("ripperdoc")
    number = len(ripperdocs)
    print(f"O sistema possui {number} ripperdocs cadastrados: ")
    for item in ripperdocs:
        print(item["pk"])

def count_clients():
    clients = dbcassandra.read_all("client")
    number = len(clients)
    print(f"O sistema possui {number} clientes cadastrados: ")
    for item in clients:
        print(item["pk"])

# ── Submenus ──────────────────────────────────────────────────────────────────

def menu_read():
    opt = -1
    while opt != 0:
        print("\n" + "=" * 40)
        print("         CONSULTAS")
        print("=" * 40)
        print("  — Entidades (MongoDB) —")
        print("  1- Consultar Cyberware")
        print("  2- Consultar Ripperdoc")
        print("  3- Consultar Cliente")
        print("  — Relacionamentos (Neo4j) —")
        print("  4- Cyberwares de um Ripperdoc")
        print("  5- Clientes que compraram um Cyberware")
        print("  — Chaves primárias (Cassandra) —")
        print("  6- Consultar número total de Cyberwares")
        print("  7- Consultar número total de Ripperdocs")
        print("  8- Consultar número total de Clientes")
        print("  0- Voltar")
        print("=" * 40)

        try:
            opt = int(input("  Opção: "))
        except ValueError:
            print("  [!] Entrada inválida.\n")
            continue

        match opt:
            case 0:
                pass
            case 1:
                read_cyberware()
            case 2:
                read_ripperdoc()
            case 3:
                read_client()
            case 4:
                read_cyberwares_by_ripperdoc()
            case 5:
                read_clients_by_cyberware()
            case 6:
                count_cyberwares()
            case 7:
                count_ripperdocs()
            case 8:
                count_clients()
            case _:
                print("  [!] Opção inválida.\n")


# ── Submenu de cadastros ──────────────────────────────────────────────────────

def menu_create():
    opt = -1
    while opt != 0:
        print("\n" + "=" * 40)
        print("           CADASTROS")
        print("=" * 40)
        print("  1- Cadastrar Cyberware")
        print("  2- Cadastrar Ripperdoc")
        print("  3- Cadastrar Cliente")
        print("  0- Voltar")
        print("=" * 40)

        try:
            opt = int(input("  Opção: "))
        except ValueError:
            print("  [!] Entrada inválida.\n")
            continue

        match opt:
            case 0:
                pass
            case 1:
                create_cyberware()
            case 2:
                create_ripperdoc()
            case 3:
                create_client()
            case _:
                print("  [!] Opção inválida.\n")


# ── Submenu de relacionamentos ────────────────────────────────────────────────

def menu_connect():
    opt = -1
    while opt != 0:
        print("\n" + "=" * 40)
        print("        RELACIONAMENTOS")
        print("=" * 40)
        print("  1- Vincular Cyberware ↔ Ripperdoc")
        print("  2- Registrar Compra (Cliente/Ripperdoc/Cyberware)")
        print("  0- Voltar")
        print("=" * 40)

        try:
            opt = int(input("  Opção: "))
        except ValueError:
            print("  [!] Entrada inválida.\n")
            continue

        match opt:
            case 0:
                pass
            case 1:
                connect_cyberware_ripperdoc()
            case 2:
                connect_cyberware_ripperdoc_client()
            case _:
                print("  [!] Opção inválida.\n")


# ── Submenu de relacionamentos ────────────────────────────────────────────────

def menu_hackear():
    opt = -1
    while opt != 0:
        print("\n" + "=" * 40)
        print("        HACKEAR")
        print("=" * 40)
        print("  1- Deletar todos os registros")
        print("  0- Voltar")
        print("=" * 40)

        try:
            opt = int(input("  Opção: "))
        except ValueError:
            print("  [!] Entrada inválida.\n")
            continue

        match opt:
            case 0:
                pass
            case 1:
                dbmongo.drop_all()
                dbneo4j.drop_all()
                dbcassandra.drop_all()
            case _:
                print("  [!] Opção inválida.\n")


# ── Menu principal ────────────────────────────────────────────────────────────

def main():
    opt = -1

    while opt != 0:
        print("\n" + "=" * 40)
        print("        NIGHT CITY DATABASE")
        print("=" * 40)
        print("  1- Cadastros")
        print("  2- Relacionamentos")
        print("  3- Consultas")
        print("  4- Hackear!")
        print("  0- Sair")
        print("=" * 40)

        try:
            opt = int(input("  Escolha uma opção: "))
        except ValueError:
            print("  [!] Entrada inválida. Digite um número.\n")
            continue

        match opt:
            case 0:
                print("Saindo... Samurai, we have a city to burn. 🔥")
            case 1:
                menu_create()
            case 2:
                menu_connect()
            case 3:
                menu_read()
            case 4:
                menu_hackear()
            case _:
                print("  [!] Opção inválida.\n")

    dbneo4j.close()


if __name__ == "__main__":
    main()
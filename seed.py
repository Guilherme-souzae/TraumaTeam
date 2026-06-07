import sys
from database_mongodb import DatabaseMongo
from database_neo4j import DatabaseNeo4j
from database_cassandra import DatabaseCassandra

dbmongo = DatabaseMongo()
dbneo4j = DatabaseNeo4j()
dbcassandra = DatabaseCassandra()

# ── Dados de seed ─────────────────────────────────────────────────────────────

CYBERWARES = [
    {"pk": "cw001", "name": "Mantis Blades",        "corp": "Arasaka",    "price": "45000", "body_part": "arms",  "danger_level": "5"},
    {"pk": "cw002", "name": "Gorilla Arms",          "corp": "Militech",   "price": "38000", "body_part": "arms",  "danger_level": "4"},
    {"pk": "cw003", "name": "Monowire",              "corp": "Kang Tao",   "price": "52000", "body_part": "hands", "danger_level": "5"},
    {"pk": "cw004", "name": "Sandevistan",           "corp": "Zetatech",   "price": "75000", "body_part": "spine", "danger_level": "3"},
    {"pk": "cw005", "name": "Kiroshi Optical MK3",  "corp": "Kiroshi",    "price": "29000", "body_part": "eyes",  "danger_level": "1"},
    {"pk": "cw006", "name": "Subdermal Armor",       "corp": "Militech",   "price": "33000", "body_part": "skin",  "danger_level": "2"},
    {"pk": "cw007", "name": "Projectile Launch System", "corp": "Arasaka", "price": "61000", "body_part": "arms",  "danger_level": "5"},
    {"pk": "cw008", "name": "Kerenzikov",            "corp": "Zetatech",   "price": "41000", "body_part": "spine", "danger_level": "3"},
    {"pk": "cw009", "name": "Second Heart",          "corp": "Biotechnica","price": "55000", "body_part": "chest", "danger_level": "2"},
    {"pk": "cw010", "name": "Cyberdeck Militech",    "corp": "Militech",   "price": "48000", "body_part": "skull", "danger_level": "4"},
]

RIPPERDOCS = [
    {"pk": "rd001", "name": "Viktor Vector",    "region": "Watson",       "base_price": "500"},
    {"pk": "rd002", "name": "Fingers",          "region": "Japantown",    "base_price": "300"},
    {"pk": "rd003", "name": "Cassius Ryder",    "region": "Santo Domingo", "base_price": "450"},
    {"pk": "rd004", "name": "Mama Welles",      "region": "Heywood",      "base_price": "400"},
    {"pk": "rd005", "name": "Octavio",          "region": "Pacifica",     "base_price": "250"},
]

CLIENTS = [
    {"pk": "cl001", "name": "V",            "psycho_tolerance": "85"},
    {"pk": "cl002", "name": "Jackie Welles","psycho_tolerance": "70"},
    {"pk": "cl003", "name": "Judy Alvarez", "psycho_tolerance": "60"},
    {"pk": "cl004", "name": "Panam Palmer", "psycho_tolerance": "75"},
    {"pk": "cl005", "name": "River Ward",   "psycho_tolerance": "65"},
    {"pk": "cl006", "name": "Kerry Eurodyne","psycho_tolerance": "50"},
    {"pk": "cl007", "name": "Goro Takemura","psycho_tolerance": "90"},
    {"pk": "cl008", "name": "Rogue Amendiares","psycho_tolerance": "95"},
]

# (ripperdoc_pk, cyberware_pk) — quais cyberwares cada ripperdoc vende
SELLS = [
    ("rd001", "cw001"), ("rd001", "cw004"), ("rd001", "cw005"), ("rd001", "cw008"),
    ("rd002", "cw002"), ("rd002", "cw006"), ("rd002", "cw009"),
    ("rd003", "cw003"), ("rd003", "cw007"), ("rd003", "cw010"),
    ("rd004", "cw001"), ("rd004", "cw005"), ("rd004", "cw006"),
    ("rd005", "cw002"), ("rd005", "cw008"), ("rd005", "cw009"),
]

# (client_pk, ripperdoc_pk, cyberware_pk) — compras realizadas
PURCHASES = [
    ("cl001", "rd001", "cw001"),
    ("cl001", "rd001", "cw004"),
    ("cl001", "rd001", "cw005"),
    ("cl002", "rd001", "cw002"),
    ("cl002", "rd002", "cw006"),
    ("cl003", "rd002", "cw009"),
    ("cl004", "rd003", "cw003"),
    ("cl004", "rd005", "cw008"),
    ("cl005", "rd004", "cw005"),
    ("cl006", "rd004", "cw006"),
    ("cl007", "rd001", "cw004"),
    ("cl007", "rd003", "cw010"),
    ("cl008", "rd001", "cw001"),
    ("cl008", "rd003", "cw007"),
]

# ── Funções de inserção ───────────────────────────────────────────────────────

def seed_mongodb():
    print("\n[MongoDB] Inserindo entidades...")

    for cw in CYBERWARES:
        dbmongo.create("cyberware", cw)
    print(f"  ✓ {len(CYBERWARES)} cyberwares inseridos")

    for rd in RIPPERDOCS:
        dbmongo.create("ripperdoc", rd)
    print(f"  ✓ {len(RIPPERDOCS)} ripperdocs inseridos")

    for cl in CLIENTS:
        dbmongo.create("client", cl)
    print(f"  ✓ {len(CLIENTS)} clientes inseridos")

def seed_neo4j():
    print("\n[Neo4j] Inserindo nós...")

    for cw in CYBERWARES:
        dbneo4j.create("cyberware", {"pk": cw["pk"], "name": cw["name"]})
    print(f"  ✓ {len(CYBERWARES)} nós Cyberware criados")

    for rd in RIPPERDOCS:
        dbneo4j.create("ripperdoc", {"pk": rd["pk"], "name": rd["name"]})
    print(f"  ✓ {len(RIPPERDOCS)} nós Ripperdoc criados")

    for cl in CLIENTS:
        dbneo4j.create("client", {"pk": cl["pk"], "name": cl["name"]})
    print(f"  ✓ {len(CLIENTS)} nós Client criados")

    print("\n[Neo4j] Criando relacionamentos SELLS...")
    for ripperdoc_pk, cyberware_pk in SELLS:
        dbneo4j.connect_cyberware_ripperdoc(cyberware_pk, ripperdoc_pk)
    print(f"  ✓ {len(SELLS)} relações SELLS criadas")

    print("\n[Neo4j] Criando relacionamentos BOUGHT...")
    for client_pk, ripperdoc_pk, cyberware_pk in PURCHASES:
        dbneo4j.connect_cyberware_ripperdoc_client(cyberware_pk, ripperdoc_pk, client_pk)
    print(f"  ✓ {len(PURCHASES)} relações BOUGHT criadas")

def seed_cassandra():
    print("\n[Cassandra] Inserindo chaves primárias...")

    for cw in CYBERWARES:
        dbcassandra.create("cyberware", cw["pk"])

    print(f"  ✓ {len(CYBERWARES)} cyberwares inseridos")

    for rd in RIPPERDOCS:
        dbcassandra.create("ripperdoc", rd["pk"])

    print(f"  ✓ {len(RIPPERDOCS)} ripperdocs inseridos")

    for cl in CLIENTS:
        dbcassandra.create("client", cl["pk"])

    print(f"  ✓ {len(CLIENTS)} clientes inseridos")

def drop_all():
    print("\n[!] Dropando bancos...")
    dbmongo.drop_all()
    print("  ✓ MongoDB dropado")
    dbneo4j.drop_all()
    print("  ✓ Neo4j dropado")
    dbcassandra.drop_all
    print("  ✓ Cassandra dropado")

# ── Entrypoint ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    args = sys.argv[1:]

    drop_all()

    seed_mongodb()
    seed_neo4j()
    seed_cassandra()

    dbneo4j.close()
    print("\n[✓] Seed concluído.\n")
from cyberware_entity import Cyberware
from ripperdoc_entity import Ripperdoc
from client_entity import Client

def create_cyberware():
    name = input("Name: ")
    corp = input("Provider: ")
    pk = input("Primary Key: ")
    price = input("Base Price ")
    part = input("Body Part:")
    danger = input("Danger Level: ")
    cyberware = Cyberware(name, corp, pk, price, part, danger)
    pass

def create_ripperdoc():
    name = input("Name: ")
    pk = input("Primary Key: ")
    region = input("Working Region: ")
    price = input("Base Price: ")
    ripperdoc = Ripperdoc(name, pk, region, price)
    pass

def create_client():
    name = input("Name: ")
    pk = input("Primary Key: ")
    tolerance = input("Psycho Tolerance: ")
    client = Client(name, pk, tolerance)
    pass

def connect_cyberware_ripperdoc():
    cyberware_name = input("Cyberware Primary Key: ")
    ripperdoc_pk = input("Ripperdoc Primary Key: ")
    pass

def connect_cyberware_ripperdoc_client():
    cyberware_name = input("Cyberware Primary Key: ")
    ripperdoc_pk = input("Ripperdoc Primary Key: ")
    client_pk = input("Client Primary Key: ")
    pass

def main():
    opt = -1

    while opt != 0:
        print("0- Exit")
        print("1- Register a Cyberware")
        print("2- Register a Ripperdoc")
        print("3- Register a Client")
        opt = int(input("Chose a option: "))

        match opt:
            case 1:
                create_cyberware()
            case 2:
                create_ripperdoc()
            case 3:
                create_ripperdoc()
            case _:
                print("Invalid option")

if __name__ == "__main__":
    main()
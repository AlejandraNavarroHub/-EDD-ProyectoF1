# HASH Mode Package
# Released under MIT License
# Copyright (c) 2020 TytusDb Team


from storage import ListaBaseDatos as Storage, serealizar
import os, re, csv

storage = Storage.ListaBaseDatos()
main_path = os.getcwd()+"\\data\\hash"
db_name_pattern = "^[a-zA-Z][a-zA-Z0-9#@$_]*"


def setDir(newPath: str) -> int:

    global main_path
    temp_path = newPath+"\\data"

    try:
        if os.path.isdir(newPath):

            if not os.path.isdir(temp_path):
                os.mkdir(temp_path)

            main_path = temp_path
            Storage.main_path = temp_path

            __init__()

            return 0
        
        else:
            return 1

    except:
        return 1


# ==//== inicialización del sistema de directorios ==//==

def __init__():

    if not os.path.isdir(os.getcwd()+"\\data"):
        os.mkdir(os.getcwd()+"\\data")

    if not os.path.isdir(os.getcwd()+"\\data\\hash"):
        os.mkdir(os.getcwd()+"\\data\\hash")
        
    for db in os.listdir(main_path):
        storage.createDatabase(db)
        
__init__()

# ==//== funciones con respecto a ListaBaseDatos ==//==
# Se llama la función sobre la clase ListaBaseDatos

def createDatabase(database: str) -> int:

    try:
        
        if re.search(db_name_pattern, database):
            return storage.createDatabase(database)

        else:
            return 1

    except:
        return 1


def showDatabases() -> list:

    return storage.showDatabases()


def alterDatabase(databaseOld: str, databaseNew: str) -> int:

    if re.search(db_name_pattern, databaseOld) and re.search(db_name_pattern, databaseNew):
        return storage.alterDatabase(databaseOld, databaseNew)

    else:
        return 1


def dropDatabase(database: str) -> int:

    return storage.dropDatabase(database)


# ==//== funciones con respecto a BaseDatos ==//==
# Primero se busca la base de datos y luego se llama la función sobre la clase BaseDatos

def createTable(database: str, table: str, numberColumns: int) -> int:

    temp = storage.Buscar(database)

    if temp:
        return temp.createTable(table, numberColumns)

    else:
        return 2


def showTables(database: str) -> list:

    temp = storage.Buscar(database)

    if temp:
        return temp.showTables()

    else:
        return None


def extractTable(database: str, table: str) -> list:

    temp = storage.Buscar(database)

    if temp:
        return temp.extractTable(table)

    else:
        return None


def extractRangeTable(database: str, table: str, columnNumber: int, lower: any, upper: any) -> list:

    temp = storage.Buscar(database)

    if temp:
        return temp.extractRangeTable(table, columnNumber, lower, upper)

    else:
        return None


def alterAddPK(database: str, table: str, columns: list) -> int:

    temp = storage.Buscar(database)

    if temp:
        return temp.alterAddPK(table, columns)

    else:
        return 2


def alterDropPK(database: str, table: str) -> int:

    temp = storage.Buscar(database)

    if temp:
        return temp.alterDropPK(table)
        
    else:
        return 2


def alterAddFK(database: str, table: str, references: dict) -> int:

    print("codigo en proceso (FASE 2)")


def alterAddIndex(database: str, table: str, references: dict) -> int:

    print("codigo en proceso (FASE 2)")


def alterTable(database: str, tableOld: str, tableNew: str) -> int:

    temp = storage.Buscar(database)

    if temp:
        return temp.alterTable(tableOld, tableNew)

    else:
        return 2


def alterAddColumn(database:str, table:str, default: any) -> int:

    temp = storage.Buscar(database)

    if temp:
        return temp.alterAddColumn(table, default)

    else:
        return 2


def alterDropColumn(database: str, table: str, columnNumber: int) -> int:

    temp = storage.Buscar(database)

    if temp:
        return temp.alterDropColumn(table, columnNumber)

    else:
        return 2


def dropTable(database: str, table: str) -> int:

    temp = storage.Buscar(database)

    if temp:
        return temp.dropTable(table)

    else:
        return 2


# ==//== funciones con respecto a Tabla ==//==
# Primero se busca la base de datos, luego la tabla, y luego se llama la función sobre la clase Tabla

def insert(database: str, table: str, register: list) -> int:

    temp = storage.Buscar(database)

    if temp:

        b = temp.Buscar(table)        
        
        if b[0]:
            tabla = temp.Cargar(table)
            var = tabla.insertar(register)            
            temp.Guardar()
            return var

        else:
            return 3

    else:
        return 2


def loadCSV(file: str, database: str, table: str) -> list:

    try:
        archivo = open(file, "r")

    except:
        return []

    temp = storage.Buscar(database)

    if temp:
        
        try:

            b = temp.Buscar(table)        
            nombre = temp.list_table[b[1]]
            
            if b[0]:
                
                tabla = serealizar.rollback(nombre, main_path+"\\"+database)
                registros = csv.reader(archivo, delimiter = ",")
                valores=[]                

                for registro in registros:                       
                    valores.append(tabla.insertar(registro))

                else:
                    serealizar.commit(tabla, table, main_path+"\\"+database)
                    return valores

            else:
                return []

        except:
            return []

    else:
        return []
        

def extractRow(database: str, table: str, columns: list) -> list:

    temp = storage.Buscar(database)

    if temp:

        b = temp.Buscar(table)       
        
        if b[0]:
            tabla = temp.Cargar(table)
            var = tabla.ExtraerTupla(columns)            
            temp.Guardar()
            return var

        else:
            return []

    else:
        return []


def update(database: str, table: str, register: dict, columns: list) -> int:

    temp = storage.Buscar(database)

    if temp:

        b = temp.Buscar(table)

        if b[0]:
            tabla = temp.Cargar(table)
            var = tabla.update(columns, register)            
            temp.Guardar()
            return var

        else:
            return 3

    else:
        return 2


def delete(database: str, table: str, columns: list) -> int:

    temp = storage.Buscar(database)

    if temp:

        b = temp.Buscar(table)        

        if b[0]:
            tabla = temp.Cargar(table)
            var = tabla.deleteTable(columns)            
            temp.Guardar()
            return var

        else:
            return 3

    else:
        return 2


def truncate(database: str, table: str) -> int:

    temp = storage.Buscar(database)

    if temp:

        b = temp.Buscar(table)

        if b[0]:
            tabla = temp.Cargar(table)
            var = tabla.truncate()            
            temp.Guardar()
            return var

        else:
            return 3

    else:
        return 2
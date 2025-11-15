# AWS Free Tier Migration Scripts

Este repositorio contiene dos scripts pensados para facilitar la migración de referencias antiguas del Free Tier de AWS hacia el nuevo dominio `freetier.amazonaws.com`.

---

## 1. `search_billingconsole.py`  
Este script **debe ejecutarse primero**.  
Su función es recorrer todo el repositorio (desde la carpeta donde lo ejecutes hasta el final del árbol) y buscar coincidencias relacionadas con:

- `billingconsole.amazonaws.com`
- `freetier.amazonaws.com`
- `GetFreeTierUsage`

Cuando encuentra una coincidencia:

- Te muestra en pantalla el archivo, la línea y el contenido.  
- Guarda toda esa información en `report.json`.

Este reporte permite revisar previamente qué partes del repositorio cambiarían y comprobar si alguno de esos cambios podría afectar a tu infraestructura.

---

## 2. `replace_migration.py`  
El segundo script se encarga de **reemplazar** las coincidencias detectadas por las nuevas rutas asociadas al dominio `freetier.amazonaws.com`.

El funcionamiento es interactivo:  
por cada coincidencia encontrada, el script te preguntará si deseas modificar esa línea o no.  
De este modo puedes decidir, usando `report.json` como referencia, qué cambios quieres aplicar.

Además, **cada archivo que sea modificado generará automáticamente una copia de seguridad** con el nombre:


---

## Flujo recomendado

1. Ejecutar `search_billingconsole.py`  
2. Revisar `report.json`  
3. Ejecutar `replace_migration.py` y confirmar o rechazar cada cambio

---

Ambos scripts ignoran automáticamente `.git`, los propios scripts y los archivos JSON generados.


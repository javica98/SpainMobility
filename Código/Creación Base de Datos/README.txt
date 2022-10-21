Para la creación de la base de datos es necesario utilizar los archivos proporcionados.
Si se desea expandir o utilizar otros datos es necesario que los nuevos archivos tengan mismo nombre y variables que los propuestos.
Si no se tiene misma estructura de datos es necesario modificar las siguientes querys.
Se recomienda seguir el orden establecido en este README.

CREACIÓN DE BASE DE DATOS:

NODOS:

1-AEROPUERTOS:

LOAD CSV WITH HEADERS FROM 'file:///aeropuertos.csv' AS row
WITH row.AEROPUERTO AS aeropuertoId, row.DISTRITO AS distrito, row.DISTRITOID AS distritoId
MERGE (a:Aeropuerto {aeropuertoId: aeropuertoId})
  SET a.distritoId = distritoId, a.distrito = distrito
RETURN count(a);

2-DISTRITOS:

LOAD CSV WITH HEADERS FROM 'file:///Distritos.csv' AS row
WITH row.Provincia AS provincia, toInteger(row.Poblacion) AS poblacion, row.DistritoId AS distritoId, row.Distrito AS distrito, row.DistritoMunicipal AS distritoMunicipal,toInteger(row.PoblacionDistritoMunicipal) AS poblacionDistritoMunicipal
MERGE (a:Distrito {distritoId: distritoId})
  SET a.provincia = provincia, a.poblacion = poblacion, a.distrito = distrito, a.distritoMunicipal=distritoMunicipal,a.poblacionDistritoMunicipal=poblacionDistritoMunicipal
RETURN count(a);

3-MUNICIPIOS:

LOAD CSV WITH HEADERS FROM 'file:///Municipios.csv' AS row
WITH row.Municipio AS municipioId, row.DistritoId AS distritoId, toInteger(row.Poblacion) AS poblacion, row.ProvinciaId AS provinciaId
MERGE (a:Municipio {municipioId: municipioId})
  SET a.poblacion = poblacion, a.provinciaId = provinciaId
RETURN count(a);

4-PROVINCIAS:

LOAD CSV WITH HEADERS FROM 'file:///Provincias.csv' AS row
WITH row.ProvinciaId AS provinciaId, row.Provincia AS provincia,toInteger(row.Poblacion) AS poblacion
MERGE (a:Provincia {provinciaId: provinciaId})
  SET a.provincia = provincia, a.poblacion = poblacion
RETURN count(a);

5-DISTRITO SANITARIO:

LOAD CSV WITH HEADERS FROM 'file:///distritosSanitarios.csv' AS row
WITH row.DistritoSanitario AS distritoSanitarioId,toInteger(row.Poblacion)AS poblacion
MERGE (a:DistritoSanitario {distritoSanitarioId: distritoSanitarioId})
    SET a.poblacion=poblacion
RETURN count(a);

ARISTAS:

1-INCIDENCIA PROVINCIAS:

:auto USING PERIODIC COMMIT 500
LOAD CSV WITH HEADERS FROM 'file:///IncidenciaProvincias.csv' AS row
WITH date(row.Fecha) AS fecha,toFloat(row.Casos) AS casos,toFloat(row.Casos7) AS casos7,toFloat(row.Casos14) AS casos14, row.ProvinciaId AS provinciaId
MATCH (d:Provincia {provinciaId: provinciaId})
MATCH (m:Municipio {provinciaId: provinciaId})
MERGE (m)-[rel:IncidenciaProvincia {fecha: fecha,casos:casos,casos7:casos7,casos14:casos14}]->(d)
RETURN count(rel);

2-INCIDENCIA DISTRITOS SANITARIOS

:auto USING PERIODIC COMMIT 500
LOAD CSV WITH HEADERS FROM 'file:///IncidenciaDistritosSanitarios.csv' AS row
WITH date(row.Fecha) AS fecha,toFloat(row.Casos) AS casos,toFloat(row.Casos7) AS casos7,toFloat(row.Casos14) AS casos14, row.DistritoSanitario AS distritoSanitarioId, row.Municipio AS municipioId
MATCH (d:DistritoSanitario {distritoSanitarioId: distritoSanitarioId})
MATCH (m:Municipio {municipioId: municipioId})
MERGE (m)-[rel:IncidenciaDistritoSanitario {fecha: fecha,casos:casos,casos7:casos7,casos14:casos14}]->(d)
RETURN count(rel);

3-FORMADO POR:

:auto USING PERIODIC COMMIT 500
LOAD CSV WITH HEADERS FROM 'file:///Municipios.csv' AS row
WITH row.Municipio AS municipioId,row.DistritoId AS distritoId
MATCH (m:Municipio {municipioId: municipioId})
MATCH (d:Distrito {distritoId: distritoId})
MERGE (d)-[rel:FormadoPor ]->(m)
RETURN count(rel);

4-INCIDENCIA MUNICIPIOS:

:auto USING PERIODIC COMMIT 500
LOAD CSV WITH HEADERS FROM 'file:///incidenciaMunicipios.csv' AS row
WITH date(row.Fecha) AS fecha,toFloat(row.Casos) AS casos,toFloat(row.Casos7) AS casos7,toFloat(row.Casos14) AS casos14, row.Municipio AS  municipioId 
MATCH (d:Distrito)-[f:FormadoPor]->(m:Municipio {municipioId: municipioId})
MERGE (m)-[rel:IncidenciaMunicipio {fecha: fecha,casos:casos,casos7:casos7,casos14:casos14}]->(d)
RETURN count(rel);

5-MOVILIDAD:

:auto USING PERIODIC COMMIT 500
LOAD CSV WITH HEADERS FROM 'file:///Movilidad.csv' AS row
WITH row.Origen AS origen,row.Destino AS destino, toInteger(row.Flujo) AS flujo, date(row.Fecha) AS fecha
MATCH (a:Aeropuerto {distritoId: destino})
MATCH (d:Distrito {distritoId: origen})
MERGE (d)-[rel:Movilidad{flujo:flujo,fecha:fecha} ]->(a)
RETURN count(rel);

6-INICIDENCIA DISTRITO MUNICIPAL:

:auto USING PERIODIC COMMIT 500
LOAD CSV WITH HEADERS FROM 'file:///incidenciaMunicipios.csv' AS row
WITH date(row.Fecha) AS fecha,toFloat(row.Casos) AS casos,toFloat(row.Casos7) AS casos7,toFloat(row.Casos14) AS casos14, row.Municipio AS  municipioId 
MATCH (d:Distrito{distritoMunicipal:municipioId})-[f:FormadoPor]->(m:Municipio)
MERGE (m)-[rel:IncidenciaDistritoMunicipal {fecha: fecha,casos:casos,casos7:casos7,casos14:casos14}]->(d)
RETURN count(rel);

7-EXPANSION

:auto USING PERIODIC COMMIT 500
LOAD CSV WITH HEADERS FROM 'file:///Expansion.csv' AS row
WITH row.Origen AS origen,row.Destino AS destino, toInteger(row.Flujo) AS flujo, date(row.Fecha) AS fecha
MATCH (a:Aeropuerto {distritoId: origen})
MATCH (d:Distrito {distritoId: destino})
MERGE (a)-[rel:Expansion{flujo:flujo,fecha:fecha} ]->(d)
RETURN count(rel);

8-INCIDENCIA PROVINCIASEXP:

:auto USING PERIODIC COMMIT 500
LOAD CSV WITH HEADERS FROM 'file:///IncidenciaProvinciasExp.csv' AS row
WITH date(row.Fecha) AS fecha,toFloat(row.Casos) AS casos,toFloat(row.Casos7) AS casos7,toFloat(row.Casos14) AS casos14, row.ProvinciaId AS provinciaId
MATCH (d:Provincia {provinciaId: provinciaId})
MATCH (m:Municipio {provinciaId: provinciaId})
MERGE (m)-[rel:IncidenciaProvinciaExp {fecha: fecha,casos:casos,casos7:casos7,casos14:casos14}]->(d)
RETURN count(rel);

9-INCIDENCIA MUNICIPIOSEXP:

:auto USING PERIODIC COMMIT 500
LOAD CSV WITH HEADERS FROM 'file:///incidenciaMunicipiosExp.csv' AS row
WITH date(row.Fecha) AS fecha,toFloat(row.Casos) AS casos,toFloat(row.Casos7) AS casos7,toFloat(row.Casos14) AS casos14, row.Municipio AS  municipioId 
MATCH (d:Distrito)-[f:FormadoPor]->(m:Municipio {municipioId: municipioId})
MERGE (m)-[rel:IncidenciaMunicipioExp {fecha: fecha,casos:casos,casos7:casos7,casos14:casos14}]->(d)
RETURN count(rel);

10-INICIDENCIA DISTRITO MUNICIPALEXP:

:auto USING PERIODIC COMMIT 500
LOAD CSV WITH HEADERS FROM 'file:///incidenciaMunicipiosExp.csv' AS row
WITH date(row.Fecha) AS fecha,toFloat(row.Casos) AS casos,toFloat(row.Casos7) AS casos7,toFloat(row.Casos14) AS casos14, row.Municipio AS  municipioId 
MATCH (d:Distrito{distritoMunicipal:municipioId})-[f:FormadoPor]->(m:Municipio)
MERGE (m)-[rel:IncidenciaDistritoMunicipalExp {fecha: fecha,casos:casos,casos7:casos7,casos14:casos14}]->(d)
RETURN count(rel);

11-RIESGOEXTERIOR:
CREATE (n:RiesgoExterior{nombre:riesgo})

12-RIESGOIMPORTADO:
:auto USING PERIODIC COMMIT 500
LOAD CSV WITH HEADERS FROM 'file:///Riesgo.csv' AS row
WITH row.Aeropuerto AS aeropuertoId, toFloat(row.RiesgoImportado) AS probCont, date(row.Fecha) AS fecha
MATCH (a:Aeropuerto {aeropuertoId: aeropuertoId})
MATCH (r:RiesgoExterior)
MERGE (r)-[rel:RiesgoImportado{probCont:probCont,fecha:fecha} ]->(a)
RETURN count(rel);
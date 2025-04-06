import sys
import os
from datetime import date
from sqlalchemy.orm import Session

# Añadir el directorio raíz del proyecto al path de Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal
from app.models.carrera import Carrera
from app.models.pensum import Pensum
from app.models.trimestre import Trimestre
from app.models.asignatura import Asignatura, AsignaturaTrimestre, prerequisito, corequisito


def import_sistemas():
    db = SessionLocal()
    
    try:
        # Crear carrera
        carrera = Carrera(
            nombre="Ingeniería en Sistemas",
            descripcion="Ingeniería en Sistemas de Información"
        )
        db.add(carrera)
        db.flush()  # Para obtener el ID de la carrera
        
        print(f"Carrera creada: {carrera.nombre} (ID: {carrera.id})")
        
        # Crear pensum
        pensum = Pensum(
            codigo="VERSION 2020 SIS",
            fecha_aprobacion=date(2023, 11, 2),
            resolucion="20231102-34/112",
            carrera_id=carrera.id
        )
        db.add(pensum)
        db.flush()  # Para obtener el ID del pensum
        
        print(f"Pensum creado: {pensum.codigo} (ID: {pensum.id})")
        
        # Crear los trimestres (1-14)
        trimestres = {}
        for i in range(1, 15):
            trimestre = Trimestre(
                numero=i,
                pensum_id=pensum.id
            )
            db.add(trimestre)
            trimestres[i] = trimestre
        
        db.flush()  # Para obtener los IDs de los trimestres
        
        print(f"Trimestres creados: {len(trimestres)}")
        
        # Diccionario para almacenar las asignaturas
        asignaturas = {}
        
        # Datos de las asignaturas del primer trimestre
        asignaturas_data = [
            # Trimestre 1
            {"codigo": "AHC109", "nombre": "REDACCION", "creditos": 4, "trimestre": 1},
            {"codigo": "AHO102", "nombre": "ORIENTACION ACADEMICA E INSTITUCIONAL", "creditos": 0, "trimestre": 1},
            {"codigo": "CBA1X3", "nombre": "VIDA EN EL MEDIO AMBIENTE (ELECTIVAS)", "creditos": 2, "trimestre": 1},
            {"codigo": "CBM101", "nombre": "ALGEBRA Y GEOMETRIA ANALITICA", "creditos": 5, "trimestre": 1},
            {"codigo": "CSH112", "nombre": "CIUDADANIA Y ETICA", "creditos": 2, "trimestre": 1},
            {"codigo": "EAA1X1", "nombre": "ELECTIVAS DE AREAS ACADEMICAS I", "creditos": 2, "trimestre": 1},
            {"codigo": "EAA1X2", "nombre": "ELECTIVAS DE AREAS ACADEMICAS II", "creditos": 2, "trimestre": 1},
            {"codigo": "INS211", "nombre": "INTRODUCCION A LA INGENIERIA DE SISTEMAS", "creditos": 3, "trimestre": 1},
            {"codigo": "SHI103", "nombre": "INGLES 01 (BASICO I)", "creditos": 0, "trimestre": 1},
            
            # Trimestre 2
            {"codigo": "AHC110", "nombre": "ARGUMENTACIÓN LINGÜÍSTICA", "creditos": 4, "trimestre": 2, "prerequisitos": ["AHC109"]},
            {"codigo": "CBM102", "nombre": "CALCULO DIFERENCIAL", "creditos": 5, "trimestre": 2, "prerequisitos": ["CBM101"]},
            {"codigo": "CSS102", "nombre": "SER HUMANO Y SOCIEDAD: TEMAS SOCIALES CONTEMPORANEOS", "creditos": 2, "trimestre": 2},
            {"codigo": "EAA1X3", "nombre": "ELECTIVAS DE AREAS ACADEMICAS III", "creditos": 2, "trimestre": 2},
            {"codigo": "ING102", "nombre": "INTRODUCCION A LA PROGRAMACION", "creditos": 2, "trimestre": 2, "prerequisitos": ["CBM101"], "corequisitos": ["ING102L"]},
            {"codigo": "ING102L", "nombre": "LABORATORIO DE INTRODUCCION A LA PROGRAMACION", "creditos": 0, "trimestre": 2, "prerequisitos": ["CBM101"], "corequisitos": ["ING102"]},
            {"codigo": "INS210", "nombre": "FUNDAMENTOS DE TI", "creditos": 4, "trimestre": 2, "prerequisitos": ["INS211"]},
            {"codigo": "SHI104", "nombre": "INGLES 02 (BASICO II)", "creditos": 0, "trimestre": 2, "prerequisitos": ["SHI103"]},
            
            # Trimestre 3
            {"codigo": "CBF210", "nombre": "FISICA MECANICA I", "creditos": 4, "trimestre": 3, "prerequisitos": ["CBM102"], "corequisitos": ["CBM201"]},
            {"codigo": "CBF210L", "nombre": "LABORATORIO DE FISICA MECANICA I", "creditos": 1, "trimestre": 3, "prerequisitos": ["CBM102"], "corequisitos": ["CBF210"]},
            {"codigo": "CBM201", "nombre": "CALCULO INTEGRAL", "creditos": 5, "trimestre": 3, "prerequisitos": ["CBM102"]},
            {"codigo": "IDS202", "nombre": "TECNOLOGIA DE OBJETOS", "creditos": 4, "trimestre": 3, "prerequisitos": ["ING102", "ING102L"]},
            {"codigo": "IDS202L", "nombre": "LABORATORIO TECNOLOGIA DE OBJETOS", "creditos": 1, "trimestre": 3, "prerequisitos": ["ING102", "ING102L"], "corequisitos": ["IDS202"]},
            {"codigo": "IDS340", "nombre": "DESARROLLO DE SOFTWARE I", "creditos": 3, "trimestre": 3, "prerequisitos": ["ING102", "ING102L"]},
            {"codigo": "IDS340L", "nombre": "LABORATORIO DE DESARROLLO DE SOFTWARE I", "creditos": 1, "trimestre": 3, "prerequisitos": ["ING102", "ING102L"], "corequisitos": ["IDS340"]},
            {"codigo": "ING228", "nombre": "HOJA DE CALCULO PARA INGENIEROS", "creditos": 1, "trimestre": 3, "prerequisitos": ["ING102", "ING102L"]},
            {"codigo": "SHI105", "nombre": "INGLES 03 (INTERMEDIO I)", "creditos": 0, "trimestre": 3, "prerequisitos": ["SHI104"]},
            
            # Trimestre 4
            {"codigo": "AHQ101", "nombre": "QUEHACER CIENTIFICO", "creditos": 4, "trimestre": 4},
            {"codigo": "CBF211", "nombre": "FISICA MECANICA II", "creditos": 4, "trimestre": 4, "prerequisitos": ["CBF210", "CBM201", "CBF210L"]},
            {"codigo": "CBF211L", "nombre": "LABORATORIO DE FISICA MECANICA II", "creditos": 1, "trimestre": 4, "prerequisitos": ["CBF210", "CBM201", "CBF210L"], "corequisitos": ["CBF211"]},
            {"codigo": "CBM202", "nombre": "CALCULO VECTORIAL", "creditos": 5, "trimestre": 4, "prerequisitos": ["CBM201"]},
            {"codigo": "EAA1X4", "nombre": "ELECTIVAS DE AREAS ACADEMICAS IV", "creditos": 2, "trimestre": 4},
            {"codigo": "IDS341", "nombre": "DESARROLLO DE SOFTWARE II", "creditos": 3, "trimestre": 4, "prerequisitos": ["IDS340", "IDS340L"]},
            {"codigo": "IDS341L", "nombre": "LABORATORIO DE DESARROLLO DE SOFTWARE II", "creditos": 1, "trimestre": 4, "prerequisitos": ["IDS340", "IDS340L"], "corequisitos": ["IDS341"]},
            {"codigo": "INS219", "nombre": "CONSEJERIA INGENIERIA SISTEMAS I", "creditos": 0, "trimestre": 4, "req_creditos": 35},
            {"codigo": "SHI106", "nombre": "INGLES 04 (INTERMEDIO II)", "creditos": 0, "trimestre": 4, "prerequisitos": ["SHI105"]},

            # Trimestre 5
            {"codigo": "CBM208", "nombre": "ALGEBRA LINEAL", "creditos": 5, "trimestre": 5, "prerequisitos": ["CBM202"]},
            {"codigo": "CSH113", "nombre": "PENSAMIENTO CREATIVO", "creditos": 2, "trimestre": 5},
            {"codigo": "IDS324", "nombre": "INGENIERIA DE REQUERIMIENTOS DE SOFTWARE", "creditos": 4, "trimestre": 5, "prerequisitos": ["IDS202", "IDS202L"]},
            {"codigo": "IDS324L", "nombre": "LABORATORIO INGENIERIA DE REQUERIMIENTOS DE SOFTWARE", "creditos": 1, "trimestre": 5, "prerequisitos": ["IDS202", "IDS202L"], "corequisitos": ["IDS324"]},
            {"codigo": "IDS343", "nombre": "ESTRUCTURAS DE DATOS Y ALGORITMOS I", "creditos": 3, "trimestre": 5, "prerequisitos": ["IDS340", "IDS340L"]},
            {"codigo": "IDS343L", "nombre": "LABORATORIO ESTRUCTURAS DE DATOS Y ALGORITMOS I", "creditos": 1, "trimestre": 5, "prerequisitos": ["IDS340", "IDS340L"], "corequisitos": ["IDS343"]},
            {"codigo": "INS216", "nombre": "FUNDAMENTOS DE SISTEMAS DE INFORMACION", "creditos": 4, "trimestre": 5, "prerequisitos": ["INS210"]},
            {"codigo": "SHI107", "nombre": "INGLES 05 (AVANZADO I)", "creditos": 0, "trimestre": 5, "prerequisitos": ["SHI106"]},

            # Trimestre 6
            {"codigo": "CBM203", "nombre": "ECUACIONES DIFERENCIALES", "creditos": 5, "trimestre": 6, "prerequisitos": ["CBM208"]},
            {"codigo": "CSH105", "nombre": "PROYECTO INTEGRADOR DE ESTUDIOS GENERALES", "creditos": 2, "trimestre": 6, "req_creditos": 40},
            {"codigo": "EEE2X1", "nombre": "ELECTIVAS DE ESTUDIOS ESPECIALIZADOS I", "creditos": 0, "trimestre": 6},
            {"codigo": "IDS344", "nombre": "ESTRUCTURAS DE DATOS Y ALGORITMOS II", "creditos": 3, "trimestre": 6, "prerequisitos": ["IDS343", "IDS343L"]},
            {"codigo": "IDS344L", "nombre": "LABORATORIO ESTRUCTURAS DE DATOS Y ALGORITMOS II", "creditos": 1, "trimestre": 6, "prerequisitos": ["IDS343", "IDS343L"], "corequisitos": ["IDS344"]},
            {"codigo": "INS377", "nombre": "BASES DE DATOS I", "creditos": 4, "trimestre": 6, "prerequisitos": ["IDS324", "IDS343", "IDS324L", "IDS343L"]},
            {"codigo": "INS377L", "nombre": "LABORATORIO BASES DE DATOS I", "creditos": 1, "trimestre": 6, "prerequisitos": ["IDS343", "IDS343L", "IDS324", "IDS324L"], "corequisitos": ["INS377"]},
            {"codigo": "SHI108", "nombre": "INGLES 06 (AVANZADO II)", "creditos": 0, "trimestre": 6, "prerequisitos": ["SHI107"]},

            # Trimestre 7
            {"codigo": "ICS202", "nombre": "ALGORITMOS MALICIOSOS", "creditos": 4, "trimestre": 7, "prerequisitos": ["IDS343", "IDS343L"]},
            {"codigo": "ICS202L", "nombre": "LABORATORIO DE ALGORITMOS MALICIOSOS", "creditos": 1, "trimestre": 7, "prerequisitos": ["IDS343", "IDS343L"], "corequisitos": ["ICS202"]},
            {"codigo": "IDS345", "nombre": "DESARROLLO DE SOFTWARE III", "creditos": 3, "trimestre": 7, "prerequisitos": ["IDS341", "IDS341L", "INS377", "INS377L"]},
            {"codigo": "IDS345L", "nombre": "LABORATORIO DE DESARROLLO DE SOFTWARE III", "creditos": 1, "trimestre": 7, "prerequisitos": ["IDS341", "IDS341L", "INS377", "INS377L"], "corequisitos": ["IDS345"]},
            {"codigo": "IEC208", "nombre": "FUNDAMENTOS ELECTRÓNICA DIGITAL", "creditos": 3, "trimestre": 7, "prerequisitos": ["CBF211", "CBF211L"]},
            {"codigo": "IEC208L", "nombre": "LABORATORIO FUNDAMENTOS ELECTRÓNICA DIGITAL", "creditos": 1, "trimestre": 7, "prerequisitos": ["CBF211", "CBF211L"], "corequisitos": ["IEC208"]},
            {"codigo": "ING214", "nombre": "ANALISIS DE DATOS EN INGENIERIA", "creditos": 4, "trimestre": 7, "prerequisitos": ["CBM201"]},
            {"codigo": "INS380", "nombre": "BASES DE DATOS II", "creditos": 4, "trimestre": 7, "prerequisitos": ["INS377", "INS377L"]},
            {"codigo": "INS380L", "nombre": "LABORATORIO DE BASES DE DATOS II", "creditos": 1, "trimestre": 7, "prerequisitos": ["INS377", "INS377L"], "corequisitos": ["INS380"]},

            # Trimestre 8
            {"codigo": "EEE2X2", "nombre": "ELECTIVAS DE ESTUDIOS ESPECIALIZADOS II", "creditos": 0, "trimestre": 8},
            {"codigo": "IDS347", "nombre": "TENDENCIAS EN DESARROLLO DE SOFTWARE", "creditos": 3, "trimestre": 8, "prerequisitos": ["IDS345", "IDS345L"]},
            {"codigo": "IDS347L", "nombre": "LABORATORIO TENDENCIAS EN DESARROLLO DE SOFTWARE", "creditos": 1, "trimestre": 8, "prerequisitos": ["IDS345", "IDS345L"], "corequisitos": ["IDS347"]},
            {"codigo": "ING230", "nombre": "INGENIERIA ECONOMICA", "creditos": 4, "trimestre": 8, "prerequisitos": ["CBM202"]},
            {"codigo": "ING231", "nombre": "EXPERIMENTACION EN INGENIERIA", "creditos": 3, "trimestre": 8, "prerequisitos": ["AHQ101", "ING214"]},
            {"codigo": "INS371", "nombre": "ARQUITECTURA DEL COMPUTADOR", "creditos": 3, "trimestre": 8, "prerequisitos": ["IEC208", "IEC208L"]},
            {"codigo": "INS371L", "nombre": "LABORATORIO ARQUITECTURA COMPUTADOR", "creditos": 1, "trimestre": 8, "prerequisitos": ["IEC208", "IEC208L"], "corequisitos": ["INS371"]},
            {"codigo": "ISE2E1", "nombre": "IMPACTO SOCIAL (ELECTIVA)", "creditos": 4, "trimestre": 8},

            # Trimestre 9
            {"codigo": "CON213", "nombre": "FUNDAMENTOS DE CONTABILIDAD", "creditos": 2, "trimestre": 9, "req_creditos": 100},
            {"codigo": "ICS320", "nombre": "FUNDAMENTOS DE CIBERSEGURIDAD", "creditos": 2, "trimestre": 9, "prerequisitos": ["INS371", "INS371L"]},
            {"codigo": "ING235", "nombre": "FORMULACION Y GESTION DE PROYECTOS TECNOLOGICOS", "creditos": 4, "trimestre": 9, "prerequisitos": ["ING231", "ING230"]},
            {"codigo": "ING235L", "nombre": "LABORATORIO FORMULACION Y GESTION DE PROYECTOS TECNOLOGICOS", "creditos": 1, "trimestre": 9, "prerequisitos": ["ING231", "ING230"], "corequisitos": ["ING235"]},
            {"codigo": "INS324", "nombre": "ANALISIS Y DISEÑO DE SISTEMAS", "creditos": 4, "trimestre": 9, "prerequisitos": ["INS377", "INS377L"]},
            {"codigo": "INS373", "nombre": "SISTEMAS OPERATIVOS", "creditos": 4, "trimestre": 9, "prerequisitos": ["INS371", "INS371L"]},
            {"codigo": "INS373L", "nombre": "LABORATORIO SISTEMAS OPERATIVOS", "creditos": 1, "trimestre": 9, "prerequisitos": ["INS371", "INS371L"], "corequisitos": ["INS373"]},

            # Trimestre 10
            {"codigo": "ECO322", "nombre": "ECONOMIA DE EMPRESA", "creditos": 4, "trimestre": 10, "prerequisitos": ["ING230"]},
            {"codigo": "INS376", "nombre": "COMUNICACION DE DATOS I", "creditos": 4, "trimestre": 10, "prerequisitos": ["INS373", "INS373L"]},
            {"codigo": "INS376L", "nombre": "LABORATORIO COMUNICACION DE DATOS I", "creditos": 1, "trimestre": 10, "prerequisitos": ["INS373", "INS373L"], "corequisitos": ["INS376"]},
            {"codigo": "INS382", "nombre": "GESTION DE TI-SEGURIDAD Y RIESGOS", "creditos": 4, "trimestre": 10, "prerequisitos": ["ICS320"]},
            {"codigo": "INS388", "nombre": "MINERIA DE DATOS", "creditos": 4, "trimestre": 10, "prerequisitos": ["INS380", "INS380L"]},
            {"codigo": "SIS307", "nombre": "ETICA PROFESIONAL INGENIERIA DE SISTEMAS", "creditos": 2, "trimestre": 10, "req_creditos": 100},

            # Trimestre 11
            {"codigo": "INS335", "nombre": "SEMINARIO DE TECNOLOGIA", "creditos": 4, "trimestre": 11, "prerequisitos": ["ING235"]},
            {"codigo": "INS369", "nombre": "INTELIGENCIA DE NEGOCIOS", "creditos": 4, "trimestre": 11, "prerequisitos": ["INS388"]},
            {"codigo": "INS379", "nombre": "COMUNICACION DE DATOS II", "creditos": 4, "trimestre": 11, "prerequisitos": ["INS376", "INS376L"]},
            {"codigo": "INS379L", "nombre": "LABORATORIO COMUNICACION DE DATOS II", "creditos": 1, "trimestre": 11, "prerequisitos": ["INS376", "INS376L"], "corequisitos": ["INS379"]},
            {"codigo": "INS384", "nombre": "GESTION DE TI - AUDITORIAS Y CONTROLES", "creditos": 4, "trimestre": 11, "prerequisitos": ["INS382"]},
            {"codigo": "SIS301", "nombre": "CONSEJERIA PROFESIONAL INGENIERIA SISTEMAS", "creditos": 0, "trimestre": 11, "prerequisitos": ["INS219"]},
            {"codigo": "SIS302", "nombre": "PASANTIA PROFESIONAL I", "creditos": 2, "trimestre": 11, "req_creditos": 160},

            # Trimestre 12
            {"codigo": "EEP3X1", "nombre": "ELECTIVAS DE ESTUDIOS PROFESIONALIZANTES I", "creditos": 0, "trimestre": 12},
            {"codigo": "ICS319", "nombre": "ETHICAL HACKING", "creditos": 4, "trimestre": 12, "prerequisitos": ["ICS320"]},
            {"codigo": "ICS319L", "nombre": "LABORATORIO ETHICAL HACKING", "creditos": 1, "trimestre": 12, "prerequisitos": ["ICS320"], "corequisitos": ["ICS319"]},
            {"codigo": "INS381", "nombre": "COMUNICACION DE DATOS III", "creditos": 4, "trimestre": 12, "prerequisitos": ["INS379L", "INS379"]},
            {"codigo": "INS381L", "nombre": "LABORATORIO COMUNICACION DE DATOS III", "creditos": 1, "trimestre": 12, "prerequisitos": ["INS379", "INS379L"], "corequisitos": ["INS381"]},
            {"codigo": "SIS303", "nombre": "ANTE-PROYECTO DE GRADO", "creditos": 4, "trimestre": 12, "prerequisitos": ["INS335"]},
            {"codigo": "SIS304", "nombre": "PASANTIA PROFESIONAL II", "creditos": 2, "trimestre": 12, "req_creditos": 160},

            # Trimestre 13
            {"codigo": "ADM315", "nombre": "ADMINISTRACION Y GESTION EMPRESARIAL", "creditos": 4, "trimestre": 13, "req_creditos": 160},
            {"codigo": "EEP3X2", "nombre": "ELECTIVAS DE ESTUDIOS PROFESIONALIZANTES II", "creditos": 0, "trimestre": 13},
            {"codigo": "IDS339", "nombre": "DEVOPS Y DEVSECOPS", "creditos": 3, "trimestre": 13, "prerequisitos": ["ICS320", "INS373", "INS373L"]},
            {"codigo": "INS348", "nombre": "GOBERNABILIDAD DE TECNOLOGIA DE LA INFORMACION", "creditos": 4, "trimestre": 13, "prerequisitos": ["INS384"]},
            {"codigo": "SIS305", "nombre": "PROYECTO DE GRADO", "creditos": 4, "trimestre": 13, "prerequisitos": ["SIS303"], "req_creditos": 180},

            # Trimestre 14
            {"codigo": "EEP3X3", "nombre": "ELECTIVAS DE ESTUDIOS PROFESIONALIZANTES III", "creditos": 0, "trimestre": 14},
            {"codigo": "INS342", "nombre": "TECNOLOGIAS DE INFORMACION EMERGENTE", "creditos": 4, "trimestre": 14, "req_creditos": 200},
            {"codigo": "INS389", "nombre": "ADMINISTRACION ESTRATEGICA DE TIC", "creditos": 4, "trimestre": 14, "prerequisitos": ["ADM315"]},
            {"codigo": "SIS306", "nombre": "PROYECTO FINAL DE GRADO", "creditos": 4, "trimestre": 14, "prerequisitos": ["SIS305"]}
        ]
        
        # Crear asignaturas
        for asig_data in asignaturas_data:
            asignatura = Asignatura(
                codigo=asig_data["codigo"],
                nombre=asig_data["nombre"],
                creditos=asig_data["creditos"],
                req_creditos=asig_data.get("req_creditos", None)
            )
            db.add(asignatura)
            db.flush()
            asignaturas[asig_data["codigo"]] = asignatura
            
            # Crear relación con el trimestre
            asig_trimestre = AsignaturaTrimestre(
                asignatura_id=asignatura.id,
                trimestre_id=trimestres[asig_data["trimestre"]].id
            )
            db.add(asig_trimestre)
        
        db.flush()
        
        # Establecer prerequisitos y corequisitos
        for asig_data in asignaturas_data:
            if "prerequisitos" in asig_data:
                for pre_code in asig_data["prerequisitos"]:
                    asignatura = asignaturas[asig_data["codigo"]]
                    prerequisito_asig = asignaturas[pre_code]
                    asignatura.prerequisitos.append(prerequisito_asig)
            
            if "corequisitos" in asig_data:
                for co_code in asig_data["corequisitos"]:
                    asignatura = asignaturas[asig_data["codigo"]]
                    corequisito_asig = asignaturas[co_code]
                    asignatura.corequisitos.append(corequisito_asig)
        
        db.commit()
        print(f"Asignaturas importadas: {len(asignaturas)}")
        print("Importación de Ingeniería en Sistemas completada con éxito.")
        
    except Exception as e:
        db.rollback()
        print(f"Error durante la importación de Ingeniería en Sistemas: {e}")
        raise
    finally:
        db.close()


def import_software():
    db = SessionLocal()
    
    try:
        # Crear carrera
        carrera = Carrera(
            nombre="Ingeniería Software",
            descripcion="Ingeniería en Software"
        )
        db.add(carrera)
        db.flush()  # Para obtener el ID de la carrera
        
        print(f"Carrera creada: {carrera.nombre} (ID: {carrera.id})")
        
        # Crear pensum
        pensum = Pensum(
            codigo="VERSION 2020 IDS",
            fecha_aprobacion=date(2023, 11, 2),
            resolucion="20231102-34/112",
            carrera_id=carrera.id
        )
        db.add(pensum)
        db.flush()  # Para obtener el ID del pensum
        
        print(f"Pensum creado: {pensum.codigo} (ID: {pensum.id})")
        
        # Crear los trimestres (1-14)
        trimestres = {}
        for i in range(1, 15):
            trimestre = Trimestre(
                numero=i,
                pensum_id=pensum.id
            )
            db.add(trimestre)
            trimestres[i] = trimestre
        
        db.flush()  # Para obtener los IDs de los trimestres
        
        print(f"Trimestres creados: {len(trimestres)}")
        
        # Diccionario para almacenar las asignaturas
        asignaturas = {}
        
        # Datos de las asignaturas del pensum de Ingeniería Software
        asignaturas_data = [
            # Trimestre 1
            {"codigo": "AHC109", "nombre": "REDACCION", "creditos": 4, "trimestre": 1},
            {"codigo": "AHO102", "nombre": "ORIENTACION ACADEMICA E INSTITUCIONAL", "creditos": 0, "trimestre": 1},
            {"codigo": "CBA1X3", "nombre": "VIDA EN EL MEDIO AMBIENTE (ELECTIVAS)", "creditos": 2, "trimestre": 1},
            {"codigo": "CBM101", "nombre": "ALGEBRA Y GEOMETRIA ANALITICA", "creditos": 5, "trimestre": 1},
            {"codigo": "CSH112", "nombre": "CIUDADANIA Y ETICA", "creditos": 2, "trimestre": 1},
            {"codigo": "EAA1X1", "nombre": "ELECTIVAS DE AREAS ACADEMICAS I", "creditos": 2, "trimestre": 1},
            {"codigo": "EAA1X2", "nombre": "ELECTIVAS DE AREAS ACADEMICAS II", "creditos": 2, "trimestre": 1},
            {"codigo": "EAA1X3", "nombre": "ELECTIVAS DE AREAS ACADEMICAS III", "creditos": 2, "trimestre": 1},
            {"codigo": "IDS207", "nombre": "INTRODUCCION A LA INGENIERIA DE SOFTWARE", "creditos": 2, "trimestre": 1},
            {"codigo": "SHI103", "nombre": "INGLES 01 (BASICO I)", "creditos": 0, "trimestre": 1},
            
            # Trimestre 2
            {"codigo": "AHC110", "nombre": "ARGUMENTACIÓN LINGÜÍSTICA", "creditos": 4, "trimestre": 2, "prerequisitos": ["AHC109"]},
            {"codigo": "CBM102", "nombre": "CALCULO DIFERENCIAL", "creditos": 5, "trimestre": 2, "prerequisitos": ["CBM101"]},
            {"codigo": "CSS102", "nombre": "SER HUMANO Y SOCIEDAD: TEMAS SOCIALES CONTEMPORANEOS", "creditos": 2, "trimestre": 2},
            {"codigo": "EAA1X4", "nombre": "ELECTIVAS DE AREAS ACADEMICAS IV", "creditos": 2, "trimestre": 2},
            {"codigo": "IDS323", "nombre": "TECNICAS FUNDAMENTALES DE INGENIERIA DE SOFTWARE", "creditos": 4, "trimestre": 2, "prerequisitos": ["IDS207"]},
            {"codigo": "IDS323L", "nombre": "LABORATORIO TECNICAS FUNDAMENTALES DE INGENIERIA DE SOFTWARE", "creditos": 1, "trimestre": 2, "prerequisitos": ["IDS207"], "corequisitos": ["IDS323"]},
            {"codigo": "ING102", "nombre": "INTRODUCCION A LA PROGRAMACION", "creditos": 2, "trimestre": 2, "prerequisitos": ["CBM101"]},
            {"codigo": "ING102L", "nombre": "LABORATORIO DE INTRODUCCION A LA PROGRAMACION", "creditos": 0, "trimestre": 2, "prerequisitos": ["CBM101"], "corequisitos": ["ING102"]},
            {"codigo": "SHI104", "nombre": "INGLES 02 (BASICO II)", "creditos": 0, "trimestre": 2, "prerequisitos": ["SHI103"]},
            
            # Trimestre 3
            {"codigo": "CBF210", "nombre": "FISICA MECANICA I", "creditos": 4, "trimestre": 3, "prerequisitos": ["CBM102"], "corequisitos": ["CBM201"]},
            {"codigo": "CBF210L", "nombre": "LABORATORIO DE FISICA MECANICA I", "creditos": 1, "trimestre": 3, "prerequisitos": ["CBM102"], "corequisitos": ["CBF210"]},
            {"codigo": "CBM201", "nombre": "CALCULO INTEGRAL", "creditos": 5, "trimestre": 3, "prerequisitos": ["CBM102"]},
            {"codigo": "IDS202", "nombre": "TECNOLOGIA DE OBJETOS", "creditos": 4, "trimestre": 3, "prerequisitos": ["ING102", "ING102L"]},
            {"codigo": "IDS202L", "nombre": "LABORATORIO TECNOLOGIA DE OBJETOS", "creditos": 1, "trimestre": 3, "prerequisitos": ["ING102", "ING102L"], "corequisitos": ["IDS202"]},
            {"codigo": "IDS340", "nombre": "DESARROLLO DE SOFTWARE I", "creditos": 3, "trimestre": 3},
            {"codigo": "IDS340L", "nombre": "LABORATORIO DE DESARROLLO DE SOFTWARE I", "creditos": 1, "trimestre": 3, "prerequisitos": ["ING102", "ING102L"], "corequisitos": ["IDS340"]},
            {"codigo": "ING228", "nombre": "HOJA DE CALCULO PARA INGENIEROS", "creditos": 1, "trimestre": 3, "prerequisitos": ["ING102", "ING102L"]},
            {"codigo": "SHI105", "nombre": "INGLES 03 (INTERMEDIO I)", "creditos": 0, "trimestre": 3, "prerequisitos": ["SHI104"]},
            
            # Trimestre 4
            {"codigo": "AHQ101", "nombre": "QUEHACER CIENTIFICO", "creditos": 4, "trimestre": 4},
            {"codigo": "CBF211", "nombre": "FISICA MECANICA II", "creditos": 4, "trimestre": 4, "prerequisitos": ["CBF210", "CBM201", "CBF210L"]},
            {"codigo": "CBF211L", "nombre": "LABORATORIO DE FISICA MECANICA II", "creditos": 1, "trimestre": 4, "prerequisitos": ["CBF210", "CBM201", "CBF210L"], "corequisitos": ["CBF211"]},
            {"codigo": "CBM202", "nombre": "CALCULO VECTORIAL", "creditos": 5, "trimestre": 4, "prerequisitos": ["CBM201"]},
            {"codigo": "CSH113", "nombre": "PENSAMIENTO CREATIVO", "creditos": 2, "trimestre": 4},
            {"codigo": "IDS341", "nombre": "DESARROLLO DE SOFTWARE II", "creditos": 3, "trimestre": 4, "prerequisitos": ["IDS340", "IDS340L"]},
            {"codigo": "IDS341L", "nombre": "LABORATORIO DE DESARROLLO DE SOFTWARE II", "creditos": 1, "trimestre": 4, "prerequisitos": ["IDS340", "IDS340L"], "corequisitos": ["IDS341"]},
            {"codigo": "IDS342", "nombre": "CONSEJERIA PROFESIONAL INGENIERIA DE SOFTWARE I", "creditos": 0, "trimestre": 4, "req_creditos": 35},
            {"codigo": "SHI106", "nombre": "INGLES 04 (INTERMEDIO II)", "creditos": 0, "trimestre": 4, "prerequisitos": ["SHI104"]},
            
            # Trimestre 5
            {"codigo": "CBM208", "nombre": "ALGEBRA LINEAL", "creditos": 5, "trimestre": 5, "prerequisitos": ["CBM202"]},
            {"codigo": "IDS208", "nombre": "TEAM BUILDING", "creditos": 4, "trimestre": 5},
            {"codigo": "IDS311", "nombre": "PROCESO DE SOFTWARE", "creditos": 4, "trimestre": 5, "prerequisitos": ["IDS323", "IDS323L"]},
            {"codigo": "IDS324", "nombre": "INGENIERIA DE REQUERIMIENTOS DE SOFTWARE", "creditos": 4, "trimestre": 5, "prerequisitos": ["IDS202", "IDS202L"]},
            {"codigo": "IDS324L", "nombre": "LABORATORIO INGENIERIA DE REQUERIMIENTOS DE SOFTWARE", "creditos": 1, "trimestre": 5, "prerequisitos": ["IDS202", "IDS202L"], "corequisitos": ["IDS324"]},
            {"codigo": "IDS343", "nombre": "ESTRUCTURAS DE DATOS Y ALGORITMOS I", "creditos": 3, "trimestre": 5, "prerequisitos": ["IDS340", "IDS340L"]},
            {"codigo": "IDS343L", "nombre": "LABORATORIO ESTRUCTURAS DE DATOS Y ALGORITMOS I", "creditos": 1, "trimestre": 5, "prerequisitos": ["IDS340", "IDS340L"], "corequisitos": ["IDS343"]},
            {"codigo": "SHI107", "nombre": "INGLES 05 (AVANZADO I)", "creditos": 0, "trimestre": 5, "prerequisitos": ["SHI106"]},
            
            # Trimestre 6
            {"codigo": "CBM203", "nombre": "ECUACIONES DIFERENCIALES", "creditos": 5, "trimestre": 6, "prerequisitos": ["CBM208"]},
            {"codigo": "CSH105", "nombre": "PROYECTO INTEGRADOR DE ESTUDIOS GENERALES", "creditos": 2, "trimestre": 6, "req_creditos": 40},
            {"codigo": "IDS344", "nombre": "ESTRUCTURAS DE DATOS Y ALGORITMOS II", "creditos": 3, "trimestre": 6, "prerequisitos": ["IDS343", "IDS343L"]},
            {"codigo": "IDS344L", "nombre": "LABORATORIO ESTRUCTURAS DE DATOS Y ALGORITMOS II", "creditos": 1, "trimestre": 6, "prerequisitos": ["IDS343", "IDS343L"], "corequisitos": ["IDS344"]},
            {"codigo": "IEC208", "nombre": "FUNDAMENTOS ELECTRÓNICA DIGITAL", "creditos": 3, "trimestre": 6, "prerequisitos": ["CBF211", "CBF211L"]},
            {"codigo": "IEC208L", "nombre": "LABORATORIO FUNDAMENTOS ELECTRÓNICA DIGITAL", "creditos": 1, "trimestre": 6, "prerequisitos": ["CBF211", "CBF211L"], "corequisitos": ["IEC208"]},
            {"codigo": "INS377", "nombre": "BASES DE DATOS I", "creditos": 4, "trimestre": 6, "prerequisitos": ["IDS324", "IDS324L", "IDS343", "IDS343L"]},
            {"codigo": "INS377L", "nombre": "LABORATORIO BASES DE DATOS I", "creditos": 1, "trimestre": 6, "prerequisitos": ["IDS324", "IDS343", "IDS324L", "IDS343L"], "corequisitos": ["INS377"]},
            {"codigo": "SHI108", "nombre": "INGLES 06 (AVANZADO II)", "creditos": 0, "trimestre": 6, "prerequisitos": ["SHI107"]},
            
            # Trimestre 7
            {"codigo": "CBM305", "nombre": "MATEMATICA DISCRETA I", "creditos": 4, "trimestre": 7, "prerequisitos": ["CBM203"]},
            {"codigo": "IDS329", "nombre": "INGENIERIA DE FACTORES HUMANOS", "creditos": 4, "trimestre": 7, "prerequisitos": ["IDS324", "IDS324L"]},
            {"codigo": "IDS329L", "nombre": "LABORATORIO INGENIERIA DE FACTORES HUMANOS", "creditos": 1, "trimestre": 7, "prerequisitos": ["IDS324", "IDS324L"], "corequisitos": ["IDS329"]},
            {"codigo": "IDS345", "nombre": "DESARROLLO DE SOFTWARE III", "creditos": 3, "trimestre": 7, "prerequisitos": ["IDS341", "IDS341L", "INS377", "INS377L"]},
            {"codigo": "IDS345L", "nombre": "LABORATORIO DE DESARROLLO DE SOFTWARE III", "creditos": 1, "trimestre": 7, "prerequisitos": ["IDS341", "IDS341L", "INS377", "INS377L"], "corequisitos": ["IDS345"]},
            {"codigo": "IDS346", "nombre": "MODELOS Y METODOS DE LA INGENIERIA DE SOFTWARE", "creditos": 3, "trimestre": 7, "prerequisitos": ["IDS202", "IDS202L"]},
            {"codigo": "INS380", "nombre": "BASES DE DATOS II", "creditos": 4, "trimestre": 7, "prerequisitos": ["INS377", "INS377L"]},
            {"codigo": "INS380L", "nombre": "LABORATORIO DE BASES DE DATOS II", "creditos": 1, "trimestre": 7, "prerequisitos": ["INS377", "INS377L"], "corequisitos": ["INS380"]},
            
            # Trimestre 8
            {"codigo": "ICS202", "nombre": "ALGORITMOS MALICIOSOS", "creditos": 4, "trimestre": 8},
            {"codigo": "ICS202L", "nombre": "LABORATORIO DE ALGORITMOS MALICIOSOS", "creditos": 1, "trimestre": 8},
            {"codigo": "IDS325", "nombre": "ASEGURAMIENTO DE LA CALIDAD DEL SOFTWARE", "creditos": 4, "trimestre": 8, "prerequisitos": ["IDS324", "IDS324L"]},
            {"codigo": "IDS325L", "nombre": "LABORATORIO ASEGURAMIENTO DE LA CALIDAD DEL SOFTWARE", "creditos": 1, "trimestre": 8, "prerequisitos": ["IDS324", "IDS324L"], "corequisitos": ["IDS325"]},
            {"codigo": "IDS335", "nombre": "DISEÑO DE SOFTWARE", "creditos": 4, "trimestre": 8, "prerequisitos": ["IDS329", "IDS329L"]},
            {"codigo": "IDS347", "nombre": "TENDENCIAS EN DESARROLLO DE SOFTWARE", "creditos": 3, "trimestre": 8, "prerequisitos": ["IDS345", "IDS345L"]},
            {"codigo": "IDS347L", "nombre": "LABORATORIO TENDENCIAS EN DESARROLLO DE SOFTWARE", "creditos": 1, "trimestre": 8, "prerequisitos": ["IDS345", "IDS345L"]},
            {"codigo": "ING214", "nombre": "ANALISIS DE DATOS EN INGENIERIA", "creditos": 4, "trimestre": 8},
            
            # Trimestre 9
            {"codigo": "CON213", "nombre": "FUNDAMENTOS DE CONTABILIDAD", "creditos": 2, "trimestre": 9, "req_creditos": 90},
            {"codigo": "IDS303", "nombre": "PRACTICA PROFESIONAL DE INGENIERIA DE SOFTWARE", "creditos": 2, "trimestre": 9, "req_creditos": 90},
            {"codigo": "IDS309", "nombre": "ARQUITECTURA DE SOFTWARE", "creditos": 4, "trimestre": 9, "prerequisitos": ["IDS335"]},
            {"codigo": "IDS348", "nombre": "DESARROLLO DE APLICACIONES WEB", "creditos": 3, "trimestre": 9, "prerequisitos": ["IDS345", "IDS345L"]},
            {"codigo": "IDS348L", "nombre": "LABORATORIO DESARROLLO DE APLICACIONES WEB", "creditos": 1, "trimestre": 9, "prerequisitos": ["IDS345", "IDS345L"], "corequisitos": ["IDS348"]},
            {"codigo": "ING230", "nombre": "INGENIERIA ECONOMICA", "creditos": 4, "trimestre": 9},
            {"codigo": "ING231", "nombre": "EXPERIMENTACION EN INGENIERIA", "creditos": 3, "trimestre": 9, "prerequisitos": ["AHQ101", "ING214"]},
            
            # Trimestre 10
            {"codigo": "IDS326", "nombre": "CONSTRUCCION DE SOFTWARE", "creditos": 4, "trimestre": 10, "prerequisitos": ["IDS309"]},
            {"codigo": "IDS326L", "nombre": "LABORATORIO CONSTRUCCION DE SOFTWARE", "creditos": 1, "trimestre": 10, "prerequisitos": ["IDS309"], "corequisitos": ["IDS326"]},
            {"codigo": "IDS349", "nombre": "DESARROLLO DE APLICACIONES MOVILES", "creditos": 3, "trimestre": 10, "prerequisitos": ["IDS348", "IDS348L"]},
            {"codigo": "IDS349L", "nombre": "LABORATORIO DESARROLLO DE APLICACIONES MOVILES", "creditos": 1, "trimestre": 10, "prerequisitos": ["IDS348", "IDS348L"], "corequisitos": ["IDS349"]},
            {"codigo": "ING235", "nombre": "FORMULACION Y GESTION DE PROYECTOS TECNOLOGICOS", "creditos": 4, "trimestre": 10, "prerequisitos": ["ING230", "ING231"]},
            {"codigo": "ING235L", "nombre": "LABORATORIO FORMULACION Y GESTION DE PROYECTOS TECNOLOGICOS", "creditos": 1, "trimestre": 10, "prerequisitos": ["ING230", "ING231"], "corequisitos": ["ING235"]},
            {"codigo": "INS371", "nombre": "ARQUITECTURA DEL COMPUTADOR", "creditos": 3, "trimestre": 10, "prerequisitos": ["IEC208", "IEC208L"]},
            {"codigo": "INS371L", "nombre": "LABORATORIO ARQUITECTURA COMPUTADOR", "creditos": 1, "trimestre": 10, "prerequisitos": ["IEC208", "IEC208L"], "corequisitos": ["INS371"]},
            {"codigo": "ISE2E1", "nombre": "IMPACTO SOCIAL (ELECTIVA)", "creditos": 4, "trimestre": 10},
            
            # Trimestre 11
            {"codigo": "ECO322", "nombre": "ECONOMIA DE EMPRESA", "creditos": 4, "trimestre": 11, "prerequisitos": ["ING230"]},
            {"codigo": "IDS328", "nombre": "ADMINISTRACION DE CONFIGURACION", "creditos": 4, "trimestre": 11, "prerequisitos": ["IDS326", "IDS326L"]},
            {"codigo": "IDS328L", "nombre": "LABORATORIO DE ADMINISTRACION DE CONFIGURACION", "creditos": 1, "trimestre": 11, "prerequisitos": ["IDS326", "IDS326L"], "corequisitos": ["IDS328"]},
            {"codigo": "IDS330", "nombre": "INTELIGENCIA ARTIFICIAL", "creditos": 3, "trimestre": 11, "prerequisitos": ["IDS326", "IDS326L"]},
            {"codigo": "IDS330L", "nombre": "LABORATORIO INTELIGENCIA ARTIFICIAL", "creditos": 1, "trimestre": 11, "prerequisitos": ["IDS326", "IDS326L"], "corequisitos": ["IDS330"]},
            {"codigo": "IDS350", "nombre": "CONSEJERIA PROFESIONAL INGENIERIA DE SOFTWARE II", "creditos": 0, "trimestre": 11, "prerequisitos": ["IDS342"]},
            {"codigo": "IDS351", "nombre": "PRUEBAS DE SOFTWARE", "creditos": 2, "trimestre": 11, "prerequisitos": ["IDS325", "IDS326", "IDS325L", "IDS326L"]},
            {"codigo": "INS373", "nombre": "SISTEMAS OPERATIVOS", "creditos": 4, "trimestre": 11, "prerequisitos": ["INS371", "INS371L"]},
            {"codigo": "INS373L", "nombre": "LABORATORIO SISTEMAS OPERATIVOS", "creditos": 1, "trimestre": 11, "prerequisitos": ["INS371", "INS371L"], "corequisitos": ["INS373"]},
            
            # Trimestre 12
            {"codigo": "ADM315", "nombre": "ADMINISTRACION Y GESTION EMPRESARIAL", "creditos": 4, "trimestre": 12, "prerequisitos": ["ECO322"]},
            {"codigo": "EEE2X1", "nombre": "ELECTIVAS DE ESTUDIOS ESPECIALIZADOS I", "creditos": 0, "trimestre": 12},
            {"codigo": "ICS320", "nombre": "FUNDAMENTOS DE CIBERSEGURIDAD", "creditos": 2, "trimestre": 12, "prerequisitos": ["INS371", "INS371L"]},
            {"codigo": "IDS339", "nombre": "DEVOPS Y DEVSECOPS", "creditos": 3, "trimestre": 12, "prerequisitos": ["INS373", "INS373L"]},
            {"codigo": "IDS352", "nombre": "ANTEPROYECTO DE GRADO", "creditos": 4, "trimestre": 12, "prerequisitos": ["IDS309", "INS371", "INS371L", "IDS325", "IDS325L", "IDS326", "IDS326L", "ING235", "ING235L"]},
            {"codigo": "IDS353", "nombre": "PASANTIA PROFESIONAL I", "creditos": 2, "trimestre": 12},
            {"codigo": "IDS354", "nombre": "GESTION DE LA INGENIERIA DE SOFTWARE", "creditos": 3, "trimestre": 12},
            
            # Trimestre 13
            {"codigo": "EEE2X2", "nombre": "ELECTIVAS DE ESTUDIOS ESPECIALIZADOS II", "creditos": 0, "trimestre": 13},
            {"codigo": "EEP3X1", "nombre": "ELECTIVAS DE ESTUDIOS PROFESIONALIZANTES I", "creditos": 0, "trimestre": 13},
            {"codigo": "IDS322", "nombre": "MANTENIMIENTO DE SOFTWARE", "creditos": 4, "trimestre": 13, "prerequisitos": ["IDS326", "IDS326L", "IDS352"]},
            {"codigo": "IDS355", "nombre": "PROYECTO DE GRADO", "creditos": 4, "trimestre": 13, "prerequisitos": ["IDS352"]},
            {"codigo": "IDS356", "nombre": "PASANTIA PROFESIONAL II", "creditos": 2, "trimestre": 13, "prerequisitos": ["IDS353"]},
            {"codigo": "IDS3X5", "nombre": "CERTIFICACION PROFESIONAL", "creditos": 0, "trimestre": 13},
            
             # Trimestre 14
            {"codigo": "EEP3X2", "nombre": "ELECTIVAS DE ESTUDIOS PROFESIONALIZANTES II", "creditos": 0, "trimestre": 14},
            {"codigo": "EEP3X3", "nombre": "ELECTIVAS DE ESTUDIOS PROFESIONALIZANTES III", "creditos": 0, "trimestre": 14},
            {"codigo": "IDS334", "nombre": "SEMINARIO DE TECNOLOGIA E INGENIERIA DE SOFTWARE", "creditos": 4, "trimestre": 14},
            {"codigo": "IDS357", "nombre": "PROYECTO FINAL DE GRADO", "creditos": 4, "trimestre": 14, "prerequisitos": ["IDS355"]}
        ]
        
        # Crear asignaturas
        for asig_data in asignaturas_data:
            asignatura = Asignatura(
                codigo=asig_data["codigo"],
                nombre=asig_data["nombre"],
                creditos=asig_data["creditos"],
                req_creditos=asig_data.get("req_creditos", None)
            )
            db.add(asignatura)
            db.flush()
            asignaturas[asig_data["codigo"]] = asignatura
            
            # Crear relación con el trimestre
            asig_trimestre = AsignaturaTrimestre(
                asignatura_id=asignatura.id,
                trimestre_id=trimestres[asig_data["trimestre"]].id
            )
            db.add(asig_trimestre)
        
        db.flush()
        
        # Establecer prerequisitos y corequisitos
        for asig_data in asignaturas_data:
            if "prerequisitos" in asig_data:
                for pre_code in asig_data["prerequisitos"]:
                    asignatura = asignaturas[asig_data["codigo"]]
                    prerequisito_asig = asignaturas[pre_code]
                    asignatura.prerequisitos.append(prerequisito_asig)
            
            if "corequisitos" in asig_data:
                for co_code in asig_data["corequisitos"]:
                    asignatura = asignaturas[asig_data["codigo"]]
                    corequisito_asig = asignaturas[co_code]
                    asignatura.corequisitos.append(corequisito_asig)
        
        db.commit()
        print(f"Asignaturas importadas: {len(asignaturas)}")
        print("Importación de Ingeniería Software completada con éxito.")
        
    except Exception as e:
        db.rollback()
        print(f"Error durante la importación de Ingeniería Software: {e}")
        raise
    finally:
        db.close()

def import_ciberseguridad():
    db = SessionLocal()
    
    try:
        # Crear carrera
        carrera = Carrera(
            nombre="Ingeniería en Ciberseguridad",
            descripcion="Ingeniería en Ciberseguridad"
        )
        db.add(carrera)
        db.flush()  # Para obtener el ID de la carrera
        
        print(f"Carrera creada: {carrera.nombre} (ID: {carrera.id})")
        
        # Crear pensum
        pensum = Pensum(
            codigo="VERSION 2020 ICS",
            fecha_aprobacion=date(2023, 11, 2),
            resolucion="20231102-34/112",
            carrera_id=carrera.id
        )
        db.add(pensum)
        db.flush()  # Para obtener el ID del pensum
        
        print(f"Pensum creado: {pensum.codigo} (ID: {pensum.id})")
        
        # Crear los trimestres (1-14)
        trimestres = {}
        for i in range(1, 15):
            trimestre = Trimestre(
                numero=i,
                pensum_id=pensum.id
            )
            db.add(trimestre)
            trimestres[i] = trimestre
        
        db.flush()  # Para obtener los IDs de los trimestres
        
        print(f"Trimestres creados: {len(trimestres)}")
        
        # Diccionario para almacenar las asignaturas
        asignaturas = {}
        
        # Datos de las asignaturas del pensum de Ingeniería en Ciberseguridad
        asignaturas_data = [
            # Trimestre 1
            {"codigo": "AHC109", "nombre": "REDACCION", "creditos": 4, "trimestre": 1},
            {"codigo": "AHO102", "nombre": "ORIENTACION ACADEMICA E INSTITUCIONAL", "creditos": 0, "trimestre": 1},
            {"codigo": "CBA1X3", "nombre": "VIDA EN EL MEDIO AMBIENTE (ELECTIVAS)", "creditos": 2, "trimestre": 1},
            {"codigo": "CBM101", "nombre": "ALGEBRA Y GEOMETRIA ANALITICA", "creditos": 5, "trimestre": 1},
            {"codigo": "CSH112", "nombre": "CIUDADANIA Y ETICA", "creditos": 2, "trimestre": 1},
            {"codigo": "EAA1X1", "nombre": "ELECTIVAS DE AREAS ACADEMICAS I", "creditos": 2, "trimestre": 1},
            {"codigo": "EAA1X2", "nombre": "ELECTIVAS DE AREAS ACADEMICAS II", "creditos": 2, "trimestre": 1},
            {"codigo": "ICS205", "nombre": "INTRODUCCIÓN A LA INGENIERÍA EN CIBERSEGURIDAD", "creditos": 3, "trimestre": 1},
            {"codigo": "SHI103", "nombre": "INGLES 01 (BASICO I)", "creditos": 0, "trimestre": 1},
            
            # Trimestre 2
            {"codigo": "AHC110", "nombre": "ARGUMENTACIÓN LINGÜÍSTICA", "creditos": 4, "trimestre": 2, "prerequisitos": ["AHC109"]},
            {"codigo": "CBM102", "nombre": "CALCULO DIFERENCIAL", "creditos": 5, "trimestre": 2, "prerequisitos": ["CBM101"]},
            {"codigo": "CSH113", "nombre": "PENSAMIENTO CREATIVO", "creditos": 2, "trimestre": 2},
            {"codigo": "CSS102", "nombre": "SER HUMANO Y SOCIEDAD: TEMAS SOCIALES CONTEMPORANEOS", "creditos": 2, "trimestre": 2},
            {"codigo": "EAA1X3", "nombre": "ELECTIVAS DE AREAS ACADEMICAS III", "creditos": 2, "trimestre": 2},
            {"codigo": "EAA1X4", "nombre": "ELECTIVAS DE AREAS ACADEMICAS IV", "creditos": 2, "trimestre": 2},
            {"codigo": "ICS206", "nombre": "CIENCIA, TECNOLOGÍA Y SOCIEDAD", "creditos": 2, "trimestre": 2},
            {"codigo": "ING102", "nombre": "INTRODUCCION A LA PROGRAMACION", "creditos": 2, "trimestre": 2, "prerequisitos": ["CBM101"]},
            {"codigo": "ING102L", "nombre": "LABORATORIO DE INTRODUCCION A LA PROGRAMACION", "creditos": 0, "trimestre": 2, "prerequisitos": ["CBM101"], "corequisitos": ["ING102"]},
            {"codigo": "SHI104", "nombre": "INGLES 02 (BASICO II)", "creditos": 0, "trimestre": 2},
            
            # Trimestre 3
            {"codigo": "AHQ101", "nombre": "QUEHACER CIENTIFICO", "creditos": 4, "trimestre": 3},
            {"codigo": "CBM201", "nombre": "CALCULO INTEGRAL", "creditos": 5, "trimestre": 3, "prerequisitos": ["CBM102"]},
            {"codigo": "IDS202", "nombre": "TECNOLOGIA DE OBJETOS", "creditos": 4, "trimestre": 3, "prerequisitos": ["ING102"]},
            {"codigo": "IDS202L", "nombre": "LABORATORIO TECNOLOGIA DE OBJETOS", "creditos": 1, "trimestre": 3, "prerequisitos": ["ING102L"], "corequisitos": ["IDS202"]},
            {"codigo": "IDS340", "nombre": "DESARROLLO DE SOFTWARE I", "creditos": 3, "trimestre": 3, "prerequisitos": ["ING102", "ING102L"]},
            {"codigo": "IDS340L", "nombre": "LABORATORIO DE DESARROLLO DE SOFTWARE I", "creditos": 1, "trimestre": 3, "prerequisitos": ["ING102L"], "corequisitos": ["IDS340"]},
            {"codigo": "ING228", "nombre": "HOJA DE CALCULO PARA INGENIEROS", "creditos": 1, "trimestre": 3, "prerequisitos": ["CBM102"]},
            {"codigo": "SHI105", "nombre": "INGLES 03 (INTERMEDIO I)", "creditos": 0, "trimestre": 3, "prerequisitos": ["SHI104"]},
            
            # Trimestre 4
            {"codigo": "CBF210", "nombre": "FISICA MECANICA I", "creditos": 4, "trimestre": 4, "prerequisitos": ["CBM201"]},
            {"codigo": "CBF210L", "nombre": "LABORATORIO DE FISICA MECANICA I", "creditos": 1, "trimestre": 4, "prerequisitos": ["CBM201"], "corequisitos": ["CBF210"]},
            {"codigo": "CBM202", "nombre": "CALCULO VECTORIAL", "creditos": 5, "trimestre": 4, "prerequisitos": ["CBM201"]},
            {"codigo": "ICS207", "nombre": "CONSEJERIA INGENIERIA CIBERSEGURIDAD I", "creditos": 0, "trimestre": 4, "req_creditos": 35},
            {"codigo": "IDS341", "nombre": "DESARROLLO DE SOFTWARE II", "creditos": 3, "trimestre": 4, "prerequisitos": ["IDS340", "IDS340L"]},
            {"codigo": "IDS341L", "nombre": "LABORATORIO DE DESARROLLO DE SOFTWARE II", "creditos": 1, "trimestre": 4, "prerequisitos": ["IDS340", "IDS340L"], "corequisitos": ["IDS341"]},
            {"codigo": "IMC207", "nombre": "SEMINARIO INTRODUCCION A ARDUINO", "creditos": 0, "trimestre": 4, "req_creditos": 35},
            {"codigo": "ING214", "nombre": "ANALISIS DE DATOS EN INGENIERIA", "creditos": 4, "trimestre": 4, "prerequisitos": ["CBM201"]},
            {"codigo": "SHI106", "nombre": "INGLES 04 (INTERMEDIO II)", "creditos": 0, "trimestre": 4, "prerequisitos": ["SHI105"]},
            
            # Trimestre 5
            {"codigo": "CBF211", "nombre": "FISICA MECANICA II", "creditos": 4, "trimestre": 5, "prerequisitos": ["CBF210", "CBM201", "CBF210L"]},
            {"codigo": "CBF211L", "nombre": "LABORATORIO DE FISICA MECANICA II", "creditos": 1, "trimestre": 5, "prerequisitos": ["CBF210", "CBM201", "CBF210L"], "corequisitos": ["CBF211"]},
            {"codigo": "CBM208", "nombre": "ALGEBRA LINEAL", "creditos": 5, "trimestre": 5, "prerequisitos": ["CBM202"]},
            {"codigo": "CSG203", "nombre": "PENSAMIENTO Y PROBLEMAS DE LA SOCIEDAD CONTEMPORANEA", "creditos": 4, "trimestre": 5},
            {"codigo": "IDS324", "nombre": "INGENIERIA DE REQUERIMIENTOS DE SOFTWARE", "creditos": 4, "trimestre": 5, "prerequisitos": ["IDS202", "IDS202L"]},
            {"codigo": "IDS324L", "nombre": "LABORATORIO INGENIERIA DE REQUERIMIENTOS DE SOFTWARE", "creditos": 1, "trimestre": 5, "prerequisitos": ["IDS202", "IDS202L"], "corequisitos": ["IDS324"]},
            {"codigo": "IDS343", "nombre": "ESTRUCTURAS DE DATOS Y ALGORITMOS I", "creditos": 3, "trimestre": 5, "prerequisitos": ["IDS341"]},
            {"codigo": "IDS343L", "nombre": "LABORATORIO ESTRUCTURAS DE DATOS Y ALGORITMOS I", "creditos": 1, "trimestre": 5, "prerequisitos": ["IDS341L"], "corequisitos": ["IDS343"]},
            {"codigo": "SHI107", "nombre": "INGLES 05 (AVANZADO I)", "creditos": 0, "trimestre": 5, "prerequisitos": ["SHI106"]},
            
            # Trimestre 6
            {"codigo": "CBM203", "nombre": "ECUACIONES DIFERENCIALES", "creditos": 5, "trimestre": 6, "prerequisitos": ["CBM208"]},
            {"codigo": "CSG204", "nombre": "ANTROPOLOGIA SOCIAL", "creditos": 4, "trimestre": 6},
            {"codigo": "CSH105", "nombre": "PROYECTO INTEGRADOR DE ESTUDIOS GENERALES", "creditos": 2, "trimestre": 6, "req_creditos": 40},
            {"codigo": "IEC208", "nombre": "FUNDAMENTOS ELECTRÓNICA DIGITAL", "creditos": 3, "trimestre": 6, "prerequisitos": ["CBF211", "CBF211L"]},
            {"codigo": "IEC208L", "nombre": "LABORATORIO FUNDAMENTOS ELECTRÓNICA DIGITAL", "creditos": 1, "trimestre": 6, "prerequisitos": ["CBF211", "CBF211L"], "corequisitos": ["IEC208"]},
            {"codigo": "INS377", "nombre": "BASES DE DATOS I", "creditos": 4, "trimestre": 6, "prerequisitos": ["IDS324", "IDS343", "IDS324L", "IDS343L"]},
            {"codigo": "INS377L", "nombre": "LABORATORIO BASES DE DATOS I", "creditos": 1, "trimestre": 6, "prerequisitos": ["IDS324", "IDS324L", "IDS343", "IDS343L"], "corequisitos": ["INS377"]},
            {"codigo": "SHI108", "nombre": "INGLES 06 (AVANZADO II)", "creditos": 0, "trimestre": 6, "prerequisitos": ["SHI107"]},
            
            # Trimestre 7
            {"codigo": "CBM305", "nombre": "MATEMATICA DISCRETA I", "creditos": 4, "trimestre": 7, "prerequisitos": ["CBM203"]},
            {"codigo": "CHH301", "nombre": "ETICA PROFESIONAL", "creditos": 2, "trimestre": 7},
            {"codigo": "ICS202", "nombre": "ALGORITMOS MALICIOSOS", "creditos": 4, "trimestre": 7, "prerequisitos": ["IDS343", "IDS341L"]},
            {"codigo": "ICS202L", "nombre": "LABORATORIO DE ALGORITMOS MALICIOSOS", "creditos": 1, "trimestre": 7, "prerequisitos": ["IDS343L", "IDS343"], "corequisitos": ["ICS202"]},
            {"codigo": "IDS345", "nombre": "DESARROLLO DE SOFTWARE III", "creditos": 3, "trimestre": 7, "prerequisitos": ["IDS341", "INS377", "IDS341L", "INS377L"]},
            {"codigo": "IDS345L", "nombre": "LABORATORIO DE DESARROLLO DE SOFTWARE III", "creditos": 1, "trimestre": 7, "prerequisitos": ["IDS341L", "INS377", "IDS341", "INS377L"], "corequisitos": ["IDS345"]},
            {"codigo": "ING230", "nombre": "INGENIERIA ECONOMICA", "creditos": 4, "trimestre": 7, "prerequisitos": ["ING214"]},
            {"codigo": "ING231", "nombre": "EXPERIMENTACION EN INGENIERIA", "creditos": 3, "trimestre": 7, "prerequisitos": ["AHQ101", "ING214"]},
            
            # Trimestre 8
            {"codigo": "CBM306", "nombre": "MATEMATICA DISCRETA II", "creditos": 4, "trimestre": 8, "prerequisitos": ["CBM305"]},
            {"codigo": "EEE2X1", "nombre": "ELECTIVAS DE ESTUDIOS ESPECIALIZADOS I", "creditos": 0, "trimestre": 8},
            {"codigo": "ICS201", "nombre": "EL CIBERESPACIO, LA CIBERGUERRA, LA GOBERNANZA INTERNET", "creditos": 4, "trimestre": 8},
            {"codigo": "ING235", "nombre": "FORMULACION Y GESTION DE PROYECTOS TECNOLOGICOS", "creditos": 4, "trimestre": 8, "prerequisitos": ["ING230", "ING231"], "corequisitos": ["ING235L"]},
            {"codigo": "ING235L", "nombre": "LABORATORIO FORMULACION Y GESTION DE PROYECTOS TECNOLOGICOS", "creditos": 1, "trimestre": 8, "prerequisitos": ["ING230", "ING231"], "corequisitos": ["ING235"]},
            {"codigo": "INS371", "nombre": "ARQUITECTURA DEL COMPUTADOR", "creditos": 3, "trimestre": 8, "prerequisitos": ["IEC208", "IEC208L"], "corequisitos": ["INS371L"]},
            {"codigo": "INS371L", "nombre": "LABORATORIO ARQUITECTURA COMPUTADOR", "creditos": 1, "trimestre": 8, "prerequisitos": ["IEC208", "IEC208L"], "corequisitos": ["INS371"]},
            {"codigo": "ISE2E1", "nombre": "IMPACTO SOCIAL (ELECTIVA)", "creditos": 4, "trimestre": 8},
            
            # Trimestre 9
            {"codigo": "CBM307", "nombre": "ANALISIS NUMERICO", "creditos": 4, "trimestre": 9, "prerequisitos": ["CBM208"]},
            {"codigo": "CBM307L", "nombre": "LABORATORIO DE ANALISIS NUMERICO", "creditos": 1, "trimestre": 9, "prerequisitos": ["CBM208"], "corequisitos": ["CBM307"]},
            {"codigo": "EEE2X2", "nombre": "ELECTIVAS DE ESTUDIOS ESPECIALIZADOS II", "creditos": 0, "trimestre": 9},
            {"codigo": "ICS301", "nombre": "ANALISIS DE MALWARE", "creditos": 4, "trimestre": 9, "prerequisitos": ["ICS202", "ICS202L"]},
            {"codigo": "ICS301L", "nombre": "LABORATORIO DE ANALISIS DE MALWARE", "creditos": 1, "trimestre": 9, "prerequisitos": ["ICS202", "ICS202L"], "corequisitos": ["ICS301"]},
            {"codigo": "ICS320", "nombre": "FUNDAMENTOS DE CIBERSEGURIDAD", "creditos": 2, "trimestre": 9, "prerequisitos": ["INS371", "INS371L"]},
            {"codigo": "INS373", "nombre": "SISTEMAS OPERATIVOS", "creditos": 4, "trimestre": 9, "prerequisitos": ["INS371", "INS371L"]},
            {"codigo": "INS373L", "nombre": "LABORATORIO SISTEMAS OPERATIVOS", "creditos": 1, "trimestre": 9, "prerequisitos": ["INS371", "INS371L"], "corequisitos": ["INS373"]},
            
            # Trimestre 10
            {"codigo": "CON213", "nombre": "FUNDAMENTOS DE CONTABILIDAD", "creditos": 2, "trimestre": 10},
            {"codigo": "ICS305", "nombre": "INFORMATICA FORENSE", "creditos": 4, "trimestre": 10, "prerequisitos": ["ICS320"]},
            {"codigo": "ICS305L", "nombre": "LABORATORIO DE INFORMATICA FORENSE", "creditos": 1, "trimestre": 10, "prerequisitos": ["ICS320"], "corequisitos": ["ICS305"]},
            {"codigo": "ICS311", "nombre": "GESTION DE INFRAESTRUCTURAS CRITICAS DE TI", "creditos": 4, "trimestre": 10, "prerequisitos": ["ICS320"]},
            {"codigo": "ICS311L", "nombre": "LABORATORIO GESTION DE INFRAESTRUCTURAS CRITICAS DE TI", "creditos": 1, "trimestre": 10, "prerequisitos": ["ICS320"], "corequisitos": ["ICS311"]},
            {"codigo": "ICS322", "nombre": "ESTANDARES Y MEJORES PRACTICAS EN CIBERSEGURIDAD", "creditos": 3, "trimestre": 10, "prerequisitos": ["ICS320"]},
            {"codigo": "ICS3C1", "nombre": "CERTIFICACION ELECTIVA", "creditos": 0, "trimestre": 10},
            {"codigo": "INS376", "nombre": "COMUNICACION DE DATOS I", "creditos": 4, "trimestre": 10, "prerequisitos": ["INS373", "INS373L"]},
            {"codigo": "INS376L", "nombre": "LABORATORIO COMUNICACION DE DATOS I", "creditos": 1, "trimestre": 10, "prerequisitos": ["INS373", "INS373L"], "corequisitos": ["INS376"]},
            
            # Trimestre 11
            {"codigo": "ECO322", "nombre": "ECONOMIA DE EMPRESA", "creditos": 4, "trimestre": 11, "prerequisitos": ["ING230"]},
            {"codigo": "EEP3X1", "nombre": "ELECTIVAS DE ESTUDIOS PROFESIONALIZANTES I", "creditos": 0, "trimestre": 11},
            {"codigo": "ICS302", "nombre": "CRIPTOGRAFIA", "creditos": 4, "trimestre": 11, "prerequisitos": ["CBM306"]},
            {"codigo": "ICS302L", "nombre": "LABORATORIO DE CRIPTOGRAFIA", "creditos": 1, "trimestre": 11, "prerequisitos": ["CBM306"], "corequisitos": ["ICS302"]},
            {"codigo": "ICS319", "nombre": "ETHICAL HACKING", "creditos": 4, "trimestre": 11, "prerequisitos": ["ICS320"]},
            {"codigo": "ICS319L", "nombre": "LABORATORIO ETHICAL HACKING", "creditos": 1, "trimestre": 11, "prerequisitos": ["ICS320"], "corequisitos": ["ICS319"]},
            {"codigo": "ICS321", "nombre": "CIBERSEGURIDAD II CONSEJERIA INGENIERIA", "creditos": 0, "trimestre": 11, "prerequisitos": ["ICS207"]},
            {"codigo": "INS379", "nombre": "COMUNICACION DE DATOS II", "creditos": 4, "trimestre": 11, "prerequisitos": ["INS376", "INS376L"]},
            {"codigo": "INS379L", "nombre": "LABORATORIO COMUNICACION DE DATOS II", "creditos": 1, "trimestre": 11, "prerequisitos": ["INS376", "INS376L"], "corequisitos": ["INS379"]},
            
            # Trimestre 12
            {"codigo": "EEP3X2", "nombre": "ELECTIVAS DE ESTUDIOS PROFESIONALIZANTES II", "creditos": 0, "trimestre": 12},
            {"codigo": "ICS325", "nombre": "ANTE PROYECTO DE CIBERSEGURIDAD", "creditos": 4, "trimestre": 12, "prerequisitos": ["ING235", "ING235L"]},
            {"codigo": "INS342", "nombre": "TECNOLOGIAS DE INFORMACION EMERGENTE", "creditos": 4, "trimestre": 12},
            {"codigo": "INS382", "nombre": "GESTION DE TI-SEGURIDAD Y RIESGOS", "creditos": 4, "trimestre": 12, "prerequisitos": ["INS377", "INS377L"]},
            {"codigo": "PSI303", "nombre": "PSICOLOGIA SOCIAL", "creditos": 4, "trimestre": 12},
            
            # Trimestre 13
            {"codigo": "ADM315", "nombre": "ADMINISTRACION Y GESTION EMPRESARIAL", "creditos": 4, "trimestre": 13, "prerequisitos": ["ECO322"]},
            {"codigo": "EEP3X3", "nombre": "ELECTIVAS DE ESTUDIOS PROFESIONALIZANTES III", "creditos": 0, "trimestre": 13},
            {"codigo": "ICS304", "nombre": "MARCO JURIDICO CYDAT", "creditos": 2, "trimestre": 13, "prerequisitos": ["ICS320"]},
            {"codigo": "ICS323", "nombre": "PASANTÍA PROFESIONAL DE CIBERSEGURIDAD I", "creditos": 2, "trimestre": 13, "req_creditos": 100},
            {"codigo": "ICS326", "nombre": "POLITICAS, PROCEDIMIENTOS Y AUDITORIA EN CIBERSEGURIDAD", "creditos": 4, "trimestre": 13, "prerequisitos": ["ICS322", "INS382"]},
            {"codigo": "ICS327", "nombre": "PROYECTO DE GRADO CIBERSEGURIDAD", "creditos": 4, "trimestre": 13, "prerequisitos": ["ICS325"]},
            
            # Trimestre 14
            {"codigo": "EEP3X4", "nombre": "ELECTIVAS ESTUDIOS DE PROFESIONALIZANTES IV", "creditos": 0, "trimestre": 14},
            {"codigo": "ICS306", "nombre": "SEMINARIO CIBERSEGURIDAD", "creditos": 4, "trimestre": 14, "prerequisitos": ["ICS325"]},
            {"codigo": "ICS324", "nombre": "PASANTÍA PROFESIONAL DE CIBERSEGURIDAD II", "creditos": 2, "trimestre": 14, "req_creditos": 180},
            {"codigo": "ICS328", "nombre": "PLANEACION ESTRATEGICA DE LA CIBERSEGURIDAD", "creditos": 4, "trimestre": 14, "prerequisitos": ["ICS326"]},
            {"codigo": "ICS329", "nombre": "PROYECTO FINAL DE CIBERSEGURIDAD", "creditos": 4, "trimestre": 14, "prerequisitos": ["ICS327"]}
        ]
        
        # Crear asignaturas
        for asig_data in asignaturas_data:
            asignatura = Asignatura(
                codigo=asig_data["codigo"],
                nombre=asig_data["nombre"],
                creditos=asig_data["creditos"],
                req_creditos=asig_data.get("req_creditos", None)
            )
            db.add(asignatura)
            db.flush()
            asignaturas[asig_data["codigo"]] = asignatura
            
            # Crear relación con el trimestre
            asig_trimestre = AsignaturaTrimestre(
                asignatura_id=asignatura.id,
                trimestre_id=trimestres[asig_data["trimestre"]].id
            )
            db.add(asig_trimestre)
        
        db.flush()
        
        # Establecer prerequisitos y corequisitos
        for asig_data in asignaturas_data:
            if "prerequisitos" in asig_data:
                for pre_code in asig_data["prerequisitos"]:
                    asignatura = asignaturas[asig_data["codigo"]]
                    prerequisito_asig = asignaturas[pre_code]
                    asignatura.prerequisitos.append(prerequisito_asig)
            
            if "corequisitos" in asig_data:
                for co_code in asig_data["corequisitos"]:
                    asignatura = asignaturas[asig_data["codigo"]]
                    corequisito_asig = asignaturas[co_code]
                    asignatura.corequisitos.append(corequisito_asig)
        
        db.commit()
        print(f"Asignaturas importadas: {len(asignaturas)}")
        print("Importación de Ingeniería en Ciberseguridad completada con éxito.")
        
    except Exception as e:
        db.rollback()
        print(f"Error durante la importación de Ingeniería en Ciberseguridad: {e}")
        raise
    finally:
        db.close()

def import_all_pensums():
    try:
        print("Iniciando importación de todos los pensums...")
        
        import_sistemas()
        
        import_software()
        
        import_ciberseguridad()
        
        print("Todos los pensums importados con éxito.")
    except Exception as e:
        print(f"Error durante la importación de pensums: {e}")
        raise

if __name__ == "__main__":
    import_all_pensums()
import collections.abc

# Parche de compatibilidad para Experta en Python 3.10+
if not hasattr(collections, 'Mapping'):
    collections.Mapping = collections.abc.Mapping

from experta import (
    Fact, KnowledgeEngine, Rule, DefFacts, 
    AND, OR, NOT, Field, AS
)

# Definición de las Clases de Hechos 
class Residuo(Fact):
    """
    Representa un residuo en el sistema.
    Atributos: id_residuo, tipo, cantidad, contaminacion, contenedor, clasificacion
    """
    pass

class Contenedor(Fact):
    """
    Representa un contenedor donde se deposita un residuo.
    Atributos: id_contenedor, capacidad, acumulacion
    """
    pass

class Tratamiento(Fact):
    """
    Representa el tratamiento asignado a un residuo.
    Atributos: id_residuo, tipo_tratamiento
    """
    pass

class ResultadoDifuso(Fact):
    """
    Representa el resultado transferido desde el sistema de lógica difusa.
    Atributos: id_residuo, valor_prioridad, categoria_prioridad (Baja, Media, Alta)
    """
    pass

class AccionGestion(Fact):
    """
    Representa las recomendaciones o acciones de gestión generadas por las reglas.
    Atributos: id_residuo, accion
    """
    pass

class CentroGestion(Fact):
    """
    Representa el centro de gestión asignado según el tratamiento.
    Atributos: id_residuo, centro
    """
    pass


# Motor de Inferencia del Sistema Experto 
class SistemaExpertoResiduos(KnowledgeEngine):
    """
    Motor de conocimiento que integra:
    - Clasificación de residuos.
    - Asignación de tratamientos.
    - Generación de acciones de gestión según prioridad y riesgo.
    - Asignación de centros de gestión.
    
    Estrategias de control y resolución de conflictos aplicadas:
    1. Salience (3 niveles: 100 Críticas, 50 Clasificación/Tratamiento, 10 Gestión general).
    2. Especificidad (Reglas con más condiciones tienen preferencia).
    3. Recencia (Resolución de conflictos en reglas de igual salience).
    4. Control de bucles mediante Lock-Fact / Check de existencia (NOT).
    """

    @DefFacts()
    def _hechos_iniciales(self):
        """Inicialización del motor de reglas."""
        yield Fact(inicio=True)

    @Rule(Fact(inicio=True), salience=100)
    def inicio_sistema(self):
        print("=== Sistema Experto para Clasificación y Gestión de Residuos Iniciado ===")


    # SECCIÓN 1: REGLAS DE CLASIFICACIÓN (Salience 50)
    @Rule(Residuo(id_residuo=MATCH.i, tipo="Plastico"), NOT(Residuo(id_residuo=MATCH.i, clasificacion="Reciclable")), salience=50)
    def clasificar_plastico(self, i):
        """Regla 1: Residuo de tipo Plastico -> clasificación Reciclable."""
        print(f"[Clasificación] Residuo {i} de tipo Plastico clasificado como Reciclable.")
        self.declare(Residuo(id_residuo=i, tipo="Plastico", clasificacion="Reciclable"))

    @Rule(Residuo(id_residuo=MATCH.i, tipo="Papel"), NOT(Residuo(id_residuo=MATCH.i, clasificacion="Reciclable")), salience=50)
    def clasificar_papel(self, i):
        """Regla 2: Residuo de tipo Papel -> clasificación Reciclable."""
        print(f"[Clasificación] Residuo {i} de tipo Papel clasificado como Reciclable.")
        self.declare(Residuo(id_residuo=i, tipo="Papel", clasificacion="Reciclable"))

    @Rule(Residuo(id_residuo=MATCH.i, tipo="Vidrio"), NOT(Residuo(id_residuo=MATCH.i, clasificacion="Reciclable")), salience=50)
    def clasificar_vidrio(self, i):
        """Regla 3: Residuo de tipo Vidrio -> clasificación Reciclable."""
        print(f"[Clasificación] Residuo {i} de tipo Vidrio clasificado como Reciclable.")
        self.declare(Residuo(id_residuo=i, tipo="Vidrio", clasificacion="Reciclable"))

    @Rule(Residuo(id_residuo=MATCH.i, tipo="Metal"), NOT(Residuo(id_residuo=MATCH.i, clasificacion="Reciclable")), salience=50)
    def clasificar_metal(self, i):
        """Regla 4: Residuo de tipo Metal -> clasificación Reciclable."""
        print(f"[Clasificación] Residuo {i} de tipo Metal clasificado como Reciclable.")
        self.declare(Residuo(id_residuo=i, tipo="Metal", clasificacion="Reciclable"))

    @Rule(Residuo(id_residuo=MATCH.i, tipo="Organico"), NOT(Residuo(id_residuo=MATCH.i, clasificacion="Organico")), salience=50)
    def clasificar_organico(self, i):
        """Regla 5: Residuo de tipo Organico -> clasificación Organico."""
        print(f"[Clasificación] Residuo {i} de tipo Organico clasificado como Organico.")
        self.declare(Residuo(id_residuo=i, tipo="Organico", clasificacion="Organico"))

    @Rule(Residuo(id_residuo=MATCH.i, tipo="Peligroso"), NOT(Residuo(id_residuo=MATCH.i, clasificacion="Peligroso")), salience=50)
    def clasificar_peligroso(self, i):
        """Regla 6: Residuo de tipo Peligroso -> clasificación Peligroso."""
        print(f"[Clasificación] Residuo {i} de tipo Peligroso clasificado como Peligroso.")
        self.declare(Residuo(id_residuo=i, tipo="Peligroso", clasificacion="Peligroso"))

    @Rule(Residuo(id_residuo=MATCH.i, tipo="Ordinario"), NOT(Residuo(id_residuo=MATCH.i, clasificacion="Ordinario")), salience=50)
    def clasificar_ordinario(self, i):
        """Regla 7: Residuo de tipo Ordinario -> clasificación Ordinario."""
        print(f"[Clasificación] Residuo {i} de tipo Ordinario clasificado como Ordinario.")
        self.declare(Residuo(id_residuo=i, tipo="Ordinario", clasificacion="Ordinario"))


    # SECCIÓN 2: REGLAS DE TRATAMIENTO Y ACCIÓN PREVIA (Salience 50)
    @Rule(
        OR(Residuo(id_residuo=MATCH.i, clasificacion="Reciclable"), Residuo(id_residuo=MATCH.i, tipo="Plastico"), Residuo(id_residuo=MATCH.i, tipo="Papel"), Residuo(id_residuo=MATCH.i, tipo="Vidrio"), Residuo(id_residuo=MATCH.i, tipo="Metal")),
        Residuo(id_residuo=MATCH.i, contaminacion=MATCH.c),
        TEST(lambda c: c < 70),
        NOT(Tratamiento(id_residuo=MATCH.i, tipo_tratamiento="Reciclaje")),
        salience=50
    )
    def tratamiento_reciclaje(self, i, c):
        """Regla 8: Residuo Reciclable con contaminación/riesgo bajo/medio (<70) -> Tratamiento Reciclaje."""
        print(f"[Tratamiento] Residuo {i} asignado a Tratamiento: Reciclaje.")
        self.declare(Tratamiento(id_residuo=i, tipo_tratamiento="Reciclaje"))

    @Rule(
        OR(Residuo(id_residuo=MATCH.i, clasificacion="Organico"), Residuo(id_residuo=MATCH.i, tipo="Organico")),
        NOT(Tratamiento(id_residuo=MATCH.i, tipo_tratamiento="Compostaje")),
        salience=50
    )
    def tratamiento_compostaje(self, i):
        """Regla 9: Residuo Orgánico -> Tratamiento Compostaje."""
        print(f"[Tratamiento] Residuo {i} asignado a Tratamiento: Compostaje.")
        self.declare(Tratamiento(id_residuo=i, tipo_tratamiento="Compostaje"))

    @Rule(
        OR(Residuo(id_residuo=MATCH.i, clasificacion="Peligroso"), Residuo(id_residuo=MATCH.i, tipo="Peligroso")),
        NOT(Tratamiento(id_residuo=MATCH.i, tipo_tratamiento="TratamientoEspecial")),
        salience=50
    )
    def tratamiento_especial(self, i):
        """Regla 10: Residuo Peligroso -> Tratamiento Especial."""
        print(f"[Tratamiento] Residuo {i} asignado a Tratamiento: TratamientoEspecial.")
        self.declare(Tratamiento(id_residuo=i, tipo_tratamiento="TratamientoEspecial"))

    @Rule(
        OR(Residuo(id_residuo=MATCH.i, clasificacion="Ordinario"), Residuo(id_residuo=MATCH.i, tipo="Ordinario")),
        NOT(Tratamiento(id_residuo=MATCH.i, tipo_tratamiento="DisposicionFinal")),
        salience=50
    )
    def tratamiento_disposicion_final(self, i):
        """Regla 11: Residuo Ordinario -> Tratamiento DisposicionFinal."""
        print(f"[Tratamiento] Residuo {i} asignado a Tratamiento: DisposicionFinal.")
        self.declare(Tratamiento(id_residuo=i, tipo_tratamiento="DisposicionFinal"))

    @Rule(
        OR(Residuo(id_residuo=MATCH.i, clasificacion="Reciclable"), Residuo(id_residuo=MATCH.i, tipo="Plastico"), Residuo(id_residuo=MATCH.i, tipo="Papel"), Residuo(id_residuo=MATCH.i, tipo="Vidrio"), Residuo(id_residuo=MATCH.i, tipo="Metal")),
        Residuo(id_residuo=MATCH.i, contaminacion=MATCH.c),
        TEST(lambda c: c >= 70),
        NOT(AccionGestion(id_residuo=MATCH.i, accion="SeparacionOPretratamiento")),
        salience=50
    )
    def requerir_separacion_pretratamiento(self, i, c):
        """Regla 12: Residuo Reciclable con contaminación alta (>=70) -> Acción SeparacionOPretratamiento."""
        print(f"[Pretratamiento] Residuo {i} requiere SeparacionOPretratamiento por nivel de contaminación alto ({c}).")
        self.declare(AccionGestion(id_residuo=i, accion="SeparacionOPretratamiento"))

 
    # SECCIÓN 3: REGLAS CRÍTICAS Y DE ESPECIFICIDAD (Salience 100)
    @Rule(
        OR(Residuo(id_residuo=MATCH.i, clasificacion="Peligroso"), Residuo(id_residuo=MATCH.i, tipo="Peligroso")),
        ResultadoDifuso(id_residuo=MATCH.i, categoria_prioridad="Alta"),
        NOT(AccionGestion(id_residuo=MATCH.i, accion="GestionUrgente")),
        salience=100
    )
    def gestion_urgente_peligroso(self, i):
        """Regla 13 (Crítica / Alta Especificidad): Residuo Peligroso con Prioridad Alta -> Acción GestionUrgente."""
        print(f"[ALERTA CRÍTICA] Residuo Peligroso {i} con prioridad ALTA requiere GestionUrgente.")
        self.declare(AccionGestion(id_residuo=i, accion="GestionUrgente"))

    @Rule(
        Residuo(id_residuo=MATCH.i, contaminacion=MATCH.c),
        TEST(lambda c: c >= 70),
        NOT(AccionGestion(id_residuo=MATCH.i, accion="ManejoEspecial")),
        salience=100
    )
    def manejo_especial_contaminacion_alta(self, i, c):
        """Regla 14 (Crítica): Residuo con contaminación/riesgo alto (>=70) -> Acción ManejoEspecial."""
        print(f"[ALERTA CRÍTICA] Residuo {i} presenta alta contaminación/riesgo ({c}) -> Requiere ManejoEspecial.")
        self.declare(AccionGestion(id_residuo=i, accion="ManejoEspecial"))

    @Rule(
        Contenedor(id_contenedor=MATCH.c_id, acumulacion=MATCH.acum),
        Residuo(id_residuo=MATCH.i, contenedor=MATCH.c_id),
        TEST(lambda acum: acum >= 80),
        NOT(AccionGestion(id_residuo=MATCH.i, accion="PriorizarGestion")),
        salience=100
    )
    def priorizar_por_contenedor_lleno(self, i, c_id, acum):
        """Regla 15 (Crítica): Contenedor con acumulación alta (>=80%) -> Acción PriorizarGestion sobre el residuo."""
        print(f"[ALERTA CRÍTICA] Contenedor {c_id} con acumulación ALTA ({acum}%) -> PriorizarGestion del residuo {i}.")
        self.declare(AccionGestion(id_residuo=i, accion="PriorizarGestion"))

   
    # SECCIÓN 4: REGLAS GENERALES DE GESTIÓN (Salience 10)
    @Rule(
        ResultadoDifuso(id_residuo=MATCH.i, categoria_prioridad="Alta"),
        NOT(AccionGestion(id_residuo=MATCH.i, accion="GestionPrioritaria")),
        salience=10
    )
    def gestion_prioritaria(self, i):
        """Regla 16: Resultado Difuso con prioridad Alta -> Acción GestionPrioritaria."""
        print(f"[Gestión] Resultado Difuso Alto para Residuo {i} -> Acción: GestionPrioritaria.")
        self.declare(AccionGestion(id_residuo=i, accion="GestionPrioritaria"))

    @Rule(
        ResultadoDifuso(id_residuo=MATCH.i, categoria_prioridad="Media"),
        NOT(AccionGestion(id_residuo=MATCH.i, accion="GestionRegular")),
        salience=10
    )
    def gestion_regular(self, i):
        """Regla 17: Resultado Difuso con prioridad Media -> Acción GestionRegular."""
        print(f"[Gestión] Resultado Difuso Medio para Residuo {i} -> Acción: GestionRegular.")
        self.declare(AccionGestion(id_residuo=i, accion="GestionRegular"))

    @Rule(
        ResultadoDifuso(id_residuo=MATCH.i, categoria_prioridad="Baja"),
        NOT(AccionGestion(id_residuo=MATCH.i, accion="GestionProgramada")),
        salience=10
    )
    def gestion_programada(self, i):
        """Regla 18: Resultado Difuso con prioridad Baja -> Acción GestionProgramada."""
        print(f"[Gestión] Resultado Difuso Bajo para Residuo {i} -> Acción: GestionProgramada.")
        self.declare(AccionGestion(id_residuo=i, accion="GestionProgramada"))

    # =====================================================================
    # SECCIÓN 5: REGLAS DE ASIGNACIÓN DE CENTRO DE GESTIÓN (Salience 10)
    # Enlaza el tratamiento determinado con la entidad semántica CentroGestion
    # =====================================================================

    @Rule(
        Tratamiento(id_residuo=MATCH.i, tipo_tratamiento="Reciclaje"),
        NOT(CentroGestion(id_residuo=MATCH.i)),
        salience=10
    )
    def asignar_centro_reciclaje(self, i):
        """Regla 19: Asignación a Centro de Reciclaje."""
        print(f"[Centro Gestión] Residuo {i} asignado a 'CentroGestion_Reciclaje'.")
        self.declare(CentroGestion(id_residuo=i, centro="CentroGestion_Reciclaje"))

    @Rule(
        Tratamiento(id_residuo=MATCH.i, tipo_tratamiento="Compostaje"),
        NOT(CentroGestion(id_residuo=MATCH.i)),
        salience=10
    )
    def asignar_centro_compostaje(self, i):
        """Regla 20: Asignación a Centro de Compostaje."""
        print(f"[Centro Gestión] Residuo {i} asignado a 'CentroGestion_Compostaje'.")
        self.declare(CentroGestion(id_residuo=i, centro="CentroGestion_Compostaje"))

    @Rule(
        Tratamiento(id_residuo=MATCH.i, tipo_tratamiento="TratamientoEspecial"),
        NOT(CentroGestion(id_residuo=MATCH.i)),
        salience=10
    )
    def asignar_centro_especial(self, i):
        """Regla 21: Asignación a Centro de Tratamiento Especial."""
        print(f"[Centro Gestión] Residuo {i} asignado a 'CentroGestion_Especial'.")
        self.declare(CentroGestion(id_residuo=i, centro="CentroGestion_Especial"))

    @Rule(
        Tratamiento(id_residuo=MATCH.i, tipo_tratamiento="DisposicionFinal"),
        NOT(CentroGestion(id_residuo=MATCH.i)),
        salience=10
    )
    def asignar_centro_disposicion(self, i):
        """Regla 22: Asignación a Centro de Disposición Final."""
        print(f"[Centro Gestión] Residuo {i} asignado a 'CentroGestion_DisposicionFinal'.")
        self.declare(CentroGestion(id_residuo=i, centro="CentroGestion_DisposicionFinal"))
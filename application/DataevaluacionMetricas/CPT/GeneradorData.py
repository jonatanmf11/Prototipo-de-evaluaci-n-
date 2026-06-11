import json
import random

catalogo = [
    "Backlog del Producto",
    "Backlog del Sprint",
    "Historias de Usuario",
    "Casos de Uso",
    "Casos de Prueba",
    "Plan de Pruebas",
    "Informe de Pruebas",
    "Criterios de Aceptación",
    "Plan de Liberación",
    "Plan de Iteración",
    "Plan del Proyecto",
    "Cronograma del Proyecto",
    "Especificación de Requisitos",
    "Documento de Requisitos",
    "Documento de Arquitectura",
    "Bosquejo de Arquitectura",
    "Modelo de Datos",
    "Diagrama de Clases",
    "Diagrama de Secuencia",
    "Diagrama de Componentes",
    "Diagrama de Despliegue",
    "Matriz de Trazabilidad",
    "Registro de Riesgos",
    "Plan de Gestión de Riesgos",
    "Registro de Interesados",
    "Caso de Negocio",
    "Documento de Visión",
    "Hoja de Ruta del Producto",
    "Prototipo",
    "Maqueta de Interfaz",
    "Wireframe",
    "Manual de Usuario",
    "Manual Técnico",
    "Registro de Defectos",
    "Registro de Deuda Técnica",
    "Acta de Reunión",
    "Informe de Estado",
    "Documento de Diseño",
    "Especificación Funcional",
    "Especificación Técnica",
    "Modelo de Procesos",
    "Plan de Calidad",
    "Plan de Configuración",
    "Lecciones Aprendidas",
    "Definición de Hecho",
    "Definición de Preparado",
    "Solicitud de Cambio",
    "Registro de Cambios",
    "Documento de Validación",
    "Documento de Verificación"
]
casos = []

for i in range(1, 201):

    agile_size = random.randint(3, 10)
    plan_size = random.randint(3, 10)

    agile = set(random.sample(catalogo, agile_size))
    plan = set(random.sample(catalogo, plan_size))

    intersection = len(agile.intersection(plan))
    union = len(agile.union(plan))

    cpt = round(intersection / union, 9) if union > 0 else 0.0

    casos.append({
        "id": i,
        "agileWorkProducts": sorted(list(agile)),
        "planDrivenWorkProducts": sorted(list(plan)),
        "expectedIntersection": intersection,
        "expectedUnion": union,
        "expectedCPT": cpt
    })

with open("application/DataevaluacionMetricas/CPT/dataCPT.json", "w", encoding="utf-8") as f:
    json.dump(casos, f, indent=2, ensure_ascii=False)
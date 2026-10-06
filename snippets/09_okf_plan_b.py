# Plan B: builds the bundle from the notebook (not needed if you already uploaded okf.zip)
# The OKF content stays in Spanish: it is the company's knowledge base and must match okf.zip
import pathlib

OKF = pathlib.Path("okf")

OKF_FILES = {
'index.md': """---
type: Index
title: Base de conocimiento de NubeAndina Consulting
description: Punto de entrada para el agente. Empieza aquí y sigue los enlaces.
timestamp: 2026-10-05T00:00:00Z
---
# NubeAndina Consulting: base de conocimiento

- [Empresa: quiénes somos, servicios y tarifas](company/index.md)
- [AWS: fundamentos de servicios, costos de referencia y patrones](aws/index.md)
""",

'log.md': """---
type: Log
---
# Cambios

## 2026-10-05
- Se agregan los servicios de plataforma de recomendaciones en tiempo real y pipeline MLOps.
- Se agrega el patrón de recomendaciones en tiempo real.
""",

'company/index.md': """---
type: Index
title: Empresa
description: Quiénes somos, catálogo de servicios y tarifas oficiales.
---
# Empresa

- [Quiénes somos y condiciones comerciales](about.md)
- [Tarifas 2026: ÚNICA fuente válida de precios de consultoría](rate-card.md)
- [Catálogo de servicios](services/index.md)
""",

'company/about.md': """---
type: Company
title: NubeAndina Consulting
description: Consultora AWS ficticia para el laboratorio. Oficinas en Bogotá y Ciudad de México.
tags: [empresa, condiciones]
timestamp: 2026-10-01T00:00:00Z
---
# NubeAndina Consulting

Consultora ficticia especializada en arquitectura, datos y ML sobre AWS. Equipo en Bogotá y Ciudad de México.

## Cómo trabajamos
1. Assessment: entendemos la necesidad y el estado actual.
2. Diseño e implementación por fases, con entregas cada 2 semanas.
3. Operación gestionada opcional.

## Condiciones comerciales
- Precios en USD, sin impuestos.
- 50 % al inicio y 50 % a la entrega.
- Vigencia de la propuesta: 30 días.
- Los costos de AWS los paga el cliente directamente a AWS; no están incluidos en nuestras tarifas.
- Solo ofrecemos servicios sobre AWS. No ofrecemos servicios sobre Azure ni Google Cloud.
""",

'company/rate-card.md': """---
type: RateCard
title: Tarifas NubeAndina Consulting 2026
description: Precios oficiales de consultoría AWS. Única fuente válida de precios.
tags: [precios, consultoria]
timestamp: 2026-10-01T00:00:00Z
status: stable
stale_after: 2027-03-31
---
# Tarifas 2026 (USD)

| Servicio | Unidad | Precio |
| --- | --- | --- |
| [Assessment de arquitectura](services/assessment.md) | paquete 1 semana | 1,800 |
| [Plataforma de recomendaciones en tiempo real](services/realtime-recs-platform.md) | paquete MVP | 9,500 |
| [Pipeline MLOps: entrenamiento diario, orquestación y alertas](services/mlops-pipeline.md) | paquete | 7,000 |
| [Migración lift-and-shift](services/migration.md) | por workload | 4,500 |
| [Well-Architected Review](services/well-architected-review.md) | paquete | 2,200 |
| [Operación gestionada](services/managed-ops.md) | mensual | 900 |
| Arquitecto cloud senior | hora | 95 |

Cualquier servicio que no esté en esta tabla no se ofrece ni se cotiza.
""",

'company/services/index.md': """---
type: Index
title: Catálogo de servicios
description: Servicios de consultoría que ofrecemos. Precios en ../rate-card.md.
---
# Catálogo de servicios

- [Assessment de arquitectura](assessment.md): punto de partida de todo proyecto.
- [Plataforma de recomendaciones en tiempo real](realtime-recs-platform.md)
- [Pipeline MLOps](mlops-pipeline.md)
- [Migración lift-and-shift](migration.md)
- [Well-Architected Review](well-architected-review.md)
- [Operación gestionada](managed-ops.md)

Precios: [tarifas](../rate-card.md).
""",

'company/services/assessment.md': """---
type: Service
title: Assessment de arquitectura
description: Diagnóstico de 1 semana del estado actual y la arquitectura objetivo.
tags: [assessment, descubrimiento]
---
# Assessment de arquitectura

- Duración: 1 semana.
- Alcance: entrevistas, revisión de datos y sistemas actuales, requisitos no funcionales (latencia, costo, equipo).
- Entregables: arquitectura objetivo, plan por fases, estimación de costos AWS.
- Requisito previo para la [plataforma de recomendaciones](realtime-recs-platform.md) y el [pipeline MLOps](mlops-pipeline.md).
- Precio: ver [tarifas](../rate-card.md).
""",

'company/services/realtime-recs-platform.md': """---
type: Service
title: Plataforma de recomendaciones en tiempo real
description: MVP de inferencia en línea con contexto, sobre servicios administrados de AWS.
tags: [ml, recomendaciones, tiempo-real]
---
# Plataforma de recomendaciones en tiempo real (paquete MVP)

- Duración: 6 a 8 semanas.
- Alcance:
  - Feature store de baja latencia en DynamoDB.
  - Grafo miembro-clase-instructor en Neptune para generar candidatos.
  - Endpoint de inferencia en SageMaker (sin Kubernetes).
  - API de recomendaciones (API Gateway + Lambda) con objetivo de latencia < 200 ms.
  - Registro de eventos (MSK Serverless o Kinesis) hacia S3 para reentrenar.
- No incluye: el pipeline de entrenamiento y orquestación (ver [Pipeline MLOps](mlops-pipeline.md)).
- Patrón de referencia: [recomendaciones en tiempo real](../../aws/patterns/recomendaciones-tiempo-real.md).
- Precio: ver [tarifas](../rate-card.md).
""",

'company/services/mlops-pipeline.md': """---
type: Service
title: Pipeline MLOps
description: Entrenamiento diario automatizado, registro de modelos, orquestación y alertas.
tags: [ml, mlops, orquestacion]
---
# Pipeline MLOps

- Duración: 3 a 4 semanas (puede ir en paralelo con la plataforma).
- Alcance: preprocesamiento en EMR (Spark), entrenamiento en SageMaker, registro de modelos,
  orquestación con Amazon MWAA (Airflow) y alertas de fallo con CloudWatch + SNS.
- Precio: ver [tarifas](../rate-card.md).
""",

'company/services/migration.md': """---
type: Service
title: Migración lift-and-shift
description: Mover un workload existente a AWS sin rediseñarlo.
tags: [migracion]
---
# Migración lift-and-shift

- Duración: 2 a 3 semanas por workload.
- Alcance: inventario, migración a EC2/RDS, pruebas y corte.
- Precio: por workload, ver [tarifas](../rate-card.md).
""",

'company/services/managed-ops.md': """---
type: Service
title: Operación gestionada
description: Operación mensual de la plataforma después del go-live.
tags: [operacion, soporte]
---
# Operación gestionada

- Monitoreo 8x5, respuesta a incidentes, parches y reporte mensual de costos.
- Precio: mensual, ver [tarifas](../rate-card.md).
""",

'company/services/well-architected-review.md': """---
type: Service
title: Well-Architected Review
description: Revisión de una carga existente contra el AWS Well-Architected Framework.
tags: [revision, buenas-practicas]
---
# Well-Architected Review

- Duración: 1 a 2 semanas.
- Alcance: revisión de los seis pilares del AWS Well-Architected Framework (excelencia operacional,
  seguridad, confiabilidad, eficiencia de rendimiento, optimización de costos y sostenibilidad).
- Entregables: informe de riesgos priorizados y plan de remediación.
- Precio: ver [tarifas](../rate-card.md).
""",

'aws/index.md': """---
type: Index
title: AWS
description: Fundamentos de servicios, costos de referencia y patrones de arquitectura.
---
# AWS

- [Fundamentos de servicios](basics/index.md)
- [Costos de referencia (ilustrativos)](basics/pricing-models.md)
- [Patrón: recomendaciones en tiempo real](patterns/recomendaciones-tiempo-real.md)
""",

'aws/basics/index.md': """---
type: Index
title: Fundamentos de servicios AWS
description: Una ficha por servicio usado en nuestras propuestas.
---
# Fundamentos

- [Amazon S3](s3.md): almacenamiento de objetos, data lake.
- [Amazon EMR](emr.md): Spark administrado para preprocesar datos.
- [Amazon DynamoDB](dynamodb.md): clave-valor de baja latencia, feature store.
- [Amazon Neptune](neptune.md): base de datos de grafos.
- [Amazon MSK](msk.md): Kafka administrado para eventos.
- [Amazon SageMaker](sagemaker.md): entrenamiento y endpoints de inferencia.
- [Amazon EKS](eks.md): Kubernetes administrado.
- [Amazon MWAA](mwaa.md): Airflow administrado.
- [Costos de referencia](pricing-models.md)
""",

'aws/basics/s3.md': """---
type: Concept
title: Amazon S3
tags: [almacenamiento, data-lake]
resource: https://aws.amazon.com/s3/
---
# Amazon S3
Almacenamiento de objetos. Se usa como data lake del historial y destino de eventos para reentrenar.
Cobro por GB almacenado al mes y por solicitudes.
""",

'aws/basics/emr.md': """---
type: Concept
title: Amazon EMR
tags: [spark, batch]
resource: https://aws.amazon.com/emr/
---
# Amazon EMR
Clústeres Spark administrados (o EMR Serverless). Ideal para preprocesar el historial diario y poblar
el feature store y el grafo. Cobro por hora de cómputo; los jobs diarios cortos mantienen el costo bajo.
""",

'aws/basics/dynamodb.md': """---
type: Concept
title: Amazon DynamoDB
tags: [nosql, baja-latencia, feature-store]
resource: https://aws.amazon.com/dynamodb/
---
# Amazon DynamoDB
Base clave-valor totalmente administrada, latencia de milisegundos de un dígito.
Patrón común como feature store en línea. Modo on-demand: se paga por lectura/escritura.
""",

'aws/basics/neptune.md': """---
type: Concept
title: Amazon Neptune
tags: [grafo]
resource: https://aws.amazon.com/neptune/
---
# Amazon Neptune
Base de datos de grafos administrada. Modela miembros, clases e instructores como nodos y las clases
tomadas como aristas, para generar candidatos de recomendación. Existe en modo serverless.
""",

'aws/basics/msk.md': """---
type: Concept
title: Amazon MSK
tags: [streaming, eventos, kafka]
resource: https://aws.amazon.com/msk/
---
# Amazon MSK
Apache Kafka administrado. MSK Serverless evita dimensionar brokers. Alternativa más simple para
equipos pequeños: Amazon Kinesis Data Streams.
""",

'aws/basics/sagemaker.md': """---
type: Concept
title: Amazon SageMaker
tags: [ml, inferencia, entrenamiento]
resource: https://aws.amazon.com/sagemaker/
---
# Amazon SageMaker
Entrenamiento administrado, registro de modelos y endpoints de inferencia en tiempo real con autoescalado.
Recomendado para equipos sin experiencia en Kubernetes: no hay clústeres que operar.
""",

'aws/basics/eks.md': """---
type: Concept
title: Amazon EKS
tags: [kubernetes, contenedores]
resource: https://aws.amazon.com/eks/
---
# Amazon EKS
Kubernetes administrado. Muy flexible (por ejemplo, GPUs para entrenamiento), pero requiere un equipo con
experiencia en Kubernetes para operarlo. Si el cliente no la tiene, preferir SageMaker.
""",

'aws/basics/mwaa.md': """---
type: Concept
title: Amazon MWAA
tags: [orquestacion, airflow]
resource: https://aws.amazon.com/managed-workflows-for-apache-airflow/
---
# Amazon MWAA
Apache Airflow administrado para orquestar el pipeline diario (preprocesar, entrenar, registrar, desplegar),
con reintentos y alertas.
""",

'aws/basics/pricing-models.md': """---
type: Concept
title: Costos AWS de referencia para un MVP de recomendaciones
description: Valores ILUSTRATIVOS para el laboratorio. No son una cotización de AWS.
tags: [precios-aws, estimacion]
timestamp: 2026-10-05T00:00:00Z
status: draft
---
# Costos AWS de referencia (ilustrativos)

Escenario: ~200.000 miembros, inferencia en línea < 200 ms, reentrenamiento diario.
Valores aproximados en USD por mes, solo para el laboratorio. Validar siempre con AWS Pricing Calculator.

| Servicio | Uso supuesto | USD/mes (rango) |
| --- | --- | --- |
| S3 | 4 TB de historial + eventos | 90 – 120 |
| DynamoDB | feature store on-demand | 300 – 600 |
| Neptune | grafo, serverless pequeño | 400 – 800 |
| SageMaker | 2 instancias de endpoint + entrenamiento diario | 500 – 900 |
| API Gateway + Lambda | API de recomendaciones | 100 – 250 |
| MSK Serverless o Kinesis | eventos de recomendaciones | 300 – 800 |
| EMR | jobs Spark diarios | 300 – 700 |
| MWAA | entorno pequeño | 350 – 450 |
| CloudWatch + SNS | métricas, logs, alertas | 50 – 150 |
| **Total estimado** | | **2,390 – 4,770** |
""",

'aws/patterns/recomendaciones-tiempo-real.md': """---
type: Pattern
title: Patrón de recomendaciones en tiempo real
description: Arquitectura de referencia inspirada en el caso público de Peloton en AWS.
tags: [ml, recomendaciones, referencia]
resource: https://www.youtube.com/watch?v=ym_Gz_zH7w8
---
# Patrón: recomendaciones en tiempo real

Referencia pública: Peloton, serie "This Is My Architecture" de AWS.

## Ruta batch (diaria)
1. Historial de miembros en S3.
2. Preprocesamiento con Spark en EMR; los mismos jobs pueblan el feature store y el grafo.
3. Entrenamiento (en el caso de referencia, en EKS con GPUs) y registro del modelo.
4. Orquestación con Airflow en MWAA.

## Ruta en línea (cada vez que el miembro inicia una sesión)
1. El dispositivo llama a un servicio que pide las recomendaciones.
2. Un orquestador obtiene features (DynamoDB), candidatos (grafo) y el modelo vigente.
3. Un servicio de inferencia puntúa los candidatos y devuelve la lista ordenada.
4. Lo recomendado se registra como evento (MSK) y llega a S3: ciclo de retroalimentación para reentrenar.

## Variante para equipos pequeños
- Sin experiencia en Kubernetes: reemplazar EKS por entrenamiento y endpoints de SageMaker.
- MSK Serverless o Kinesis Data Streams en lugar de un clúster MSK dimensionado a mano.
- Servicios de consultoría que lo implementan: [plataforma](../../company/services/realtime-recs-platform.md)
  y [pipeline MLOps](../../company/services/mlops-pipeline.md).
""",

}

for path, content in OKF_FILES.items():
    dest = OKF / path
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(content, encoding="utf-8")

print(f"{len(OKF_FILES)} OKF files written to {OKF.resolve()}")
!find okf -name '*.md' | sort

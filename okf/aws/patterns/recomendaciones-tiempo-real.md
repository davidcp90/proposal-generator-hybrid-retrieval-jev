---
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

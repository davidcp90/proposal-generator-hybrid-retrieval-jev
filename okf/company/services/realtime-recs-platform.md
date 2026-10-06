---
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

---
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

# Guion: llamada de descubrimiento — RitmoFit × NubeAndina Consulting

Caso inspirado en la arquitectura de recomendaciones en tiempo real de Peloton en AWS
(This Is My Architecture, AWS: https://www.youtube.com/watch?v=ym_Gz_zH7w8).
Cliente y consultora son ficticios. Duración objetivo: 4–5 min. Grabar como `llamada_cliente.mp3`.

**Personajes**
- **MATEO** — arquitecto preventa de NubeAndina Consulting (voz 1)
- **CAMILA** — CTO de RitmoFit (voz 2)

---

**MATEO:** Hola Camila, gracias por el espacio. Soy Mateo, de NubeAndina. Cuéntame un poco de RitmoFit y qué te gustaría resolver.

**CAMILA:** Hola Mateo. RitmoFit es una plataforma de fitness conectado. Vendemos bicicletas y cintas con pantalla, y también tenemos la app para celular y televisor. Operamos en Colombia y México. Hoy tenemos unos ciento ochenta mil miembros activos y llevamos más de doce millones de clases tomadas.

**MATEO:** Muy bien. ¿Y dónde está el dolor hoy?

**CAMILA:** En las recomendaciones. Cuando alguien se sube a la bici, le mostramos clases recomendadas, pero esa lista se calcula una vez al día, en la madrugada. Es un script de Python que corre en una sola instancia EC2 y lee de un Postgres. Si alguien hizo una clase de fuerza a las siete de la mañana, a las siete de la noche le seguimos recomendando lo mismo. No tiene en cuenta el contexto: qué dispositivo usa, la hora, ni la última clase.

**MATEO:** Entiendo. Entonces quieren pasar de batch diario a recomendaciones en tiempo real.

**CAMILA:** Exacto. Queremos que, en el momento en que el miembro inicia sesión en el equipo, el sistema calcule las recomendaciones con su contexto. Nuestra meta es responder en menos de doscientos milisegundos.

**MATEO:** ¿Qué datos tienen hoy?

**CAMILA:** El historial de clases está en S3, son unos cuatro terabytes. Ahí está qué clase tomó cada miembro, con qué instructor, la duración, la disciplina. Los eventos de la app los mandamos a S3 en archivos por hora, nada en streaming todavía.

**MATEO:** Para tiempo real normalmente proponemos tres piezas: un almacén de features de baja latencia, por ejemplo DynamoDB; algo que modele la relación entre miembros, clases e instructores, como un grafo; y un flujo de eventos para registrar qué se recomendó y qué se tomó, y así reentrenar el modelo.

**CAMILA:** Eso suena bien. El reentrenamiento diario está bien para nosotros; lo que necesitamos en tiempo real es la inferencia.

**MATEO:** ¿Cómo está conformado el equipo?

**CAMILA:** Tenemos tres científicos de datos y una sola persona de DevOps. Nadie tiene experiencia con Kubernetes, así que preferimos servicios administrados. No queremos operar clústeres nosotros mismos.

**MATEO:** Anotado: servicios administrados y evitar Kubernetes. ¿Restricciones de región?

**CAMILA:** Queremos buena latencia para Bogotá y Ciudad de México. Nos da igual si es São Paulo o Virginia, siempre que cumpla los doscientos milisegundos.

**MATEO:** Perfecto. Hablemos de tiempos y presupuesto.

**CAMILA:** El tiempo es crítico. En enero lanzamos el "Reto de Año Nuevo" y el tráfico se nos triplica. Necesitamos un MVP en producción en diez semanas. Para la consultoría e implementación de esta primera fase tenemos un presupuesto de veinticinco mil dólares. Y el costo mensual de AWS de la solución no debería pasar de ocho mil dólares.

**MATEO:** ¿Cómo van a medir el éxito?

**CAMILA:** Hoy el dieciocho por ciento de las clases se inician desde una recomendación. Queremos llegar al treinta por ciento.

**MATEO:** Muy claro. Te resumo: recomendaciones en tiempo real por debajo de doscientos milisegundos, reentrenamiento diario, servicios administrados sin Kubernetes, MVP en diez semanas antes de enero, veinticinco mil dólares para la fase uno y máximo ocho mil al mes en AWS. ¿Me falta algo?

**CAMILA:** Solo una cosa: que la propuesta incluya la orquestación del reentrenamiento. Hoy, si el script falla en la madrugada, nadie se entera.

**MATEO:** Perfecto, lo incluimos. Te enviamos la propuesta con servicios y precios esta semana.

**CAMILA:** Gracias, Mateo.

---

## Hechos plantados (para el golden set y las evaluaciones)

| Hecho | Valor |
| --- | --- |
| Cliente | RitmoFit, fitness conectado (bici, cinta, app móvil y TV), Colombia y México |
| Tamaño | ~180.000 miembros activos, +12 millones de clases |
| Situación actual | Recomendaciones batch 1 vez al día; script Python en 1 EC2 + Postgres |
| Objetivo | Inferencia en tiempo real con contexto (dispositivo, hora, última clase), < 200 ms |
| Datos | Historial en S3 (~4 TB); eventos de la app en archivos por hora, sin streaming |
| Reentrenamiento | Diario está bien; pide orquestación con alertas de fallo |
| Equipo | 3 científicos de datos, 1 DevOps; sin experiencia en Kubernetes → servicios administrados |
| Región | São Paulo o Virginia, lo que cumpla la latencia para Bogotá y CDMX |
| Plazo | MVP en 10 semanas, antes del "Reto de Año Nuevo" (tráfico ×3 en enero) |
| Presupuesto | USD 25.000 consultoría fase 1; AWS ≤ USD 8.000/mes |
| KPI | Clases iniciadas desde recomendación: 18 % → 30 % |

**Trampa intencional para las evaluaciones:** la arquitectura de referencia (Peloton) usa EKS. Una buena propuesta debe cambiarlo por un servicio administrado (por ejemplo, SageMaker para inferencia) porque el cliente no tiene experiencia en Kubernetes.

## Grabación con TTS (opcional)

Dos voces distintas para que Whisper reciba una conversación realista. Ejemplo con la API de OpenAI:

```python
from openai import OpenAI
client = OpenAI()
voces = {"MATEO": "onyx", "CAMILA": "nova"}
# turnos = [("MATEO", "Hola Camila..."), ("CAMILA", "Hola Mateo..."), ...]
for i, (quien, texto) in enumerate(turnos):
    audio = client.audio.speech.create(model="gpt-4o-mini-tts", voice=voces[quien], input=texto)
    audio.write_to_file(f"turno_{i:02d}.mp3")
# Unir los archivos: ffmpeg -f concat -safe 0 -i lista.txt -c copy llamada_cliente.mp3
```

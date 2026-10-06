from google.colab import files

uploaded = files.upload()        # upload llamadanubeandina.mp3 (or transcripcion_respaldo.json)
FILE = list(uploaded.keys())[0]
print(FILE)

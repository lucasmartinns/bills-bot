import os
import json
from google.cloud import speech_v2
from google.cloud.speech_v2.types import cloud_speech

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./service_account.json"

def transcrever_local(caminho_audio: str, saida_json: str = "transcricao.json"):
    client = speech_v2.SpeechClient()

    with open(caminho_audio, "rb") as f:
        conteudo = f.read()

    config = cloud_speech.RecognitionConfig(
        auto_decoding_config={},
        features=cloud_speech.RecognitionFeatures(
            enable_word_confidence=True,
            enable_word_time_offsets=True,
        ),
        language_codes=["pt-BR"],
        model="latest_long",
    )

    request = cloud_speech.RecognizeRequest(
        recognizer="projects/milho2025/locations/global/recognizers/_",
        config=config,
        content=conteudo,
    )

    response = client.recognize(request=request)

    resultados = []
    for resultado in response.results:
        alternativas = []
        for alt in resultado.alternatives:
            alternativas.append({
                "transcricao": alt.transcript,
                "confianca": alt.confidence,
                "palavras": [
                    {
                        "texto": w.word,
                        "inicio": w.start_offset.total_seconds(),
                        "fim": w.end_offset.total_seconds(),
                        "confianca": w.confidence
                    }
                    for w in alt.words
                ]
            })
        resultados.append({"alternativas": alternativas})

    with open(saida_json, "w", encoding="utf-8") as f:
        json.dump({"resultados": resultados}, f, ensure_ascii=False, indent=2)

    print(f"Transcrição salva em {saida_json}")

if __name__ == "__main__":
    transcrever_local("./audios/audio1.opus", "transcricao.json")

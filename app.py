from flask import Flask, render_template, request, jsonify, redirect, url_for
import random
import json
import os

app = Flask(__name__)

# ==========================
#  CONFIGURACIÓN
# ==========================

DATA_1 = "data_app1.json"   # persona anterior
DATA_2 = "data_app2.json"   # chat nuevo (para ella)
MAX_MENSAJES = 8            # últimos mensajes que se guardan


# ==========================
#  FRASES POR EMOCIÓN
#  (sin nombres, igual de alfas)
# ==========================

EMOCIONES = {
    "ternura": [
        "Si existiera un botón para verte esos ojos ya lo hubiera roto por ti.",
        "Contigo no sé si hablar normal o tratarte bonito, ya el tiempo lo dirá.",
        "No sé si eres buena idea o mala idea… pero sí sé que me interesa averiguarlo.",
        "Hay mensajes bonitos… y luego está ese que espero que me mandes tú 😏",
        "A veces las conexiones llegan sin aviso… y esta se siente interesante."
    ],
    "risa": [
        "Prometo hacerte reír… pero no prometo que sea por chistoso, tal vez por menso 😂",
        "Si te hago reír 3 veces seguidas, me debes un abrazo.",
        "Si sigues aquí es porque te gusto… o porque no tienes nada mejor que hacer, ambas me sirven 😂",
        "Tranquila, no muerdo… bueno… depende de la situación 😈",
        "Yo soy como las notificaciones inesperadas: aparezco, sonríes y ya te distraigo 😎",
        "Prometo portarme bien… hasta que tú empieces con indirectas 😏",
        "Si te vuelves adicta a hablar conmigo… no es mi culpa, es mi talento 😌",
        "Yo no coqueteo… yo pruebo terreno. Si sonríes, continúo 😂",
        "Si después de leer esto te da risa… ahí ya te enamoraste tantito y ni modo 😈"
    ],
    "picante": [
        "Si te digo todo lo que quiero hacer cuando te vea… esta app se vuelve +18 😏",
        "De todas mis distracciones, tú puedes ser una de mis favoritas.",
        "No te voy a perseguir… pero si tú te acercas, tampoco me voy a hacer el santo 😌",
        "No soy intenso, soy claro, lo demás se descubre con calma… o sin ella 😏",
        "Si supieras lo que estoy pensando… estarías sonriendo nerviosa ahora mismo.",
        "No soy tu opción… soy ese problema que sabes que te va a gustar.",
        "No planeo impresionarte… planeo que lo sientas.",
        "Yo no juego a enamorar… juego a conectar. Lo demás pasa solo.",
        "No corro… pero tampoco voy lento. Yo voy al ritmo donde la cosa se pone peligrosa 😈"
    ],
    "sorpresa": [
        "Sorpresa: si llegaste hasta aquí, oficialmente sé que te empiezo a gustar. Ya no hay reembolso.",
        "Se rumora que quien lee esto debería aceptar una cita conmigo.",
        "No estoy tratando de impresionarte, estoy observando si tú vales mi tiempo.",
        "Si crees que ya me entendiste… estás lejos. Y por eso sigues aquí 😌",
        "No te voy a advertir nada… prefiero que lo descubras y luego entiendas por qué te avisé tarde 🔥",
        "Si ya sientes la curiosidad… no la frenes."
    ]
}


# ==========================
#  MANEJO DE ESTADO (JSON)
# ==========================

def load_state(file_path):
    """Carga historial desde el JSON correspondiente a cada app."""
    if not os.path.exists(file_path):
        return {"historial": []}

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            data = json.load(f)
    except Exception:
        data = {"historial": []}

    if "historial" not in data or not isinstance(data["historial"], list):
        data["historial"] = []

    return data


def save_state(file_path, historial):
    """Guarda el historial (recorta a los últimos N mensajes)."""
    data = {"historial": historial[-MAX_MENSAJES:]}
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)


# ==========================
#  VISTAS GENÉRICAS
# ==========================

def app_view(file_path, estado_endpoint):
    """
    Vista genérica para la app de ella.
    Cada app (1 o 2) llama a esto con su propio archivo y endpoint de estado.
    """
    state = load_state(file_path)
    historial = state["historial"]
    frase_generada = None

    if request.method == "POST":
        # Botones de emoción
        if "emocion" in request.form:
            emo = request.form["emocion"]
            if emo in EMOCIONES:
                frase_generada = random.choice(EMOCIONES[emo])

        # Pregunta de ella
        elif "pregunta" in request.form:
            texto = request.form["pregunta"].strip()
            if texto:
                historial.append({"de": "ella", "texto": texto})
                save_state(file_path, historial)

    return render_template(
        "index.html",
        frase_generada=frase_generada,
        estado_url=url_for(estado_endpoint),
    )


def miguel_view(file_path, estado_endpoint, self_endpoint):
    """
    Vista genérica para tu panel (Miguel).
    """
    state = load_state(file_path)
    historial = state["historial"]

    if request.method == "POST":
        respuesta = request.form.get("respuesta", "").strip()
        if respuesta:
            historial.append({"de": "miguel", "texto": respuesta})
            save_state(file_path, historial)

    # Volvemos a cargar (por si se recortó el historial)
    state = load_state(file_path)

    return render_template(
        "miguel.html",
        estado_url=url_for(estado_endpoint),
        post_url=url_for(self_endpoint),
    )


# ==========================
#  RUTAS APP 1 (persona anterior)
# ==========================

@app.route("/", methods=["GET", "POST"])
@app.route("/app1", methods=["GET", "POST"])
def app1():
    # Esta es la app que ya habías usado antes
    return app_view(DATA_1, "estado1")


@app.route("/miguel", methods=["GET", "POST"])
@app.route("/miguel_app1", methods=["GET", "POST"])
def miguel_app1():
    # Panel tuyo para la persona anterior
    return miguel_view(DATA_1, "estado1", "miguel_app1")


@app.route("/estado1")
def estado1():
    return jsonify(load_state(DATA_1))


# ==========================
#  RUTAS APP 2 (chat nuevo, para ella)
# ==========================

@app.route("/app2", methods=["GET", "POST"])
def app2():
    # App nueva, link que le vas a pasar a ella
    return app_view(DATA_2, "estado2")


@app.route("/miguel_app2", methods=["GET", "POST"])
def miguel_app2():
    # Panel tuyo privado para este segundo chat
    return miguel_view(DATA_2, "estado2", "miguel_app2")


@app.route("/estado2")
def estado2():
    return jsonify(load_state(DATA_2))


# ==========================

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

# Frases por emoción (igual que antes)
EMOCIONES = {
    "ternura": [
        "Si existiera un botón para verte esos ojos ya lo hubiera roto por ti Ketsally",
"Contigo no sé si hablar normal o tratarte bonito ya el tiempo lo dira",
"No sé si eres buena idea o mala idea… pero sí sé que me interesa averiguarlo.",
"Hay mensajes bonitos… y luego está ese que espero que me mandes tú 😏",
"A veces las conexiones llegan sin aviso… y esta se siente interesante."

    ],
    "risa": [
        "Prometo hacerte reír… pero no prometo que sea por chistoso, tal vez por menso 😂",
        "Si te hago reír 3 veces seguidas, me debes un abrazo.",
        "Si sigues aquí es porque te gusto… o porque no tienes nada mejor que hacer, ambas me sirven 😂",


"Tranquila, no muerdo… bueno… depende de la situación 😈",

"Si tienes buen sentido del humor, cuidado… porque luego eso se combina con química y ya sabes",

"Yo soy como las notificaciones inesperadas: aparezco, sonríes y ya te distraigo 😎",


"Prometo portarme bien… hasta que tú empieces con indirectas 😏",

"Si te vuelves adicta a hablar conmigo… no es mi culpa, es mi talento 😌",

"Yo no coqueteo… yo pruebo terreno. Si sonríes, continúo 😂",

"Si después de leer esto te da risa… ahí ya te enamoraste tantito y ni modo 😈"

    ],
    "picante": [
        "Si te digo todo lo que quiero hacer cuando te vea… esta app se vuelve +18 😏",
        
        "De todas mis distracciones, tu puedes ser una de mis favoritas."
        "No te voy a perseguir… pero si tú te acercas, tampoco me voy a hacer el santo 😌",

"No soy intenso, soy claro, lo demás se descubre con calma… o sin ella 😏",

"Si supieras lo que estoy pensando… estarías sonriendo nerviosa ahora mismo.",

"No soy tu opción… soy ese problema que sabes que te va a gustar.",


"No planeo impresionarte… planeo que lo sientas.",

"Yo no juego a enamorar… juego a conectar. Lo demás pasa solo.",


"No corro… pero tampoco voy lento. Yo voy al ritmo donde la cosa se pone peligrosa 😈"


    ],
    "sorpresa": [
        "Sorpresa: si llegaste hasta aquí, oficialmente se que te empiezo a gustar. Ya no hay reembolso.",
        "Se rumora que quien lee esto debería aceptar una cita conmigo."
        

"No estoy tratando de impresionarte Ketzally, estoy observando si tú vales mi tiempo.",

"Si crees que ya me entendiste… estás lejos. Y por eso sigues aquí 😌",

"No te voy a advertir nada… prefiero que lo descubras y luego entiendas por qué te avisé tarde 🔥",


"Si ya sientes la curiosidad… no la frenes"

    ]
}

# Aquí guardamos la última pregunta de ella y tu respuesta
ultima_pregunta = None
ultima_respuesta = None


@app.route("/", methods=["GET", "POST"])
def index():
    global ultima_pregunta, ultima_respuesta

    emocion_seleccionada = None
    frase_generada = None

    if request.method == "POST":
        # Botones de emoción
        if "emocion" in request.form:
            emocion_seleccionada = request.form["emocion"]
            if emocion_seleccionada in EMOCIONES:
                frase_generada = random.choice(EMOCIONES[emocion_seleccionada])

        # Pregunta de Ketzally
        elif "pregunta" in request.form:
            pregunta = request.form["pregunta"].strip()
            if pregunta:
                ultima_pregunta = pregunta
                ultima_respuesta = None  # borramos la anterior para que esperes contestar tú

    return render_template(
        "index.html",
        emocion_seleccionada=emocion_seleccionada,
        frase_generada=frase_generada,
        pregunta_ketzally=ultima_pregunta,
        respuesta_pregunta=ultima_respuesta
    )


@app.route("/miguel", methods=["GET", "POST"])
def miguel():
    """
    Página solo para ti, donde lees la pregunta y escribes tu respuesta.
    """
    global ultima_pregunta, ultima_respuesta

    if request.method == "POST":
        respuesta = request.form.get("respuesta", "").strip()
        if respuesta:
            ultima_respuesta = respuesta
            # Después de guardar la respuesta, te manda a la página principal
            return redirect(url_for("index"))

    return render_template(
        "miguel.html",
        pregunta_ketzally=ultima_pregunta,
        respuesta_pregunta=ultima_respuesta
    )


if __name__ == "__main__":
    app.run(debug=True)

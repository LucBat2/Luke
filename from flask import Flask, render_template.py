from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Proposta</title>
        <style>
            body {
                text-align: center;
                font-family: Arial, sans-serif;
                margin-top: 50px;
            }
            img {
                max-width: 300px;
                border-radius: 10px;
            }
            h1 {
                font-size: 2.5em;
                color: #333;
            }
            button {
                padding: 10px 20px;
                font-size: 1.2em;
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            button:hover {
                background-color: #0056b3;
            }
        </style>
    </head>
    <body>
        <h1>Aceita casar comigo?</h1>
        <img src="https://placekitten.com/300/300" alt="Gato fofo">
        <br><br>
        <button onclick="alert('Você disse sim!')">Sim</button>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(debug=True)

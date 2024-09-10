Python utilizando Flask, que é um framework leve e fácil de usar para APIs. O objetivo será criar uma API que:

  Receba um arquivo de áudio enviado pelo aplicativo.
  Converta o áudio em texto utilizando uma biblioteca de reconhecimento de fala.
  (Opcional) Converta o texto para Libras ou use uma API externa para fazer essa conversão.
  Retorne o resultado para o aplicativo cliente.


API REST utilizando o Flask para converter áudio em texto. Vamos dividir isso em partes e explicar o que cada uma faz.

1. Importação das Bibliotecas
   
  Python 
  from flask import Flask, request, jsonify
  import speech_recognition as sr
  import os

Flask: Framework que permite criar APIs de forma rápida e simples.
speech_recognition: Biblioteca para reconhecimento de fala (converte áudio em texto).
os: Módulo para manipulação de arquivos e caminhos de sistema.


3. Criação do Aplicativo Flask
  Python
  app = Flask(__name__)

  Essa linha cria uma instância do aplicativo Flask. O objeto app será usado para definir as rotas e configurar o servidor.

5. Função para Converter Áudio em Texto
   Python
  def convert_audio_to_text(audio_path):
      """Converte o arquivo de áudio para texto."""
      recognizer = sr.Recognizer()
      with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
          try:
            text = recognizer.recognize_google(audio, language='pt-BR')
        except sr.UnknownValueError:
            text = "Não foi possível reconhecer o áudio."
        except sr.RequestError:
            text = "Erro na requisição ao serviço de reconhecimento de fala."
    return text
   
sr.Recognizer: Inicializa o objeto reconhecedor de fala.
sr.AudioFile: Carrega o arquivo de áudio para processamento.
recognizer.recognize_google: Usa o serviço de reconhecimento de fala do Google para converter o áudio em texto.


7. Rota para Receber e Processar o Áudio
python
  @app.route('/convert', methods=['POST'])
  def convert_audio():
    if 'file' not in request.files:
        return jsonify({"error": "Arquivo de áudio não encontrado."}), 400

    file = request.files['file']
    audio_path = os.path.join('temp', file.filename)
    file.save(audio_path)

    text = convert_audio_to_text(audio_path)
    
    # Limpa o arquivo temporário
    os.remove(audio_path)

    return jsonify({"text": text})
   
@app.route('/convert', methods=['POST']): Define a rota /convert para aceitar requisições POST.
Verifica se o arquivo de áudio foi enviado na requisição. Se não, retorna um erro.
Salva o arquivo de áudio temporariamente no diretório temp.
Converte o áudio em texto chamando a função convert_audio_to_text.
Remove o arquivo de áudio temporário após o processamento.
Retorna o texto convertido como uma resposta JSON.


9. Executando o Servidor Flask
python
if __name__ == '__main__':
    app.run(debug=True)
   
*Inicia o servidor Flask no modo de debug (útil durante o desenvolvimento).
**Como Utilizar o Código**

1-Salvar o Código

*Crie um arquivo chamado app.py no diretório do seu projeto e cole o código completo nele.

2-Criar o Diretório para Arquivos Temporários

*No mesmo diretório onde está o app.py, crie um diretório chamado temp para armazenar temporariamente os arquivos de áudio:

  (Terminal)
  mkdir temp
  
3-Executar o Servidor

Com o ambiente virtual ativado, execute o servidor Flask:

(terminal)
python app.py
Você verá uma mensagem indicando que o servidor está rodando em http://127.0.0.1:5000/.

4-Testar a API com uma Ferramenta HTTP

Use uma ferramenta como o Postman ou cURL para enviar um arquivo de áudio para o servidor:

Postman:
Selecione o método POST.
Use a URL http://127.0.0.1:5000/convert.
Vá para a aba "Body" e escolha "form-data".
Adicione um campo key chamado file e selecione um arquivo de áudio (.wav ou .mp3).
Clique em "Send".
Verificar a Resposta

Você deve receber uma resposta JSON com o texto convertido do áudio.

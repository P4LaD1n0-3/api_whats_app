from flask import Flask, request,jsonify
from util import identificar_tipo_mensagem, generateMessage

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return "simple page home!"



@app.route('/whatsapp', methods=['GET', 'POST'])
def verifyToken():
    try:
      
        acessToken = '98ZeEcfXDt1MHiB7lsCqqpFqqpYmGmYmI7e7cqQxOzRT4ApSU5o2Ck9i4Q4VOjpo'
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if request.method == 'GET':
            if token and challenge and token == acessToken:
                return challenge
            else:
                return "EVENT_RECEIVED"
        elif request.method == 'POST':
     
            # Acessar dados específicos
            data = request.get_json()
            message_content = identificar_tipo_mensagem(data)
            
            message_type = message_content['message_type']
            content_type = message_content['content_type']
            content = message_content['content']
            

            
            number_phone = "5543999920340"
            number_phone1 = "554398354970"
            number_phone2 = "5543988725270"
            
            print(message_type)    
            print(content_type)
            print(content)


            generateMessage(number_phone, message_type, content_type, content)
            
            return "EVENT_RECEIVED"
                
            #return jsonify(status='success'), 200
    
    
    except Exception as exception:
        print(exception)
        return str(exception), 400



if __name__ == "__main__":
    app.run(port=8000)

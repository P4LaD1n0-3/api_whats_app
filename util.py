import requests
import json


def enviar_mensagem_whatsapp(token, phone_number_id, number_phone, message_type, type, message ):
    url = f"https://graph.facebook.com/v13.0/{phone_number_id}/messages"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": number_phone,
        "type": f"{message_type}",
        f"{message_type}": {
            f"{type}": message
        }
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        print("Mensagem enviada com sucesso!")
    else:
        print(f"Erro ao enviar mensagem: {response.status_code}")
        print(response.json())


def generateMessage(number_phone, message, type, message_type):

    # Exemplo de uso
    token = "EAAMReAkLJKwBOxfKCZAaj2bCtMHwKwGzyZB72LxS1cgBYDIRI5lh5KDVj9xc48Gzw5ZCibAXJJspNoOmBAmRn0xXNPZB4ZBsZA9XvSHrrr3rdBaGZBq8rPsFfwUl1X5tl4SHlVvkT9ybEa8nEutyDIcGn3EwMfHSNFEO813PKZAyrG2Impqt9b2XIPBwBZCj1Ds4C"
    phone_number_id = "316435644895442"
    enviar_mensagem_whatsapp(token, phone_number_id,
                             number_phone, message, type, message_type)


def identificar_tipo_mensagem(data):
    try:
        message = data['entry'][0]['changes'][0]['value']['messages'][0]
        type = message['type']

        # Lista de tuplas com tipos de mensagem e chaves correspondentes
        types_messages = [
            ('text', 'text', 'body'),
            ('image', 'image', 'link'),
            ('video', 'video', 'link'),
            ('audio', 'audio', 'link'),
            ('document', 'document', 'link'),
            ('sticker', 'sticker', 'link'),
            ('location', 'location', ('latitude', 'longitude')),
            ('contact', 'contact', 'name')
        ]

        for tipo_msg, chave_primaria, chave_secundaria in types_messages:
            if type == tipo_msg:
                if type == 'location':
                    return {
                        'latitude': message[chave_primaria]['latitude'],
                        'longitude': message[chave_primaria]['longitude']
                    }
                return {
                    'message_type': tipo_msg,
                    'content_type': 'link' if 'link' in chave_secundaria else 'body',
                    'content': message[chave_primaria][chave_secundaria]
                }

    except KeyError as e:
        return f"Erro na estrutura da mensagem: {e}"

import json
import jwt

def lambda_handler(event, context):
    secret_key = 'secret-key'
    
    # Data payload you want to encode
    payload = {
        'user_id': 123,
        'email': 'user@example.com'
    }

    try:
        # Encoding the payload with the secret key
        encoded_jwt = jwt.encode(payload, secret_key, algorithm='HS256')
        print(f"Encoded JWT: {encoded_jwt}")

        # Decoding the payload with the secret key
        decoded_jwt = jwt.decode(encoded_jwt, secret_key, algorithms=['HS256'])
        print(f"Decoded JWT: {decoded_jwt}")

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'JWT encoded and decoded successfully!',
                'encoded': encoded_jwt,
                'decoded': decoded_jwt
            })
        }

    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'An error occurred',
                'error': str(e)
            })
        }

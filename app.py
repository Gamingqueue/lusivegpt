
from flask import Flask, request, jsonify, render_template
import json
import os
from totp_generator import generate_totp_code, validate_key, get_key_info

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-code', methods=['POST'])
def get_code():
    data = request.json
    user_key = data.get('key')

    if not user_key:
        return jsonify({'error': 'Key is required'}), 400

    # Get key info for better error messages
    key_info = get_key_info(user_key)
    
    if not key_info.get('exists', False):
        return jsonify({'error': 'Invalid key provided'}), 403
    
    if not key_info.get('is_valid', False):
        max_uses = key_info.get('max_uses', 1)
        usage_count = key_info.get('usage_count', 0)
        if max_uses == -1:
            return jsonify({'error': 'Key validation failed'}), 403
        else:
            return jsonify({'error': f'Key has reached its usage limit ({usage_count}/{max_uses} uses)'}), 403

    code, error = generate_totp_code(user_key)
    if error:
        return jsonify({'error': error}), 500
    
    # Get updated key info after usage
    updated_key_info = get_key_info(user_key)
    remaining = updated_key_info.get('remaining_uses', 0)
    
    response_data = {
        'code': code, 
        'success': True,
        'usage_info': {
            'max_uses': updated_key_info.get('max_uses'),
            'usage_count': updated_key_info.get('usage_count'),
            'remaining_uses': remaining
        }
    }
    
    return jsonify(response_data)

@app.route('/validate-key', methods=['POST'])
def validate_key_endpoint():
    data = request.json
    user_key = data.get("key")
    
    if not user_key:
        return jsonify({'valid': False, 'message': 'Key is required'})
    
    key_info = get_key_info(user_key)
    
    if not key_info.get('exists', False):
        return jsonify({'valid': False, 'message': 'Invalid key provided'})
    
    is_valid = key_info.get('is_valid', False)
    max_uses = key_info.get('max_uses', 1)
    usage_count = key_info.get('usage_count', 0)
    remaining = key_info.get('remaining_uses', 0)
    
    if is_valid:
        if max_uses == -1:
            message = 'Key is valid and has unlimited uses'
        else:
            message = f'Key is valid ({remaining} uses remaining out of {max_uses})'
        return jsonify({
            'valid': True, 
            'message': message,
            'usage_info': {
                'max_uses': max_uses,
                'usage_count': usage_count,
                'remaining_uses': remaining
            }
        })
    else:
        if max_uses == -1:
            message = 'Key validation failed'
        else:
            message = f'Key has reached its usage limit ({usage_count}/{max_uses} uses)'
        return jsonify({
            'valid': False, 
            'message': message,
            'usage_info': {
                'max_uses': max_uses,
                'usage_count': usage_count,
                'remaining_uses': remaining
            }
        })

@app.route('/key-info', methods=['POST'])
def key_info_endpoint():
    """Get detailed information about a key"""
    data = request.json
    user_key = data.get("key")
    
    if not user_key:
        return jsonify({'error': 'Key is required'}), 400
    
    key_info = get_key_info(user_key)
    
    if not key_info.get('exists', False):
        return jsonify({'error': 'Key not found'}), 404
    
    return jsonify(key_info)

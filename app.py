from flask import Flask, request, jsonify
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Your actual credentials
ACUMBAMAIL_TOKEN = "a2f90a65fd8b4cc9bbf041d40ddc3e26"
ACUMBAMAIL_LIST_ID = "1154863"

@app.route('/')
def home():
    return "Webhook server is running! ✅"

@app.route('/webhook', methods=['GET', 'POST'])
def handle_webhook():
    if request.method == 'GET':
        return jsonify({"message": "Webhook endpoint is working! Use POST to send data."}), 200
    
    try:
        data = request.get_json()
        logger.info(f"Received webhook data: {data}")
        
        # Extract email from readable_data
        email = None
        if 'readable_data' in data and 'Email' in data['readable_data']:
            email = data['readable_data']['Email']
        
        if not email:
            logger.error("No email found in readable_data!")
            return jsonify({"error": "No email found"}), 400
        
        logger.info(f"Processing email: {email}")
        
        # Add to Acumbamail
        success = add_to_acumbamail(email)
        
        if success:
            logger.info(f"✅ Successfully added {email} to Acumbamail")
            return jsonify({"status": "success", "email": email}), 200
        else:
            logger.error(f"❌ Failed to add {email} to Acumbamail")
            return jsonify({"status": "error"}), 500
            
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500
def add_to_acumbamail(email):
    url = "https://acumbamail.com/api/1/addSubscriber/"
    
    payload = {
        'auth_token': ACUMBAMAIL_TOKEN,
        'list_id': ACUMBAMAIL_LIST_ID,
        'email': email
    }
    
    try:
        logger.info(f"Sending to Acumbamail: {email}")
        response = requests.post(url, data=payload, timeout=15)
        logger.info(f"Acumbamail response: {response.status_code} - {response.text}")
        
        return response.status_code == 200
        
    except requests.RequestException as e:
        logger.error(f"Acumbamail API error: {str(e)}")
        return False
        
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    print("🚀 Starting webhook server...")
    print(f"Server running on port {port}")

    app.run(debug=False, host='0.0.0.0', port=port)




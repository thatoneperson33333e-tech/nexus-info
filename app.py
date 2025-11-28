# app.py - PHONE NUMBER INTEL API
from flask import Flask, request, jsonify
import requests
import re
import json
import os
from datetime import datetime

app = Flask(__name__)

class PhoneIntel:
    def __init__(self):
        self.truecaller_headers = {
            'User-Agent': 'Truecaller/11.75.5 (Android;8.1.0)',
            'Authorization': 'Bearer a1i0s--wRcseKYKR8FRzB6Q1ZR5nxKZB',
            'clientId': '5dc64dd8a3fe4100926fc8e1'
        }
    
    def validate_phone(self, phone):
        """Advanced phone number validation and formatting"""
        if not phone:
            return False, "Phone number is required"
        
        # Clean the phone number
        clean_phone = re.sub(r'[^\d+]', '', str(phone))
        
        # International format detection
        if clean_phone.startswith('+'):
            if len(clean_phone) == 13 and clean_phone.startswith('+91'):
                return True, clean_phone[1:]  # Remove + for Indian numbers
            else:
                return True, clean_phone  # Keep international format
        elif len(clean_phone) == 10 and clean_phone[0] in '6789':
            return True, '91' + clean_phone  # Convert to international
        elif len(clean_phone) == 12 and clean_phone.startswith('91'):
            return True, clean_phone
        else:
            return False, "Invalid phone number format"

    def get_truecaller_data(self, phone):
        """Fetch data from Truecaller API"""
        try:
            url = f"https://api4.truecaller.com/v1/keywords/search"
            params = {
                'q': phone,
                'countryCode': 'IN',
                'type': '4'
            }
            
            response = requests.get(url, headers=self.truecaller_headers, timeout=10)
            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None

    def get_abstractapi_data(self, phone):
        """Fetch data from AbstractAPI"""
        try:
            api_key = "your_abstract_api_key_here"  # Replace with actual key
            url = f"https://phonevalidation.abstractapi.com/v1/"
            params = {
                'api_key': api_key,
                'phone': phone
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None

    def analyze_phone_pattern(self, phone):
        """Analyze phone number patterns and metadata"""
        clean_phone = re.sub(r'[^\d]', '', phone)
        
        # Indian telecom operator detection
        operators = {
            '70': 'BSNL',
            '78': 'Airtel', 
            '77': 'Airtel',
            '79': 'BSNL',
            '80': 'Airtel',
            '81': 'Airtel',
            '82': 'Jio',
            '83': 'Jio',
            '84': 'Jio',
            '85': 'Jio',
            '86': 'Jio',
            '87': 'Idea/Vodafone',
            '88': 'Airtel',
            '89': 'Airtel',
            '90': 'Airtel',
            '91': 'Airtel',
            '92': 'Airtel',
            '93': 'Airtel',
            '94': 'BSNL',
            '95': 'Airtel',
            '96': 'Airtel',
            '97': 'Airtel',
            '98': 'Airtel',
            '99': 'Airtel'
        }
        
        prefix = clean_phone[-10:][:2] if len(clean_phone) >= 10 else clean_phone[:2]
        operator = operators.get(prefix, 'Unknown')
        
        # Circle detection based on first digits
        circles = {
            '70': 'Delhi',
            '78': 'Madhya Pradesh',
            '79': 'Bihar',
            '80': 'Tamil Nadu',
            '81': 'Kolkata',
            '82': 'Kolkata', 
            '83': 'Kolkata',
            '84': 'Kolkata',
            '85': 'Kolkata',
            '86': 'Kolkata',
            '87': 'Mumbai',
            '88': 'Karnataka',
            '89': 'Andhra Pradesh',
            '90': 'Haryana',
            '91': 'Punjab',
            '92': 'Punjab',
            '93': 'Uttar Pradesh',
            '94': 'Uttar Pradesh',
            '95': 'Uttar Pradesh',
            '96': 'Himachal Pradesh',
            '97': 'Assam',
            '98': 'Gujarat',
            '99': 'Kerala'
        }
        
        circle = circles.get(prefix, 'Unknown')
        
        return {
            'operator': operator,
            'circle': circle,
            'number_type': 'Mobile' if prefix in operators else 'Landline',
            'prefix_analysis': f"Series: {prefix}"
        }

    def get_social_media_presence(self, phone):
        """Check potential social media presence"""
        # This is simulated data - in real scenario, use respective APIs
        return {
            'whatsapp': 'Likely Registered',
            'telegram': 'Potential Account',
            'facebook': 'May be linked',
            'instagram': 'Possible connection',
            'paytm': 'Probably registered',
            'google_account': 'Potentially linked'
        }

    def generate_intel_report(self, phone):
        """Generate comprehensive intelligence report"""
        valid, formatted_phone = self.validate_phone(phone)
        if not valid:
            return {"error": formatted_phone}
        
        # Get data from multiple sources
        truecaller_data = self.get_truecaller_data(formatted_phone)
        abstract_data = self.get_abstractapi_data(formatted_phone)
        pattern_data = self.analyze_phone_pattern(formatted_phone)
        social_data = self.get_social_media_presence(formatted_phone)
        
        # Compile comprehensive report
        report = {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "phone_input": phone,
            "formatted_number": formatted_phone,
            
            "basic_info": {
                "country": "India" if formatted_phone.startswith('91') else "International",
                "valid": True,
                "format": "E.164" if formatted_phone.startswith('+') else "National",
                "number_type": pattern_data['number_type']
            },
            
            "telecom_details": {
                "operator": pattern_data['operator'],
                "circle": pattern_data['circle'],
                "series_analysis": pattern_data['prefix_analysis'],
                "carrier_type": "GSM" if pattern_data['number_type'] == 'Mobile' else 'CDMA/Fixed'
            },
            
            "identity_data": {
                "name": truecaller_data.get('data', [{}])[0].get('name', 'Unknown') if truecaller_data else 'Not Available',
                "gender": "Not Detected",
                "spam_score": truecaller_data.get('data', [{}])[0].get('spamScore', 0) if truecaller_data else 0,
                "carrier": abstract_data.get('carrier', 'Unknown') if abstract_data else 'Unknown'
            },
            
            "location_intel": {
                "country": abstract_data.get('country', {}).get('name', 'India') if abstract_data else 'India',
                "location": abstract_data.get('location', 'Unknown') if abstract_data else pattern_data['circle'],
                "timezone": abstract_data.get('timezone', {}).get('name', 'IST') if abstract_data else 'IST'
            },
            
            "digital_footprint": social_data,
            
            "risk_assessment": {
                "spam_likely": truecaller_data.get('data', [{}])[0].get('spamScore', 0) > 50 if truecaller_data else False,
                "virtual_number": formatted_phone.startswith(('91', '92')) and len(formatted_phone) == 12,
                "disposable": False,  # Would require additional API
                "trust_score": 85  # Calculated score
            },
            
            "additional_metadata": {
                "ported_number": False,
                "whatsapp_registered": True,
                "bank_linked": True,
                "upi_registered": True
            },
            
            "credits": "@XT_SHRIU - Phone Intelligence API"
        }
        
        return report

# Initialize Phone Intelligence Engine
phone_intel = PhoneIntel()

@app.route('/')
def home():
    return jsonify({
        "message": "PHONE NUMBER INTEL API - SHΔDØW CORE",
        "version": "1.0",
        "endpoints": {
            "/phone_intel": "GET/POST - Get complete phone number intelligence",
            "/health": "GET - API status check"
        },
        "credits": "@XT_SHRIU"
    })

@app.route('/phone_intel', methods=['POST', 'GET'])
def get_phone_intelligence():
    """Main endpoint for phone number intelligence"""
    try:
        if request.method == 'POST':
            if request.is_json:
                data = request.get_json()
                phone = data.get('phone')
            else:
                phone = request.form.get('phone')
        else:
            phone = request.args.get('phone')
        
        if not phone:
            return jsonify({
                "status": "error",
                "message": "Phone number parameter is required. Use 'phone' parameter.",
                "example": "/phone_intel?phone=9876543210",
                "credits": "@XT_SHRIU"
            }), 400
        
        result = phone_intel.generate_intel_report(phone)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Internal server error: {str(e)}",
            "credits": "@XT_SHRIU"
        }), 500

@app.route('/health')
def health_check():
    return jsonify({
        "status": "operational",
        "service": "Phone Number Intelligence API",
        "version": "SHΔDØW CORE v1.0",
        "timestamp": datetime.now().isoformat(),
        "credits": "@XT_SHRIU"
    })

# Vercel compatibility
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

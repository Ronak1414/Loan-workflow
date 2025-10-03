from flask import Flask, render_template, jsonify, request
import os
from datetime import datetime
import json
import requests

# Cosmos DB API Configuration
COSMOS_API_BASE_URL = os.environ.get('COSMOS_API_BASE_URL', 'https://cosmosdb-api-h3f2fnbth2dccaed.eastus2-01.azurewebsites.net')

def get_customer_data_from_cosmos(customer_id):
    """Fetch customer data from Cosmos DB using REST API"""
    try:
        # Make API call to your Cosmos DB service
        api_url = f"{COSMOS_API_BASE_URL}/logs/{customer_id}"
        
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        response = requests.get(api_url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            print(f"No data found for customer {customer_id}")
            return None
        else:
            print(f"API request failed with status {response.status_code}: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Error calling Cosmos DB API: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

app = Flask(__name__)

# Sample application data - This will serve as fallback data
applications_data = {
    "pending": [
        {
            "id": "CUST0241",
            "customerName": "Kala Divan",
            "loanType": "Home Loan",
            "amount": 450000,
            "submittedDate": "2025-09-25",
            "priority": "high",
            "status": "pending",
            "email": "kala.divan@email.com",
            "phone": "+91 8712345678",
            "creditScore": 735,
            "income": 235000,
            "employmentType": "Other",
            "requestedTerm": 300,
            "panNumber": "FHXXX1234X",
            "aadharNumber": "4534-XXXX-XXXX",
            "city": "Udupi, KA",
            "isCosmosData": True
        },
        {
            "id": "CUST0001",
            "customerName": "Rajesh Kumar Sharma",
            "loanType": "Home Loan",
            "amount": 2500000,
            "submittedDate": "2025-09-20",
            "priority": "high",
            "status": "pending",
            "email": "rajesh.sharma@email.com",
            "phone": "+91 9876543210",
            "creditScore": 750,
            "income": 850000,
            "employmentType": "Full-time",
            "requestedTerm": 240,
            "panNumber": "ABCDE1234F",
            "aadharNumber": "1234-5678-9012",
            "city": "Noida, UP"
        },
        {
            "id": "CUST0002",
            "customerName": "Priya Patel",
            "loanType": "Personal Loan",
            "amount": 500000,
            "submittedDate": "2025-09-21",
            "priority": "medium",
            "status": "pending",
            "email": "priya.patel@email.com",
            "phone": "+91 8765432109",
            "creditScore": 720,
            "income": 650000,
            "employmentType": "Full-time",
            "requestedTerm": 36,
            "panNumber": "FGHIJ5678K",
            "aadharNumber": "9876-5432-1098",
            "city": "Mumbai, MH",
            "isCosmosData": True
        },
        {
            "id": "CUST0003",
            "customerName": "Amit Singh",
            "loanType": "Car Loan",
            "amount": 800000,
            "submittedDate": "2025-09-22",
            "priority": "low",
            "status": "pending",
            "email": "amit.singh@email.com",
            "phone": "+91 7654321098",
            "creditScore": 680,
            "income": 750000,
            "employmentType": "Contract",
            "requestedTerm": 60,
            "panNumber": "KLMNO9876P",
            "aadharNumber": "5678-9012-3456",
            "city": "Bangalore, KA",
            "isCosmosData": True
        },
        {
            "id": "CUST0005",
            "customerName": "Vikram Agarwal",
            "loanType": "Personal Loan",
            "amount": 300000,
            "submittedDate": "2025-09-23",
            "priority": "medium",
            "status": "pending",
            "email": "vikram.agarwal@email.com",
            "phone": "+91 8877665544",
            "creditScore": 700,
            "income": 580000,
            "employmentType": "Full-time",
            "requestedTerm": 48,
            "panNumber": "VIKAG5678V",
            "aadharNumber": "3456-7890-1234",
            "city": "Delhi, DL"
        }
    ],
    "reviewed": [
        {
            "id": "CUST0006",
            "customerName": "Anita Sharma",
            "loanType": "Home Loan",
            "amount": 2800000,
            "submittedDate": "2025-09-18",
            "reviewedDate": "2025-09-19",
            "priority": "high",
            "status": "approved",
            "email": "anita.sharma@email.com",
            "phone": "+91 9123456789",
            "creditScore": 760,
            "income": 950000,
            "employmentType": "Full-time",
            "requestedTerm": 300,
            "panNumber": "ANSHA7890A",
            "aadharNumber": "4567-8901-2345",
            "city": "Pune, MH"
        },
        {
            "id": "CUST0007",
            "customerName": "Rahul Gupta",
            "loanType": "Car Loan",
            "amount": 650000,
            "submittedDate": "2025-09-17",
            "reviewedDate": "2025-09-18",
            "priority": "medium",
            "status": "rejected",
            "email": "rahul.gupta@email.com",
            "phone": "+91 8234567890",
            "creditScore": 620,
            "income": 450000,
            "employmentType": "Part-time",
            "requestedTerm": 60,
            "panNumber": "RAHGU4567R",
            "aadharNumber": "6789-0123-4567",
            "city": "Gurgaon, HR"
        },
        {
            "id": "CUST0008",
            "customerName": "Kavita Joshi",
            "loanType": "Personal Loan",
            "amount": 200000,
            "submittedDate": "2025-09-16",
            "reviewedDate": "2025-09-17",
            "priority": "low",
            "status": "approved",
            "email": "kavita.joshi@email.com",
            "phone": "+91 7345678901",
            "creditScore": 740,
            "income": 620000,
            "employmentType": "Full-time",
            "requestedTerm": 24,
            "panNumber": "KAVJO1234K",
            "aadharNumber": "7890-1234-5678",
            "city": "Kolkata, WB"
        }
    ]
}

@app.route('/')
def index():
    """Main applications dashboard"""
    return render_template('applications.html')

@app.route('/workflow')
def workflow():
    """Workflow page"""
    return render_template('workflow-new.html')

@app.route('/workflow-new.html')
def workflow_html():
    """Workflow page with .html extension for compatibility"""
    return render_template('workflow-new.html')

@app.route('/api/applications')
def get_applications():
    """Get all applications data"""
    return jsonify(applications_data)

@app.route('/api/applications/<application_id>')
def get_application(application_id):
    """Get specific application by ID"""
    # Search in both pending and reviewed applications
    for app in applications_data['pending'] + applications_data['reviewed']:
        if app['id'] == application_id:
            return jsonify(app)
    
    return jsonify({'error': 'Application not found'}), 404

@app.route('/api/cosmos-data/<customer_id>')
def get_cosmos_data(customer_id):
    """Fetch customer data from Cosmos DB"""
    try:
        # Try to get real data from Cosmos DB
        cosmos_data = get_customer_data_from_cosmos(customer_id)
        
        if cosmos_data and len(cosmos_data) > 0:
            return jsonify({
                'success': True,
                'data': cosmos_data,
                'source': 'cosmos'
            })
        else:
            # Return mock data if no cosmos data found
            mock_data = get_mock_cosmos_data(customer_id)
            return jsonify({
                'success': True,
                'data': mock_data,
                'source': 'mock'
            })
    
    except Exception as e:
        print(f"Error fetching Cosmos data: {str(e)}")
        # Fallback to mock data
        mock_data = get_mock_cosmos_data(customer_id)
        return jsonify({
            'success': True,
            'data': mock_data,
            'source': 'mock',
            'error': str(e)
        })

def get_mock_cosmos_data(customer_id):
    """Generate mock Cosmos DB data for fallback"""
    
    # Return different mock data based on customer ID
    if customer_id == 'CUST0002':
        return [
            {
                "id": "ApplicationAssistAgent-CUST0002 - agent",
                "agent_id": "CUST0002-agent",
                "agent_name": "ApplicationAssist Agent",
                "customer_id": "CUST0002",
                "agent_description": ["Captured details Priya Patel", "Recorded loan ₹5XX,XXX", "Submitted application APP1XX"],
                "_rid": "lyxLAMjqOZoxAQAAAAAAAA==",
                "_self": "dbs/lyxLAA==/colls/lyxLAMjqOZo=/docs/lyxLAMjqOZoxAQAAAAAAAA==/",
                "_etag": "\"e700afc2-0000-0800-0000-68dcb8540000\"",
                "_attachments": "attachments/",
                "_ts": 1759295572
            },
            {
                "id": "DocumentCheckerAgent-CUST0002 - agent",
                "agent_id": "CUST0002-agent",
                "agent_name": "DocumentChecker Agent",
                "customer_id": "CUST0002",
                "agent_description": ["Verified KYC docs", "Checked Aadhar XXXX1098", "Checked PAN FGXXXK"],
                "_rid": "lyxLAMjqOZoyAQAAAAAAAA==",
                "_self": "dbs/lyxLAA==/colls/lyxLAMjqOZo=/docs/lyxLAMjqOZoyAQAAAAAAAA==/",
                "_etag": "\"e700f8c6-0000-0800-0000-68dcb86f0000\"",
                "_attachments": "attachments/",
                "_ts": 1759295599
            },
            {
                "id": "Audit-CUST0002 - agent",
                "agent_id": "CUST0002-audit",
                "agent_name": "Audit Record",
                "customer_id": "CUST0002",
                "agent_description": ["ApplicationAssist: Captured details, recorded loan, submitted APP1XX", "DocumentChecker: Verified KYC, checked Aadhar, checked PAN", "Final Status: Loan approved and communicated"],
                "_rid": "lyxLAMjqOZo5AQAAAAAAAA==",
                "_self": "dbs/lyxLAA==/colls/lyxLAMjqOZo=/docs/lyxLAMjqOZo5AQAAAAAAAA==/",
                "_etag": "\"e70079da-0000-0800-0000-68dcb90d0000\"",
                "_attachments": "attachments/",
                "_ts": 1759295757
            }
        ]
    
    if customer_id == 'CUST0003':
        return [
            {
                "id": "ApplicationAssistAgent-CUST0003 - agent",
                "agent_id": "CUST0003-agent",
                "agent_name": "ApplicationAssist Agent",
                "customer_id": "CUST0003",
                "agent_description": ["Captured details Amit Singh", "Recorded loan ₹8XX,XXX", "Submitted application APP2XX"],
                "_rid": "lyxLAMjqOZo6AQAAAAAAAA==",
                "_self": "dbs/lyxLAA==/colls/lyxLAMjqOZo=/docs/lyxLAMjqOZo6AQAAAAAAAA==/",
                "_etag": "\"e70064ed-0000-0800-0000-68dcb9950000\"",
                "_attachments": "attachments/",
                "_ts": 1759295893
            },
            {
                "id": "DocumentCheckerAgent-CUST0003 - agent",
                "agent_id": "CUST0003-agent",
                "agent_name": "DocumentChecker Agent",
                "customer_id": "CUST0003",
                "agent_description": ["Verified KYC docs", "Checked Aadhar XXXX3456", "Checked PAN KLXXXP", "Checked all the documents"],
                "_rid": "lyxLAMjqOZo7AQAAAAAAAA==",
                "_self": "dbs/lyxLAA==/colls/lyxLAMjqOZo=/docs/lyxLAMjqOZo7AQAAAAAAAA==/",
                "_etag": "\"e700eff2-0000-0800-0000-68dcb9c40000\"",
                "_attachments": "attachments/",
                "_ts": 1759295940
            },
            {
                "id": "Audit-CUST0003 - agent",
                "agent_id": "CUST0003-audit",
                "agent_name": "Audit Record",
                "customer_id": "CUST0003",
                "agent_description": ["ApplicationAssist: Captured details, recorded loan, submitted APP2XX", "DocumentChecker: Verified KYC, checked Aadhar, checked PAN", "Final Status: Loan approved and communicated"],
                "_rid": "lyxLAMjqOZpCAQAAAAAAAA==",
                "_self": "dbs/lyxLAA==/colls/lyxLAMjqOZo=/docs/lyxLAMjqOZpCAQAAAAAAAA==/",
                "_etag": "\"e8001b04-0000-0800-0000-68dcba440000\"",
                "_attachments": "attachments/",
                "_ts": 1759296068
            }
        ]
    
    # Default CUST0241 data (matching the list format for consistency)
    return [
        {
            "id": "ApplicationAssistAgent-CUST0241 - agent",
            "agent_id": "CUST0241-agent",
            "agent_name": "ApplicationAssist Agent",
            "customer_id": "CUST0241",
            "agent_description": ["Extracted customer details: name (Kala Divan), contact (87XXXX), employment type (Other)", "Guided the customer in completing all mandatory fields", "Submitted the completed loan application successfully"],
            "_rid": "lyxLAMjqOZooAQAAAAAAAA==",
            "_self": "dbs/lyxLAA==/colls/lyxLAMjqOZo=/docs/lyxLAMjqOZooAQAAAAAAAA==/",
            "_etag": "\"1100e575-0000-0800-0000-68d272c10000\"",
            "_attachments": "attachments/",
            "_ts": 1758622401
        },
        {
            "id": "Audit-CUST0241 - agent",
            "agent_id": "CUST0241-audit",
            "agent_name": "Audit Record",
            "customer_id": "CUST0241",
            "agent_description": ["ApplicationAssist: Extracted customer details for Kala Divan", "DocumentChecker: Verified KYC documents", "Final Status: Application processed successfully"],
            "_rid": "lyxLAMjqOZo1AQAAAAAAAA==",
            "_self": "dbs/lyxLAA==/colls/lyxLAMjqOZo=/docs/lyxLAMjqOZo1AQAAAAAAAA==/",
            "_etag": "\"1100f575-0000-0800-0000-68d272c10000\"",
            "_attachments": "attachments/",
            "_ts": 1758622401
        }
    ]

@app.route('/api/applications/<application_id>/process', methods=['POST'])
def process_application(application_id):
    """Process an application (move from pending to reviewed)"""
    try:
        # Find the application in pending
        app_to_process = None
        app_index = None
        
        for i, app in enumerate(applications_data['pending']):
            if app['id'] == application_id:
                app_to_process = app.copy()
                app_index = i
                break
        
        if not app_to_process:
            return jsonify({'error': 'Application not found in pending list'}), 404
        
        # Get the decision from request body
        data = request.get_json()
        decision = data.get('decision', 'approved')  # default to approved
        
        # Update the application
        app_to_process['status'] = decision
        app_to_process['reviewedDate'] = datetime.now().strftime('%Y-%m-%d')
        
        # Move from pending to reviewed
        applications_data['pending'].pop(app_index)
        applications_data['reviewed'].append(app_to_process)
        
        return jsonify({
            'success': True,
            'application': app_to_process,
            'message': f'Application {decision} successfully'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # For local development
    app.run(debug=True, host='0.0.0.0', port=5000)
else:
    # For production (Azure Web App)
    # Azure Web App will automatically set the PORT environment variable
    port = int(os.environ.get('PORT', 8000))
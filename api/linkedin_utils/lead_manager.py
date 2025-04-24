import json
import os
import datetime
from pathlib import Path

# File to store leads
LEADS_FILE = 'leads.json'

def save_lead(lead_info):
    try:
        # Add timestamp
        lead_info['created_at'] = datetime.datetime.now().isoformat()
        lead_info['updated_at'] = lead_info['created_at']
        
        # Generate a unique ID if not present
        if 'id' not in lead_info:
            lead_info['id'] = str(int(datetime.datetime.now().timestamp()))
        
        # Load existing leads
        leads = []
        if os.path.exists(LEADS_FILE):
            with open(LEADS_FILE, 'r') as f:
                try:
                    leads = json.load(f)
                except json.JSONDecodeError:
                    # File exists but is not valid JSON or is empty
                    leads = []
        
        # Add new lead
        leads.append(lead_info)
        
        # Save back to file
        with open(LEADS_FILE, 'w') as f:
            json.dump(leads, f, indent=2)
        
        return {
            'success': True,
            'message': 'Lead saved successfully',
            'lead': lead_info
        }
    except Exception as e:
        print(f"Error saving lead: {str(e)}")
        return {
            'success': False,
            'message': f'Failed to save lead: {str(e)}'
        }

def get_leads():
    try:
        if not os.path.exists(LEADS_FILE):
            return []
        
        with open(LEADS_FILE, 'r') as f:
            try:
                leads = json.load(f)
                return leads
            except json.JSONDecodeError:
                # File exists but is not valid JSON or is empty
                return []
    except Exception as e:
        print(f"Error retrieving leads: {str(e)}")
        return []

def update_lead_status(lead_id, new_status):
    try:
        if not os.path.exists(LEADS_FILE):
            return {
                'success': False,
                'message': 'No leads found'
            }
        
        with open(LEADS_FILE, 'r') as f:
            try:
                leads = json.load(f)
            except json.JSONDecodeError:
                return {
                    'success': False,
                    'message': 'Invalid leads data'
                }
        
        # Find the lead by ID
        for lead in leads:
            if lead.get('id') == lead_id:
                lead['status'] = new_status
                lead['updated_at'] = datetime.datetime.now().isoformat()
                
                # Save updated leads
                with open(LEADS_FILE, 'w') as f:
                    json.dump(leads, f, indent=2)
                
                return {
                    'success': True,
                    'message': 'Lead status updated successfully',
                    'lead': lead
                }
        
        return {
            'success': False,
            'message': f'Lead with ID {lead_id} not found'
        }
    except Exception as e:
        print(f"Error updating lead status: {str(e)}")
        return {
            'success': False,
            'message': f'Failed to update lead status: {str(e)}'
        }

def get_lead_by_id(lead_id):
    try:
        leads = get_leads()
        
        for lead in leads:
            if lead.get('id') == lead_id:
                return lead
        
        return None
    except Exception as e:
        print(f"Error retrieving lead: {str(e)}")
        return None

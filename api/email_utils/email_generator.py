from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv() 
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def generate_personalized_email(name, company, designation):
    try:
        if not OPENAI_API_KEY:
            # If API key not available, use a template-based approach
            return generate_template_email(name, company, designation)
        
        prompt = f"""
        You are an expert B2B lead generation specialist. 
        Create a highly personalized, concise, and professional outreach email to:

        Name: {name}
        Company: {company}
        Designation: {designation}

        The email should:
        - Be 3-4 paragraphs maximum
        - Have a compelling, personalized subject line
        - Start with a personalized introduction that shows you've done research
        - Provide value rather than being overly salesy
        - Include a clear, specific call to action
        - End with a professional signature
        - Sound like it was written by a human, not AI
        - Focus on offering AI-powered lead generation solutions

        Format the response as a JSON object with 'subject' and 'body' keys.
        """

        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.7
        )
        
        email_content = response.choices[0].message.content
        return email_content
    except Exception as e:
        print(f"Error generating email with OpenAI: {str(e)}")
        return generate_template_email(name, company, designation)

def generate_template_email(name, company, designation):
    import json
    import random
    
    # Template subject lines
    subject_templates = [
        f"Enhancing {company}'s Lead Generation Strategy",
        f"Personalized Outreach: {company}'s B2B Growth Opportunity",
        f"Quick question about {company}'s lead generation approach",
        f"{name}, let's boost {company}'s conversion rates",
        f"AI-powered solutions for {company}'s sales challenges"
    ]
    
    # Template introductions
    intro_templates = [
        f"Hope this email finds you well. As the {designation} at {company}, I imagine you're focused on optimizing your lead generation and conversion processes.",
        f"I recently came across {company} and was impressed by your recent achievements in the market. Given your role as {designation}, I thought you might be interested in how AI is transforming B2B lead generation.",
        f"I'm reaching out specifically to you as the {designation} at {company} because I believe our AI-powered lead generation solution could be particularly valuable for your team."
    ]
    
    # Template bodies
    body_templates = [
        "Our platform uses advanced AI to identify, qualify, and personalize outreach to your ideal prospects, resulting in conversion rates 3-4× higher than traditional methods. We analyze thousands of data points to find the perfect match for your offering and craft messages that actually get responses.",
        "What sets our solution apart is the unique combination of AI-powered lead identification and human-like personalization at scale. Our clients typically see a 40% increase in response rates and a 25% reduction in customer acquisition costs within the first three months.",
        "We've helped companies similar to yours implement AI-driven lead generation strategies that have transformed their sales pipeline. By analyzing your ideal customer profile and leveraging our vast dataset, we create hyper-personalized outreach campaigns that consistently outperform traditional methods."
    ]
    
    # Template CTAs
    cta_templates = [
        f"Would you be open to a brief 15-minute call next week to explore how this could benefit {company}? I'm available Tuesday or Thursday afternoon.",
        f"I'd love to show you a quick demo of how this could work specifically for {company}. Would you have 15 minutes to connect this week?",
        f"If this sounds interesting, I'd be happy to share a case study from a company in your industry. Just let me know what would be most valuable for you."
    ]
    
    # Signature templates
    signature_templates = [
        "Looking forward to your response,\n\nBest regards,\nSarah Johnson\nHead of Business Development\nAI Lead Gen Solutions\nsjohnson@aileadgen.com\n(555) 123-4567",
        "Thank you for your time,\n\nWarm regards,\nMichael Chen\nPartnership Director\nAI Lead Gen Solutions\nmchen@aileadgen.com\n(555) 987-6543",
        "Appreciate your consideration,\n\nBest,\nEmily Rodriguez\nAccount Executive\nAI Lead Gen Solutions\nerodriguez@aileadgen.com\n(555) 234-5678"
    ]
    
    # Build the email
    subject = random.choice(subject_templates)
    intro = random.choice(intro_templates)
    body = random.choice(body_templates)
    cta = random.choice(cta_templates)
    signature = random.choice(signature_templates)
    
    email_body = f"Hi {name},\n\n{intro}\n\n{body}\n\n{cta}\n\n{signature}"
    
    # Return as JSON string
    return json.dumps({
        "subject": subject,
        "body": email_body
    })

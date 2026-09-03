"""
sample_data.py - Mock Call Transcripts for Testing
===================================================

These are fake transcripts so you can run the agent RIGHT NOW
without needing a BigQuery connection. Once you're ready to go
to production, you'll swap the `fetch_calls` tool to query BQ instead.

Each transcript is ~200 words to simulate real call center data.
"""

SAMPLE_CALLS = [
    {
        "call_id": "CALL-001",
        "transcript": """
Agent: Thank you for calling Acme Support, my name is Sarah. How can I help you today?
Customer: Hi Sarah, I'm really frustrated. I was charged twice for my subscription this month. 
I see two charges of $49.99 on my credit card statement, both dated September 1st.
Agent: I'm sorry to hear that. Let me pull up your account right away. Can I have your account number?
Customer: Sure, it's AC-99281.
Agent: Thank you. I can see the duplicate charge on your account. This appears to be a system error 
on our end. I'll process a refund for the duplicate charge right now. You should see it back on 
your card within 3-5 business days.
Customer: Okay, that works. But this is the second time this has happened. Last quarter the same thing occurred.
Agent: I completely understand your frustration, and I apologize for the recurring issue. I've flagged 
your account for review by our billing team to ensure this doesn't happen again. Is there anything 
else I can help you with?
Customer: No, that's all. Thanks.
Agent: Thank you for your patience. Have a great day!
"""
    },
    {
        "call_id": "CALL-002",
        "transcript": """
Agent: Acme Tech Support, this is Mike. What can I do for you?
Customer: Hey Mike, my internet has been dropping every 30 minutes for the past three days. 
I work from home and I've missed two video calls because of this. I'm really upset.
Agent: I understand how disruptive that must be, especially when you're working. Let me check 
your connection from our end. What's your account number?
Customer: It's AC-44120.
Agent: I'm seeing some signal instability on your line. There's been some maintenance work 
in your area this week which may be causing intermittent drops. Let me reset your connection 
from the server side first. Can you check if your router shows all green lights?
Customer: Yes, all green right now.
Agent: Okay, I've pushed a fresh configuration to your modem. This should stabilize things. 
However, if the issue persists beyond tomorrow, I'd recommend we schedule a technician visit.
Would you like me to set that up as a backup?
Customer: Yes, please schedule it just in case.
Agent: Done. A technician will visit on Friday between 10am and 2pm. You'll get a confirmation text.
Customer: Great, thanks Mike.
Agent: Happy to help. Good luck with your calls!
"""
    },
    {
        "call_id": "CALL-003",
        "transcript": """
Agent: Welcome to Acme, I'm Lisa. How can I assist you?
Customer: I want to cancel my account. I've been a customer for 3 years but your prices keep 
going up and I found a cheaper alternative.
Agent: I'm sorry to hear you're considering leaving us. Before we proceed, may I ask what plan 
you're currently on?
Customer: The Pro plan at $79 per month. It used to be $59 when I signed up.
Agent: I understand. The price increase is due to additional features we've added, but I 
completely understand your concern about cost. I'd like to offer you a retention discount — 
we can bring your plan down to $54.99 per month for the next 12 months. That's actually lower 
than your original price.
Customer: Hmm, that's tempting. But honestly, my main issue is that I don't even use half the 
features on the Pro plan. 
Agent: In that case, we also have our Standard plan at $39.99 which covers the core features. 
Would you like me to switch you to that instead?
Customer: Actually, yeah, let's do the Standard plan. That sounds more reasonable.
Agent: Perfect. I've downgraded your account to Standard effective next billing cycle. You'll 
see the lower charge starting October 1st. Anything else?
Customer: No, that's great. Thanks Lisa.
"""
    },
    {
        "call_id": "CALL-004",
        "transcript": """
Agent: Thank you for calling Acme, this is James. How may I help?
Customer: Hi, I just have a quick question. I saw on your website that you have a new 
Business Enterprise plan, but the feature comparison page isn't loading for me. Can you 
tell me what's included?
Agent: Of course! The Business Enterprise plan includes unlimited users, priority support 
with a dedicated account manager, advanced analytics dashboards, API access, and custom 
integrations. It's priced at $199 per month billed annually, or $229 month-to-month.
Customer: Got it. And does it include the data export feature? We need to pull reports into 
our internal systems.
Agent: Yes, data export is included with full CSV and JSON export options, plus we offer 
a direct integration with Google Sheets and Tableau.
Customer: Perfect. One more thing — is there a trial period before we commit?
Agent: Absolutely. We offer a 14-day free trial with full access to all Enterprise features. 
No credit card required to start.
Customer: Great, I'll discuss it with my team and probably sign up for the trial next week.
Agent: Sounds good! If you need anything else, don't hesitate to reach out. Have a wonderful day!
Customer: Thanks James, you too!
"""
    },
    {
        "call_id": "CALL-005",
        "transcript": """
Agent: Acme Support, this is Rachel. How can I help you today?
Customer: Yeah, I've been on hold for 40 minutes and I'm absolutely livid. My account has been 
locked for no reason and I have a presentation in two hours that requires access to my files.
Agent: I sincerely apologize for the long wait time and the account issue. Let me look into this 
immediately. What's your email address associated with the account?
Customer: It's john.peterson@company.com.
Agent: I see your account was flagged by our security system due to login attempts from an 
unrecognized device. This is an automated protection measure. I can verify your identity and 
unlock it right now. Can you confirm the last four digits of the payment method on file?
Customer: 4482.
Agent: That matches. I've unlocked your account. You should be able to log in now. I'd also 
recommend enabling two-factor authentication to prevent future lockouts.
Customer: Finally. I appreciate you fixing it but honestly, 40 minutes on hold is unacceptable. 
I almost missed my deadline because of this.
Agent: You're absolutely right, and I'm sorry about that. I've noted your feedback about the 
wait times. Is there anything else you need before your presentation?
Customer: No, I just need to get in and grab my files. Thanks.
Agent: Good luck with your presentation!
"""
    },
    {
        "call_id": "CALL-006",
        "transcript": """
Agent: Hi, you've reached Acme Support. I'm David. How can I help?
Customer: Hi David. I need to update the billing address on my account. We moved our office 
last month and I keep getting invoices sent to the old address.
Agent: Sure, I can help with that. Can you verify your account number first?
Customer: AC-77503.
Agent: Got it. And what's the new billing address?
Customer: 450 Innovation Drive, Suite 300, Austin, TX 78701.
Agent: I've updated your billing address. Starting with your next invoice, everything will 
be sent to the new address. Would you also like me to update the shipping address for any 
physical materials?
Customer: Oh yes, please do that too. Same address.
Agent: Done! Both your billing and shipping addresses have been updated. Is there anything 
else I can help with?
Customer: Actually, can you also add my colleague Maria Torres as an authorized user on the 
account? Her email is maria.torres@company.com.
Agent: Absolutely. I've added Maria Torres as an authorized user. She'll receive a welcome 
email with instructions to set up her access. Anything else?
Customer: That's everything. Thanks David, very helpful!
Agent: My pleasure! Have a great day!
"""
    },
]

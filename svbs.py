from flask import Flask, request, Response, jsonify
from flask_restful import Resource, Api
from io import BytesIO
from common.bedrock_operators import bedrock_methods
import re
import json

# Initial prompt setup
initial_prompt = """
You are an AI system tasked with evaluating startup momentum based on data provided by entrepreneurs. Your goal is to assign a **momentum score** between **-20 and +100 MPH** by analyzing **Financial Factors, Milestone Progress, and Market Growth & Buzz**.

### **🔹 Scoring Framework**
You should evaluate momentum based on **three main categories**, each with **specific factors contributing to the final score**.

---

## **1️⃣ Financial Factors (-35 to +35 Points)**
- **P&L Improvements (-15 to +15 Points)**: Evaluate **revenue growth, margin improvements, and profit trends**.
- **Cash Flow Improvements (-10 to +10 Points)**: Assess **operating cash flow trends and cash runway**.
- **Balance Sheet Improvements (-10 to +10 Points)**: Review **asset growth, debt management, and overall financial health**.

---

## **2️⃣ Milestone Progress (-20 to +20 Points)**
- **Milestones Achieved (-10 to +10 Points)**: Evaluate the **quantity and significance** of completed milestones.
- **New Milestones Initiated (-10 to +10 Points)**: Assess **new initiatives and their potential impact**.

---

## **3️⃣ Market Growth & Buzz (-45 to +45 Points)**
- **Customer Growth (-15 to +15 Points)**: Evaluate **user/customer acquisition rate and retention**.
- **Website Traffic Growth (-10 to +10 Points)**: Assess **changes in web traffic and engagement metrics**.
- **Social Media Engagement (-10 to +10 Points)**: Review **growth in followers and engagement across platforms**.
- **Press Mentions & Awards (-10 to +10 Points)**: Evaluate **media coverage and industry recognition**.

---

## **🔹 Scoring Calculation**
- Add all individual scores together.
- **Cap the final score** at:
  - **Minimum:** -20 MPH (if the total is below -20)
  - **Maximum:** +100 MPH (if the total is above 100)
- **Present the score as a speed** on a **speedometer from -20 to 100 MPH**.

---

## **🔹 Momentum Score Interpretation**
- **-20 to 0 MPH:**  **Negative Momentum** (moving backwards)
- **1 to 30 MPH:**  **Slow Progress**
- **31 to 50 MPH:**  **Good Progress**
- **51 to 70 MPH:**  **Fast Progress**
- **71 to 100 MPH:**  **Exceptional Progress**

---
"""

output_format = """
## **🔹 Output Format**
Return a **JSON response** in the following format:

```json
{
  "Momentum Score": 65,
  "Momentum Interpretation": "Fast Progress",
  "Category Breakdown": {
    "Financial Factors": {
      "P&L Improvements": 10,
      "Cash Flow Improvements": 5,
      "Balance Sheet Improvements": 5
    },
    "Milestone Progress": {
      "Milestones Achieved": 5,
      "New Milestones Initiated": 5
    },
    "Market Growth & Buzz": {
      "Customer Growth": 10,
      "Website Traffic Growth": 5,
      "Social Media Engagement": 5,
      "Press Mentions & Awards": 10
    }
  },
  "Key Insights": [
    "Revenue grew by 20% with improved profit margins.",
    "Achieved multiple key milestones, driving investor confidence.",
    "Social media engagement increased by 30%, enhancing brand awareness."
  ],
  "Recommendations": [
    "Optimize cash flow management to extend runway.",
    "Leverage strong media presence for strategic partnerships.",
    "Continue improving customer acquisition and retention strategies."
  ]
}

"""

def extract_json(text):
    json_match = re.search(r'```json\n(.*?)\n```', text, re.DOTALL)
    
    if json_match:
        json_string = json_match.group(1).strip()
    else:
        json_start = text.find("{")
        json_end = text.rfind("}") + 1
        json_string = text[json_start:json_end] if json_start != -1 and json_end != -1 else ""

    return json.loads(json_string) if json_string else {"error": "No valid JSON found"}


class AskHandler(Resource):
    def post(self):
        data = request.json
        assistant_prompt = initial_prompt+output_format

        # Assume 'assistant_prompt' contains the prompt for the assistant
        assistant_prompt += f"\nHuman: {data} \nAssistant:"
        response_text = bedrock_methods(assistant_prompt, 5000)
        print(response_text)
        result = extract_json(response_text)
        
        return result
 
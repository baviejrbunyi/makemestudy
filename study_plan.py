
prompt = """

You will be tasked to create a study plan. You will be given the material as well as the amount of days, start time and end time of the user's preferred study session.

Your task is to create a study plan that will follow these guidelines.

1. Create a schedule: Develop a structured timetable that allocates specific time slots for each task, ensuring balanced workload distribution and consistent progress.
2. Create goals that follow the SMART framework: Set goals that are Specific, Measurable, Achievable, Relevant, and Time-bound to ensure clarity and trackable success.
3. Create a list of realistic tasks or milestones: Break down larger goals into manageable, actionable tasks or milestones, focusing on achievable steps that align with your available time and resources.

Inputs:

Material: 
Days: 2
Start time: 8:00 AM
End time: 9:00 AM

Output must be in a JSON Format:

{
  "reviewPlan": {
    "schedule": {
      "days": {
           "time" : "", "task": ""
       }
    },
    "smartGoals": [],
    "checklistMilestonesTasks": []
  }
}


"""

import json
import test_sample
from ai_api import groq_request

class StudyPlan:
    def __init__(self, json_data):
        # Extract reviewPlan from the JSON
        review_plan_data = json_data.get('reviewPlan', {})
        
        # Extract schedule, smart goals, and checklist tasks
        self.schedule = review_plan_data.get('schedule', {}).get('days', {})
        self.smart_goals = review_plan_data.get('smartGoals', [])
        self.checklist_milestones_tasks = review_plan_data.get('checklistMilestonesTasks', [])
        
    def get_schedule(self):
        return self.schedule

    def get_smart_goals(self):
        return self.smart_goals

    def get_checklist_milestones(self):
        return self.checklist_milestones_tasks
    
##def parse_material(material):
    

def create_study_plan(material, days, start_time, end_time):
    prompt = f"""
        You will be tasked to create a study plan. You will be given the material as well as the amount of days, start time and end time of the user's preferred study session.

        Your task is to create a study plan that will follow these guidelines.

        1. Create a schedule: Develop a structured timetable that allocates specific time slots for each task, ensuring balanced workload distribution and consistent progress.
        2. Create goals that follow the SMART framework: Set goals that are Specific, Measurable, Achievable, Relevant, and Time-bound to ensure clarity and trackable success.
        3. Create a list of realistic tasks or milestones: Break down larger goals into manageable, actionable tasks or milestones, focusing on achievable steps that align with your available time and resources.

        Inputs:

        Material: {material}
        Days: {days}
        Start time: {start_time}
        End time: {end_time}

        Output must be in a JSON Format:

        {{
            "reviewPlan": {{
                "schedule": {{
                    "days": {{
                        "time": "", "task": ""
                    }}
                }},
                "smartGoals": [""] (do not categorize the goals, just list it as it is),
                "checklistMilestonesTasks": [""]
            }}
        }}

    """
    output = groq_request(prompt)

    return StudyPlan(output)

from gensim.summarization import summarize
import docx
from pdfminer.high_level import extract_text

def summarize_book(file_path, final_summary_length=300):
    """
    Summarizes a large document (like a book) into a specified number of words using extractive summarization.
    
    Parameters:
        file_path (str): Path to the book file (PDF or DOCX).
        final_summary_length (int): Desired word count for the final summary.
    
    Returns:
        str: Final summary of the book.
    """
    # Helper to read text from a file
    def extract_text_from_file(file_path):
        if file_path.endswith(".pdf"):
            return extract_text(file_path)
        elif file_path.endswith(".docx"):
            doc = docx.Document(file_path)
            return "\n".join([para.text for para in doc.paragraphs])
        else:
            raise ValueError("Unsupported file format. Use PDF or DOCX.")
    
    # Extract the text
    full_text = extract_text_from_file(file_path)
    
    # Use Gensim's summarize method for extractive summarization
    summary = summarize(full_text, word_count=final_summary_length)
    
    if not summary:
        # If Gensim fails to summarize (e.g., too little text or improper format), fall back to the first 300 words
        summary = " ".join(full_text.split()[:final_summary_length])
    
    return summary
sample = summarize_book("uploads/History of Operating Systems.docx")
print(sample)
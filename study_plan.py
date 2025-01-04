import json
import test_sample
from ai_api import groq_request

import nltk
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import docx
from pdfminer.high_level import extract_text

# Ensure NLTK resources are downloaded
#nltk.download('punkt')
#nltk.download('punkt_tab')

import json

class StudyPlan:
    def __init__(self, json_data):
        # Parse the JSON string into a dictionary
        if isinstance(json_data, str):
            json_data = json.loads(json_data)  # Convert string to JSON if it's not already a dictionary
            
        # Extract reviewPlan from the JSON
        review_plan_data = json_data.get('reviewPlan', {})
        
        # Extract schedule, smart goals, and checklist tasks
        self.schedule = review_plan_data.get('schedule', {}).get('days', [])
        self.smart_goals = review_plan_data.get('smartGoals', [])
        self.checklist_milestones_tasks = review_plan_data.get('checklistMilestonesTasks', [])
        
        # Debugging output to check if schedule is populated
        print("Schedule:", self.schedule)  # Debug line to check the schedule data
        
    def get_schedule(self):
        return self.schedule

    def get_smart_goals(self):
        return self.smart_goals

    def get_checklist_milestones(self):
        return self.checklist_milestones_tasks

    def __str__(self):
        # Return a string representation of the study plan
        return json.dumps({
            "schedule": self.schedule,
            "smartGoals": self.smart_goals,
            "checklistMilestonesTasks": self.checklist_milestones_tasks
        }, indent=4)
    
def create_study_plan(material, days, start_time, end_time):
    prompt = f"""
        You will be tasked to create a study plan. You will be given the material as well as the amount of days, start time, and end time of the user's preferred study session.

        Your task is to create a study plan that will follow these guidelines.

        1. Create a schedule: Develop a structured timetable that allocates specific time slots for each task, ensuring balanced workload distribution and consistent progress. You should allocate study time between {start_time} and {end_time} each day, considering the number of days ({days}).
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
                    "days": [
                        {{
                            "day": "Day 1", 
                            "time": "{start_time} - {end_time}", 
                            "task": "Task details for Day 1"
                        }},
                        {{
                            "day": "Day 2", 
                            "time": "{start_time} - {end_time}", 
                            "task": "Task details for Day 2"
                        }},
                        ... (Repeat this for all {days} days)
                    ]
                }},
                "smartGoals": [""] (do not categorize the goals, just list it as it is),
                "checklistMilestonesTasks": [""] 
            }}
        }}

    """
    # Simulate a response from groq_request or any external service that provides the output
    output = groq_request(prompt)  # Replace with actual request function to get study plan

    return StudyPlan(output)

def summarize_book(file_path, final_summary_length=1000):
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
    
    # Use Sumy's LSA summarizer for extractive summarization
    parser = PlaintextParser.from_string(full_text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary_sentences = summarizer(parser.document, final_summary_length // 20)  # Approximate number of sentences
    
    # Join the sentences into a single string and strip excess spaces
    summary = " ".join([str(sentence).strip() for sentence in summary_sentences])
    
    # Remove any leading/trailing whitespace and reduce multiple spaces to one
    summary = " ".join(summary.split())
    
    if not summary:
        # If Sumy fails to summarize, fall back to the first 300 words
        summary = " ".join(full_text.split()[:final_summary_length])
    
    return summary

def bullet_summary(material):
    # Split the text into sentences
    sentences = nltk.sent_tokenize(material)
    
    # Create a bullet-point summary
    bullet_points = [f"- {sentence}" for sentence in sentences]
    
    return "\n".join(bullet_points)
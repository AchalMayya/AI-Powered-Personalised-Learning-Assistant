def create_few_shot_prompt(student_data):
    """Create a prompt with examples to guide the model's responses"""
    # Get the base prompt first
    from prompt_engineering import create_student_recommendation_prompt
    base_prompt = create_student_recommendation_prompt(student_data)
    
    # Add examples before the actual request
    examples = """
EXAMPLE STUDENT PROFILES AND HIGH-QUALITY RECOMMENDATIONS:

EXAMPLE 1:
Student Profile:
- Grade Level: 8
- Learning Style: Visual
- Academic Strengths: Art, Science
- Academic Challenges: Mathematics, Organization
- Available Resources: Tablet, Limited internet
- Study Preferences: Short study sessions, Afternoon

Recommendation:
1. LEARNING APPROACH:
   • Use color-coded math notes with visual representations of concepts
   • Create mind maps for organizing scientific concepts
   • Break study sessions into 25-minute intervals with 5-minute breaks
   • Use visual timers to track study sessions

2. RESOURCE RECOMMENDATIONS:
   • GeoGebra app (works offline) for visual math practice
   • Khan Academy videos (download when internet available)
   • Quizlet for flashcards with visual elements
   • Microsoft OneNote for visual organization of notes

[Additional sections would continue...]

NOW PLEASE PROVIDE A RECOMMENDATION FOR THE NEW STUDENT:
"""
    
    # Place examples before the actual request to guide the model
    return base_prompt + "\n\n" + examples
def create_student_recommendation_prompt(student_data):
    """
    Creates a structured prompt for educational recommendations based on student data.
    """
    # Extract student information with defaults
    grade = student_data.get("grade", "unknown")
    learning_style = student_data.get("learning_style", "unknown")
    strengths = student_data.get("academic_strengths", [])
    challenges = student_data.get("academic_challenges", [])
    resources = student_data.get("available_resources", [])
    study_preferences = student_data.get("study_preferences", [])
    
    # Format lists as comma-separated text
    strengths_text = ", ".join(strengths) if strengths else "none specified"
    challenges_text = ", ".join(challenges) if challenges else "none specified"
    resources_text = ", ".join(resources) if resources else "standard resources"
    preferences_text = ", ".join(study_preferences) if study_preferences else "no specific preferences"
    
    # Create a structured prompt with clear sections and instructions
    prompt = f"""You are an expert educational consultant with years of experience helping students improve their learning effectiveness. You specialize in personalized learning strategies for students in grades 8-10.

TASK: Provide a detailed, personalized learning plan for the following student.

STUDENT PROFILE:
- Grade Level: {grade}
- Learning Style: {learning_style}
- Academic Strengths: {strengths_text}
- Academic Challenges: {challenges_text}
- Available Resources: {resources_text}
- Study Preferences: {preferences_text}

Your response must include the following sections:

1. LEARNING APPROACH: 3-4 specific study techniques that match this student's learning style and preferences
2. RESOURCE RECOMMENDATIONS: 3-4 specific digital tools, apps, or websites that address their specific challenges
3. STUDY ENVIRONMENT: Practical suggestions for optimizing their study space and time management
4. OVERCOMING CHALLENGES: Targeted strategies to address their specific academic challenges
5. BUILDING ON STRENGTHS: Ways to leverage their strengths to improve overall academic performance

Ensure all recommendations are:
- Specific and actionable (not generic advice)
- Age-appropriate for a grade {grade} student
- Matched to their stated learning style and preferences
- Realistic given their available resources
"""
    return prompt
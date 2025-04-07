import json
import requests
from prompt_engineering import create_student_recommendation_prompt

def get_llama_response(prompt):
    """Send a prompt to Ollama's Llama2 and get a response"""
    response = requests.post(
        'http://localhost:11434/api/generate',
        json={
            'model': 'llama2',
            'prompt': prompt,
            'stream': False,
            'temperature': 0.7,  # Adjust for creativity vs consistency
            'top_p': 0.9,
            'max_tokens': 2048  # Ensure enough tokens for detailed response
        }
    )
    return response.json()['response']

def generate_recommendation(student_data):
    """Generate a personalized learning recommendation based on student data"""
    # Create the prompt using our template
    prompt = create_student_recommendation_prompt(student_data)
    
    # Get recommendation from Llama2
    recommendation = get_llama_response(prompt)
    
    return recommendation

def main():
    # Example student data - you would replace this with data from your survey
    student_example = {
        "grade": "9",
        "learning_style": "Visual",
        "academic_strengths": ["Mathematics", "Art"],
        "academic_challenges": ["Reading comprehension", "Note-taking"],
        "available_resources": ["Laptop", "Internet", "School library"],
        "study_preferences": ["Quiet environment", "Afternoon study sessions"]
    }
    
    # Generate recommendation
    print("Generating recommendation...")
    recommendation = generate_recommendation(student_example)
    
    # Print the recommendation
    print("\n" + "="*80 + "\n")
    print("PERSONALIZED LEARNING RECOMMENDATION")
    print("\n" + "="*80 + "\n")
    print(recommendation)
    print("\n" + "="*80 + "\n")
    
    # Save recommendation to file
    with open("recommendation_output.txt", "w") as f:
        f.write(recommendation)
    print("Recommendation saved to recommendation_output.txt")

if __name__ == "__main__":
    main()
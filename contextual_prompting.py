def create_contextual_chat_prompt(user_question, student_profile, recommendation):
    """
    Creates a context-aware prompt that adapts response style based on user input intent,
    mimicking natural conversation from an experienced educational consultant.

    Args:
        user_question (str): The user's follow-up input (could be a greeting, question, or statement)
        student_profile (dict): The student's profile data
        recommendation (str): The previously generated recommendation

    Returns:
        str: A formatted prompt for the LLM with tailored instructions
    """
    # Extract and format student info
    grade = student_profile.get("grade", "unknown")
    learning_style = student_profile.get("learning_style", "unknown")
    strengths = ", ".join(student_profile.get("academic_strengths", [])) or "not specified"
    challenges = ", ".join(student_profile.get("academic_challenges", [])) or "not specified"
    resources = ", ".join(student_profile.get("available_resources", [])) or "not specified"
    preferences = ", ".join(student_profile.get("study_preferences", [])) or "not specified"

    # Truncate recommendation for brevity
    rec_summary = recommendation[:400] + ("..." if len(recommendation) > 400 else "")

    # Detect intent: casual greeting/comment vs. question/doubt
    user_input = user_question.strip().lower()
    is_greeting_or_casual = any(
        user_input.startswith(word) for word in ["hi", "hello", "hey", "thanks", "ok", "cool"]
    ) or len(user_input.split()) <= 2  # Short inputs treated as casual
    is_question = "?" in user_input or any(
        word in user_input for word in ["how", "what", "why", "when", "where", "can", "should"]
    )

    # Base context setup
    base_context = f"""Imagine you’re a seasoned educational consultant with over 15 years of experience helping students succeed. 
You’ve just worked with a Grade {grade} student who learns best through a {learning_style} style. I’m their guide, and I’m chatting with you about their learning plan.

**Student Context:**
- **Grade:** {grade}
- **Learning Style:** {learning_style}
- **Strengths:** {strengths}
- **Challenges:** {challenges}
- **Resources Available:** {resources}
- **Study Preferences:** {preferences}

**Your Previous Recommendation (Summary):**
{rec_summary}

**My Input:**
{user_question}
"""

    # Tailor instructions based on intent
    if is_greeting_or_casual and not is_question:
        prompt = base_context + """
**How to Respond:**
- Keep it short, casual, and friendly—like a quick chat.
- Match my tone and don’t over-explain.
- Only bring in the student’s profile or recommendation if I ask for it.
- Sound warm and approachable, like a trusted mentor checking in.
"""
    else:  # Questions or detailed queries
        prompt = base_context + """
**How to Respond:**
- Answer my question directly and specifically—get to the point.
- Connect your advice to the student’s profile and prior recommendation where it fits naturally.
- Offer practical, hands-on tips based on your experience, like you’ve seen work with students before.
- Keep it concise but rich enough to be actionable.
- Use a warm, encouraging tone, like you’re confident in my ability to succeed with your guidance.
"""
    return prompt

def enhance_conversation_history(conversation_history, max_context_length=4000):
    """
    Optimizes conversation history to maintain relevant context efficiently, prioritizing key details and recent interactions.

    Args:
        conversation_history (str): The current conversation history
        max_context_length (int): Maximum character length for history

    Returns:
        str: Optimized conversation history
    """
    if len(conversation_history) <= max_context_length:
        return conversation_history

    lines = conversation_history.split("\n")
    profile_lines = [line for line in lines if "student context" in line.lower() or any(field in line.lower() for field in ["grade:", "learning style:", "strengths:", "challenges:", "resources:", "preferences:"])]
    recommendation_lines = [line for line in lines if "previous recommendation" in line.lower() or line.strip().startswith("- ") and not line.strip().startswith("- **")]

    qna_pairs = []
    current_pair = []
    for line in lines:
        if "my input:" in line.lower():
            if current_pair:
                qna_pairs.append("\n".join(current_pair))
            current_pair = [line]
        elif current_pair and line.strip():
            current_pair.append(line)
    if current_pair:
        qna_pairs.append("\n".join(current_pair))

    optimized_lines = profile_lines + [""] + recommendation_lines + [""]
    remaining_length = max_context_length - len("\n".join(optimized_lines))

    for pair in reversed(qna_pairs):
        if len(pair) + len("\n\n") <= remaining_length:
            optimized_lines.append(pair)
            remaining_length -= len(pair) + len("\n\n")
        else:
            break

    optimized_history = "\n".join(optimized_lines).strip()
    if len(optimized_history) > max_context_length:
        optimized_history = optimized_history[:max_context_length].rsplit('\n', 1)[0]
    return optimized_history

# Example usage for testing
if __name__ == "__main__":
    student_profile = {
        "grade": "9",
        "learning_style": "Visual",
        "academic_strengths": ["Mathematics", "Science"],
        "academic_challenges": ["Reading comprehension"],
        "available_resources": ["Laptop", "Internet"],
        "study_preferences": ["Quiet environment"]
    }
    recommendation = "1. Study Techniques:\n- Use flashcards for math.\n- Watch science videos.\n2. Resources:\n- Khan Academy for practice."
    
    # Test casual input
    casual_prompt = create_contextual_chat_prompt("Hello", student_profile, recommendation)
    print("Casual Prompt:\n", casual_prompt, "\n")

    # Test question input
    question_prompt = create_contextual_chat_prompt("How can I improve my reading comprehension?", student_profile, recommendation)
    print("Question Prompt:\n", question_prompt)
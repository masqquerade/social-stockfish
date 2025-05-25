def get_message_prompt(goal, additional_context, chat_history) -> tuple[str, str]:
    return ((
    f"""
    Think step by step.
    First, carefully analyze the conversation using this structured approach:

    ### Step 1: Style Analysis
    - ** Client's tone**: [formal/casual/playful/serious]
    - ** Message length **:[short / medium / long responses]
    - ** Language patterns **:[slang, punctuation habits, emoji usage]
    - ** Sentence structure **:[simple / complex, questions vs statements]

    ### Step 2: Relationship Dynamics
    - ** Current relationship stage **:[strangers / acquaintances / friends / romantic interest]
    - ** Power dynamic **:[equal / one pursuing other / professional]
    - ** Conversation momentum **:[flowing well / stalled / awkward / heated]

    ### Step 3: Goal Assessment
    - ** Primary objective **: {goal}

    ## Message Generation Rules

    1. **CRITICAL**: Mirror the client's exact communication style, NOT the other person's
    2. Match their typical message length (±20% of their average)
    3. Use their vocabulary level and slang preferences
    4. Copy their emoji usage patterns (frequency and types)
    5. Maintain their punctuation and capitalization habits
    6. Respect their level of directness vs. subtlety

    ## Chat History
    <chat_history>
    {chat_history}
    </chat_history>

    ## Client's Goal
    <client_goal>
    {goal}
    </client_goal>

    ## Additional Context
    <additional_context>
    {additional_context}
    </additional_context >

    ## Output Format
    CRITICAL: Do NOT use markdown formatting. Do NOT wrap your response in ```json or ``` blocks;
    Do not add anything else to your answer. Only the pre-set JSON format. Do not add any explanations blocks or your thoughts.
    Output ONLY the raw JSON object with no formatting, no code blocks, no additional text.
    The format is JSON with this structure:
    {{
        "user": "CLIENT_USERNAME",
        "message": "your_suggested_message_here"
    }}
    """
	), "You are an expert communication assistant. Your task is to analyze a conversation and generate an authentic message that matches the client's communication style perfectly.")

def get_message_score_prompt(goal, additional_context, chat_history) -> tuple[str, str]:
    return ((
        f"""
        You will be provided with the following information:

        <chat_history>
        {chat_history}
        </chat_history>

        <client_goal>
        {goal}
        </client_goal>
        
        <additional_context>
        {additional_context}
        </additional_context>

        Your task is to thoroughly analyze this information and provide a valuation of the generated message (LAST MESSAGE IN HISTORY). Follow these steps:

        1. Carefully examine the chat history. Pay close attention to:
           - The relationship dynamic between the participants
           - The tone and style of communication
           - Any recurring themes or topics
           - The level of engagement from both parties
           - Punctuation marks, message writing style

        2. Examine the latest message (the last one in the chat history) in the context of:
           - Its relevance to the ongoing conversation
           - Its potential effectiveness in progressing towards the client's goal
           - Its appropriateness given the established rapport and context
           - **IMPORTANT**: evaluate the message based on the analysis in point 1.

        3. Consider the client's goal and assess how well the generated message (the last one in history) aligns with and advances this objective.

        4. Check the consistency of the chatting style:
           - Compare the linguistic style of the generated message to the client's previous messages
           - Look for discrepancies in capitalization, punctuation, use of emojis, abbreviations, etc.

        After your analysis, you will provide a score for the generated message on a scale from -1 to 1 (floating), where:
        -1 represents a message that is highly ineffective or potentially damaging to the conversation or goal
        0 represents a neutral message that neither helps nor hinders the goal
        1 represents a message that is highly effective in progressing towards the client's goal

        Present your evaluation in the JSON format: 
        {{
        "score": [Provide your score from -1 to 1 here],
        }}
        
        CRITICAL: Do NOT use markdown formatting. Do NOT wrap your response in ```json or ``` blocks;
        Do not add anything else to your answer. Only the pre-set JSON format.
        Output ONLY the raw JSON object with no formatting, no code blocks, no additional text.
        Do not add anything else to your answer. Only the pre-set JSON format.
        Do not add any explanations or your thought.

        Remember, your primary goal is to be a expert in understanding the dynamics between the two people (the client and the chat partner) and to make an informed decision about whether the generated message is effective in achieving the client's goal.
        """
    ), "You are a sophisticated AI designed to analyze conversations and evaluate the effectiveness of messages in achieving specific conversational goals. Your primary function is to assess a newly generated message within the context of a previous chat history and a client's goal.")
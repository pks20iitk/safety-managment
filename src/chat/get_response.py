import logging
from azure_openai import AzureOpenAI  # Assuming AzureOpenAI is a valid import
from config import KEY, API_VERSION, AZURE_ENDPOINT, GENERATIVE_MODEL_NAME

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_response_from_llm(prompt: str, result: str) -> dict:
    """
    Generates a response based on the user's prompt and the provided result context,
    along with follow-up questions.

    Args:
        prompt (str): The user's question or request.
        result (str): The context information obtained from the search results.

    Returns:
        dict: A dictionary containing the generated response and follow-up questions.
    """
    logger.info("Generating response from LLM")
    
    # Prepare the messages for the Azure OpenAI model
    messages = [
        {
            "role": "system",
            "content": (
                f"You have received the following question: '{prompt}'. "
                f"Use the context provided: {result} to generate a relevant response. "
                "Your response should be accurate, coherent, and well-presented. "
                "If the required information is not available, clearly indicate that."
            ),
        },
        {"role": "user", "content": result},
    ]

    # Create an instance of the Azure OpenAI client
    client = AzureOpenAI(
        api_key=KEY,
        api_version=API_VERSION,
        azure_endpoint=AZURE_ENDPOINT,
    )

    try:
        # Generate the completion using the OpenAI model
        completion = client.chat.completions.create(
            model=GENERATIVE_MODEL_NAME,
            messages=messages,
            max_tokens=800
        )
        response_content = completion.choices[0].message.content.strip()
        followup_questions = generate_followup_questions(response_content)

        return {
            "response": response_content,
            "followup_questions": followup_questions
        }

    except Exception as e:
        logger.error(f"Error generating response: {e}")
        return {"error": "An error occurred while generating the response."}
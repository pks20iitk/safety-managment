import logging
from azure_openai import AzureOpenAI  # Assuming AzureOpenAI is a valid import
from config import KEY, API_VERSION, AZURE_ENDPOINT, GENERATIVE_MODEL_NAME
 
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
 
async def generate_response_with_followup(manual_prompt: str, user_prompt: str, search_results: list) -> dict:
    """
    Generates a response based on the user's query and search results, along with follow-up questions.
 
    Args:
        manual_prompt (str): The initial prompt provided by the user.
        user_prompt (str): The user's specific question or request.
        search_results (list): The results obtained from the search operation.
 
    Returns:
        dict: A dictionary containing the generated response and follow-up questions.
    """
    logger.info("Generating response with follow-up questions")
   
    # Construct context information from search results
    context_info = format_search_results(search_results)
 
    # Prepare the messages for the Azure OpenAI model
    messages = [
        {
            "role": "system",
            "content": (
                f"As a proficient language model, you have been given the following query: '{manual_prompt}' "
                f"and context: {context_info}. You possess exceptional skills in comprehending and analyzing context, "
                "as well as a strong foundation in logic, mathematics, and reasoning. Your primary responsibility is to "
                "generate accurate and relevant responses based solely on the context provided. In cases where the "
                "required information is not available, you should clearly indicate that the information is missing. "
                "Additionally, your responses should be well-presented for the user, coherent, and captivating, making "
                "it easy and enjoyable for users to read and understand."
            ),
        },
        {"role": "user", "content": user_prompt},
    ]
 
    # Create an instance of the Azure OpenAI client
    client = AzureOpenAI(
        api_key=KEY,
        api_version=API_VERSION,
        azure_endpoint=AZURE_ENDPOINT,
    )
 
    # Generate the completion using the OpenAI model
    try:
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
 
def format_search_results(search_results: list) -> str:
    """
    Formats the search results into a coherent string for context.
 
    Args:
        search_results (list): The results obtained from the search operation.
 
    Returns:
        str: A formatted string representing the search results.
    """
    formatted_results = "\n".join([f"File: {result['FileName']}, Page: {result['page_num']}, Content: {result['result_content']}" for result in search_results])
    return formatted_results
 
def generate_followup_questions(response: str) -> list:
    """
    Generates follow-up questions based on the provided response.
 
    Args:
        response (str): The generated response from the AI model.
 
    Returns:
        list: A list of follow-up questions related to the response.
    """
    followup_questions = [
        "Can you elaborate more on this topic?",
        "What are the implications of this information?",
        "Are there any examples that illustrate this point?"
    ]
    return followup_questions
import os
import logging
import uvicorn
from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse
from search.algorithm import get_results_vector_search
from search.files_processing import save_highlighted_pdf

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.post("/search")
async def search(
        prompt: str = Form(...),
        algorithm_type: str = Form(...),
        number_of_search_result: int = Form(...),
        number_of_nearest_neighbour: int = Form(...),
        filter_keywords: str = Form(default="")
):
    """
    API endpoint to search for documents based on the provided parameters.

    Args:
        prompt (str): The search query.
        algorithm_type (str): The type of search algorithm to use.
        number_of_search_result (int): The number of search results to return.
        number_of_nearest_neighbour (int): The number of nearest neighbors to consider.
        filter_keywords (str): Keywords to filter the search results.

    Returns:
        JSONResponse: A JSON response containing the search results.
    """
    logger.info("Starting search operation")
    final_results = []

    try:
        result_content, filename, page_num = await get_results_vector_search(
            prompt,
            filter_keywords,
            number_of_search_result,
            number_of_nearest_neighbour,
            algorithm_type == "hybrid",
            algorithm_type == "exhaustive_knn",
            algorithm_type == "semantic"
        )

        if result_content:
            result_dict = {
                "Prompt": prompt,
                "Data": [{"page_num": str(int(page) + 1), "FileName": file, "result_content": content}
                          for page, content in zip(page_num, result_content)]
            }
            final_results.append(result_dict)

            # Save highlighted PDF
            save_highlighted_pdf("user_folder_path", "username", "facility", result_content, filename, page_num)

        logger.info("Search operation completed successfully")
        return JSONResponse(content=final_results, status_code=200)

    except Exception as e:
        logger.error(f"Error during search operation: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8003)
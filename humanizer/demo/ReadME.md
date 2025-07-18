# Simplified Turnitin Demo

This project is a simplified proof-of-concept demonstrating the core principles behind plagiarism and AI writing detection, built with Python and FastAPI.

## Core Concepts Demonstrated

1.  **Plagiarism Detection**: Uses a document "fingerprinting" method. It breaks text into overlapping chunks (shingles), hashes them, and compares the resulting set of hashes using the Jaccard Similarity index.
2.  **AI Writing Detection**: Uses two statistical metrics as proxies:
    *   **Burstiness**: Measures the variation in sentence length. Low variation can be a sign of AI-generated text.
    *   **Vocabulary Richness**: Measures the ratio of unique words to total words. This serves as a simple proxy for the "perplexity" or predictability of word choice.

**Disclaimer:** This is a highly simplified educational tool and **not** a production-ready system. Real-world systems use far more sophisticated models, massive databases, and continuous machine learning.

## How to Run

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the FastAPI Server:**
    ```bash
    uvicorn main:app --reload
    ```
    The server will be running at `http://127.0.0.1:8000`.

3.  **Test the API:**
    You can use tools like `curl`, Postman, or FastAPI's built-in docs at `http://127.0.0.1:8000/docs`.

    **Example `curl` command to test for plagiarism:**
    (This text is very similar to doc_id=1 in our database)
    ```bash
    curl -X POST "http://127.0.0.1:8000/analyze/" \
    -H "Content-Type: application/json" \
    -d '{
      "text": "The Industrial Revolution marked a major transition to brand new manufacturing processes in Europe. This shift included moving from manual production to machine-based methods."
    }'
    ```

    **Example `curl` command to test for AI patterns:**
    (This text has very uniform sentence length)
    ```bash
    curl -X POST "http://127.0.0.1:8000/analyze/" \
    -H "Content-Type: application/json" \
    -d '{
      "text": "The system processes input data. The algorithm calculates the result. The output is then displayed. The user can review the final report. This process is highly efficient."
    }'
    ```
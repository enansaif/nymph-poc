# Assessment Task 0: Conceptual ML Design

## Approach 1: Vector Embedding–Based Semantic Matching

### Data Processing Pipeline
- Data Ingestion: CVs (PDF, DOC, text) and job postings (plain text or HTML).
- Parsing & Cleaning:
  - Text extraction using OCR.
  - Section detection (skills, experience, education, summary).
  - Basic normalization (lowercasing, standardizing job titles and skills).
- Embedding / Feature Engineering:
  - Encode CVs and job postings into embeddings using pretrained embedding models.
  - Generate section-wise embeddings (skills-only, experience-only) and combine them using weighted averages.
  - Generate feature wise embeddings (required-skills, good-to-have, leadership, achievements)
  - Store embeddings in a vector database (FAISS, ChromaDB, Pinecone).

### Model Architecture
- Encoder:
  - Independent encoders for CVs and job postings (same pretrained model).
- Similarity Computation:
  - Cosine similarity between CV and job description embeddings.
- Retrieval Layer:
  - Search vector database for fast retrieval at scale (Match with multiple CVs).
- Output:
  - A similarity score representing overall semantic match between CV and job.

### Pros and Cons
- Pros:
  - Works well for large candidate pools.
  - Requires little or no labeled training data.
  - Easy to update when new CVs or jobs arrive.
  - Can match with multiple candidates fast.
- Cons:
  - Weak at enforcing hard constraints (mandatory skills, minimum experience).
  - May rank related but unsuitable candidates highly.
  - Very difficult to select matching weights and logic.

---

## Approach 2: Transformer-Based Matching with Entity Recognition

### Data Processing Pipeline
- Data Ingestion: Same CV and job posting sources as above.
- Parsing, Cleaning & Entity Extraction:
  - Transformer-based NER models extract skills, job titles, experience duration, education, certifications, tools, and domain entities.
  - Normalize skills, tools, titles (mapping “JS” → “JavaScript”).
  - Classify job requirements as mandatory or preferred and identify minimum experience needed.
- Structured Representation:
  - Convert extracted data into features such as:
    - Skill overlap and coverage
    - Years of experience match
    - Seniority and role alignment
  - Retain original text to preserve context.

### Model Architecture
Encoder:
- The model reads the CV text and the job description together.
- It builds a combined understanding of what the candidate offers and what the job requires.
- The output is a one dimensional vector that represents how related the CV and the job are based on their text.

Entity-Aware Reasoning:
- Important details such as skills, years of experience, and education are identified separately.
- These values are also one dimensional and added on top of the encoder output.
- The model is trained on good and bad CV–job examples, so it learns which parts of the text is more important.
- During comparison, the model focuses more on important sections like skills and requirements.

Prediction Head:
- A final layer takes the combined understanding (and any important extra information).
- It converts this into a single score.

### Pros and Cons
- Pros:
  - Strong understanding of explicit job requirements.
  - Better handling of mandatory skills and experience constraints.
  - Suitable for high-quality shortlisting.
- Cons:
  - Higher inference latency and computational cost.
  - Requires labeled CV–JD pairs or carefully designed schemas.
  - Limited scalability.

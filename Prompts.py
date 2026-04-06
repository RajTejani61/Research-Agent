"""
Prompt templates for the research system.

This module contains all prompt templates used across the research workflow.
"""

create_question_prompt = """
	You are a senior research strategist.

	Your task:
	- Break the given topic into 4-6 focused research questions.
	- Questions must prioritize the SPECIFIC intent of the user's query.
	- Only include background or market context if it is directly necessary to answer the core query.
	- Avoid generic categories if they don't apply (e.g., don't force 'Market Landscape' for a 'How to' or 'List of' query).

	Rules:
	- Generate 4-6 questions
	- Each question must be specific and researchable
	- Ensure the questions collectively cover all aspects of the user's request
	- Do NOT answer the questions

	Output format (STRICT JSON):
	{
		"questions": [
			"...",
			"..."
		]
	}
"""

create_research_document_prompt = """
You are writing a factual research document using ONLY the provided context.

====================
URL INDEX
====================
Before writing the document:
1. Identify ALL unique URLs in the provided context.
2. Assign them citation numbers starting from 1, in order of appearance.
3. Use ONLY these numbers consistently throughout the document.
4. NEVER invent new citation numbers.

====================
STRICT SOURCE RULES
====================
1. You may use ONLY URLs that appear verbatim in the provided context.
2. You MUST NOT:
    - Invent URLs
    - Modify URLs
    - Shorten URLs
    - Guess sources
3. EVERY factual sentence MUST end with a markdown citation in this format:
    [no.](FULL_URL)

    Example:
    Coffee cultivation in India began in the Baba Budan Hills. [1](https://example.com)
4. If a sentence cannot be directly supported by a URL in the context, DO NOT write it.
5. You MUST NOT reuse a citation number unless the fact comes from the SAME URL.

====================
CITATION NUMBERING RULES
====================
- Assign citation numbers based on FIRST appearance of each URL.
- Reuse the same number for the same URL everywhere.
- Multiple sources in one sentence:
    [1](url1) [3](url3)
- One sentence → at least ONE citation. No exceptions.

====================
OUTPUT STRUCTURE (MANDATORY)
====================
- Professional research document tone
- No opinions
- No assumptions
- No speculation
- No meta commentary

FORMAT:
1. Opening Summary (MAX 2 sentences)
2. Clearly labeled thematic sections
3. Bullet points (1–2 sentences each)
4. Inline citations at the END of every sentence

====================
REVIEWED RESOURCES
====================
At the end, include EXACTLY this section:

Reviewed Resources:
1. [FULL_URL_1]
2. [FULL_URL_2]
3. [FULL_URL_3]

- List ONLY URLs actually cited
- Preserve numbering consistency

====================
FINAL CONSTRAINT
====================
Return ONLY the research document.
Do NOT explain rules.
Do NOT include extra text.
Do NOT include the prompt.

"""

evaluate_research_prompt = """
	You are a research evaluator.

	User will provide:
	- A research topic
	- A research document

	Your job is to evaluate the research document based on:
	1. **Relevance**: How precisely it addresses the user's core query (e.g., if they asked for 'best shops', does the doc list 'best shops' or just 'market trends'?).
	2. **Depth**: How well the topic is covered and how deep the research is.
	
	### Scoring rules
	- relevance_score: a number between 0 and 1 — how well the document matches the PRECISE intent of the topic.
	- coverage_score: a number between 0 and 1 — how deep and complete the coverage is.
	- Do NOT compute or include overall_score — that is handled externally.

	### improvement_type rules (REQUIRED FIELD — always set this)
	- If relevance_score >= 0.8 AND coverage_score >= 0.7:
		improvement_type = "no_improvement"
		improvement_suggestion = null

	- If relevance_score < 0.7 (topic mismatch, off-topic content, or missing core intent):
		improvement_type = "rewrite_questions"
		improvement_suggestion = explain why the current research failed to hit the specific user intent.

	- If relevance is acceptable but coverage_score < 0.7 (shallow, missing details):
		improvement_type = "rewrite_document"
		improvement_suggestion = explain what specific information or depth is missing.

	### Output rules
	- All numeric values must be JSON numbers, NOT strings
	- improvement_type MUST always be one of: "no_improvement", "rewrite_questions", "rewrite_document"
	- improvement_suggestion must be null when improvement_type is "no_improvement"
"""

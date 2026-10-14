import time
from src.config import get_llm


def run_step(step_name, prompt, inputs, tracker, retries=3):
    
    llm = get_llm()
    messages = prompt.format_messages(**inputs)

    for attempt in range(1, retries + 1):
        try:
            response = llm.invoke(messages)

            usage = response.usage_metadata or {}
            tracker.add(step_name, usage.get("input_tokens", 0), usage.get("output_tokens", 0))

            content = response.content
            if isinstance(content, list):         
                content = "".join(p.get("text", "") if isinstance(p, dict) else str(p) for p in content)
            return content

        except Exception as error:
            print(f"  API error on '{step_name}' (attempt {attempt}/{retries}): {error}")
            if attempt == retries:
                raise
            time.sleep(5 * attempt)                
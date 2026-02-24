import os
import pathway as pw
from pathway.xpacks.llm import llms

def create_rag(table):

    api_key = os.getenv("OPENAI_API_KEY")

    llm = llms.OpenAIChat(
        model="gpt-4o-mini",
        api_key=api_key,
        temperature=0.3
    )

    @pw.udf
    def explain(title, recommendation):
        prompt = f"""
        News: {title}
        Recommendation: {recommendation}
        Explain briefly why this decision makes sense.
        """
        return llm(prompt)

    return table.select(
        symbol=table.symbol,
        rag_explanation=explain(table.title, table.recommendation)
    )
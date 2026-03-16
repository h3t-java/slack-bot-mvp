from app.rag_pipeline import run_rag

question = "How many vacation days do employees receive?"

answer = run_rag(question)

print(answer)
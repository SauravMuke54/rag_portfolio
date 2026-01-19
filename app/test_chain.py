from rag_chain import build_rag_chain

qa = build_rag_chain()

while True:
    query = input("You: ")
    if query.lower() in ["exit", "quit"]:
        break

    result = qa.invoke({"question": query})
    print(result['chat_history'][-1].content)
    # print("\nBot:", result["answer"])

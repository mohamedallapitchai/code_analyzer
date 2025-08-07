import os
import uuid

from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import GithubFileLoader
from langchain_core.chat_history import InMemoryChatMessageHistory, BaseChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]


if __name__ == '__main__':
    load_dotenv()
    access_token = os.getenv("ACCESS_TOKEN")

    # 1 - Load the github repository
    loader = GithubFileLoader(
        repo="mohamedallapitchai/boundingBox_fullblown",  # the repo name
        branch="main",  # the branch name
        access_token=access_token,
        github_api_url="https://api.github.com",
        file_filter=lambda file_path: file_path.endswith(
            ".scala"
        ) or file_path.endswith(".md"),
    )
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=3000,  # chunk size (characters)
        chunk_overlap=100,  # chunk overlap (characters)
        separators=["\nclass ", "\nobject ", "\n", " "]
    )

    chunks = text_splitter.split_documents(documents)
    #print(f"number of chunks is {len(chunks)}")
    api_key = os.getenv("API_KEY")

    llm = ChatOpenAI(model="gpt-4o", api_key=api_key)

    prompt = ChatPromptTemplate.from_template("""
    You are an expert in Scala software engineering.
    Analyze the following Scala code and explain 
    1) what it is doing and what kind of problem it helps solve.
    ```
    scala
    {code_chunk}
    ```
    """)

    chain = prompt | llm | StrOutputParser()

    summaries = [chain.invoke({"code_chunk": chunk}) for chunk in chunks]
    num_summaries = len(summaries)
    print(f"length of summaries is {len(summaries)}")

    final_prompt_str = """
       Here are the {num_summaries} summaries of different parts of a Scala SDK project:
       {summaries}
       Based on these, Give me a precise problem statement with example input and output so that
       I will ask my developer to develop a program based on the problem statement provided by you.
       Provide as much details as possible for the developer to write a program
       to solve this problem including input restrictions and
       output expected.

       Answers:
      """

    final_prompt_template = (
        ChatPromptTemplate.from_messages([("system", "You are a scala expert."), ("human", final_prompt_str), ]))

    final_chain = final_prompt_template | llm | StrOutputParser()

    # From now on, I want to tweak my response by conversing to the model, so I need chat history
    store = {}
    with_message_history = RunnableWithMessageHistory(final_chain, get_session_history, input_messages_key="summaries")

    uniqueId = str(uuid.uuid4())
    config = {"configurable": {"session_id": uniqueId}}
    response = with_message_history.invoke({"summaries": summaries, "num_summaries": num_summaries}, config=config)
    print(response)
    print("\n\n")
    print("If you are happy with output enter 'bye' otherwise key-in for more clarification")
    normal_prompt_template = ChatPromptTemplate.from_messages([("placeholder", "{text}")])
    normal_chain = normal_prompt_template | llm | StrOutputParser()
    with_message_history_normal = RunnableWithMessageHistory(normal_chain, get_session_history,
                                                             input_messages_key="text")
    text = input("Mohamed: ")

    while True:
        if text != 'bye':
            response = with_message_history_normal.invoke({"text": text}, config)
            print(response)
            print("\n\n")
            print("If you are happy with output enter 'bye' otherwise key-in for more clarification")
            text = input("Mohamed: ")
        else:
            break

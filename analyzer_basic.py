import os

from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import GithubFileLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

if __name__ == '__main__':
    load_dotenv()
    access_token = os.getenv("ACCESS_TOKEN")

    # 1 - Load the github repository
    loader = GithubFileLoader(
        repo="mohamedallapitchai/boundingBoxP",  # the repo name
        branch="main",  # the branch name
        access_token=access_token,
        github_api_url="https://api.github.com",
        file_filter=lambda file_path: file_path.endswith(
            ".scala"
        ),
    )
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=3000,  # chunk size (characters)
        chunk_overlap=100,  # chunk overlap (characters)
        separators=["\nclass ", "\nobject ", "\n", " "]
    )

    chunks = text_splitter.split_documents(documents)
    print(f"number of chunks is {len(chunks)}")
    api_key = os.getenv("API_KEY")

    llm = ChatOpenAI(model="gpt-4o", api_key=api_key)

    prompt = ChatPromptTemplate.from_template("""
    You are an expert in Scala software engineering.
    Analyze the following Scala code and explain what it is doing and what kind of problem it helps solve.

    ```
    scala
    {code_chunk}
    ```
    """)

    chain = prompt | llm | StrOutputParser()

    summaries = [chain.invoke({"code_chunk": chunk}) for chunk in chunks]
    num_summaries = len(summaries)
    print(f"length of summaries is {len(summaries)}")

    final_prompt_template = ChatPromptTemplate.from_template("""
     Here are the {num_summaries} summaries of different parts of a Scala SDK project:
     {summaries}

     Based on these, answer me the following questions.
     Questions:
     1) what is the overall purpose of this codebase? What problem is this project trying to solve?
     and 
     2) Give me 3 examples (runs) of the program with input and output ?
     
     Answers:
    """)

    # final_prompt = final_prompt_template.format(num_summaries=num_summaries, summaries="\n\n".join(summaries))
    # print(f"final_prompt is ${final_prompt}")
    # ready_to_go_prompt = StringPromptValue(text=final_prompt)
    final_chain = final_prompt_template | llm | StrOutputParser()
    response = final_chain.invoke({"num_summaries": num_summaries, "summaries": "\n\n".join(summaries)})
    print(response)

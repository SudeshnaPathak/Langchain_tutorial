from operator import itemgetter
import os
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate , MessagesPlaceholder
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]=os.getenv("LANGCHAIN_TRACING_V2")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

embeddings = OpenAIEmbeddings()
    
db = FAISS.load_local("jalshakti_faiss_index", embeddings,allow_dangerous_deserialization=True)
prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details. If the answer is not related to context, just say "NA" only.\n\n.
    In the user asks to generate a report ingore the 'State Name' and generate the report based on the user question.
    Answer the user question to the best of your ability in proper {language}.
    Answer only from the provided context and not from anywhere else.
    Context:\n {context}?\n
    Question: \n{question}\n
    
    Answer:
    """
llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)
# prompt = PromptTemplate(template = prompt_template , input_variables={"context","question"})

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", prompt_template),
        MessagesPlaceholder(variable_name="messages"),
    ]    
 )

retriever = db.as_retriever()

text_chain = (
    {
        "context": itemgetter("question") | retriever,
        "question": itemgetter("question"),
        "language": itemgetter("language"),
        "messages":itemgetter("messages")
    }
    | prompt
    | llm
    | StrOutputParser()
)

# while True:
#     question = input("Query: ")
#     language = input("Language: ")
#     SessionId = input("SessionId: ")
#     response = text_chain.invoke(
#         {"question" : question , "language" : language ,"messages": [HumanMessage(content=question)]}
#         ,config={"configurable": {"session_id": SessionId}}
#         )
#     print(response)


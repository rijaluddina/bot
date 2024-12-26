from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import START, StateGraph, add_messages
from langgraph.checkpoint.memory import MemorySaver
from typing_extensions import Annotated, TypedDict
from connect.utils.terminal.markdown import render
from prompt_toolkit.formatted_text import HTML
from langchain_groq import ChatGroq
from prompt_toolkit import prompt
from dotenv import load_dotenv
from typing import Sequence

load_dotenv()

COLOR_GREEN = "\033[0;32m"
COLOR_BLUE = "\033[0;34m"
COLOR_NC = "\033[0m"

prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a helpful assistant. Answer all questions to the best of your ability in {language}.
            If you are required to answer with program code, make sure it is in the form of a code block and accompanied by the correct syntax, for example:
                ```python
                print("hello world")
                ```
            """,
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)
model = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.75,
)


class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    language: str

workflow = StateGraph(state_schema=State)

def create_prompt(state: State) -> str:
    return prompt_template.invoke(state)

def invoke_model(prompt: str) -> dict:
    return model.invoke(prompt)

def call_model(state: State) -> dict:
    prompt = create_prompt(state)
    response = invoke_model(prompt)
    return {"messages": response}

def prompt_continuation(width:int, line_number:int, wrap_count:int) -> str:
    if wrap_count > 0:
        return " " * (width - 3) + "-> "
    else:
        text = ("%i." % (line_number)).rjust(width)
        return HTML(f"<strong>{text}</strong>")

workflow.add_edge(START, "model")
workflow.add_node("model", call_model)

memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

config = {"configurable": {"thread_id": "uuid"}}

while True:
    print(f"{COLOR_BLUE}###PROMPT :{COLOR_NC}")
    query = prompt(
        HTML("<strong>1.</strong>"),
        multiline=True,
        prompt_continuation=lambda width, line_number, wrap_count: prompt_continuation(0, line_number + 1, wrap_count),
    )
    language = "indonesian"

    if query.strip().upper() == "Q":
        break
    if len(query.strip()) < 3:
        print("Messages must be a minimum of 3 characters.")
        continue

    input_messages = [HumanMessage(query)]
    output = app.invoke({"messages": input_messages, "language": language}, config=config)
    json = output["messages"][-1]
    print(f"{COLOR_GREEN}###ANSWER :{COLOR_NC}")
    print(render(json.content))

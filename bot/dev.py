from prompt_toolkit import prompt
from prompt_toolkit.formatted_text import HTML
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import START, StateGraph, add_messages
from langgraph.checkpoint.memory import MemorySaver
from connect.utils.terminal.markdown import render
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from typing import Sequence
from typing_extensions import Annotated, TypedDict

load_dotenv()
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
model = ChatGroq(model="llama3-8b-8192")


class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    language: str


workflow = StateGraph(state_schema=State)


def call_model(state: State):
    prompt = prompt_template.invoke(state)
    response = model.invoke(prompt)
    return {"messages": response}


workflow.add_edge(START, "model")
workflow.add_node("model", call_model)

memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

config = {"configurable": {"thread_id": "uuid"}}


def prompt_continuation(width, line_number, wrap_count):
    """Display continuation prompt with line numbers and arrow."""
    if wrap_count > 0:
        return " " * (width - 3) + "-> "
    else:
        text = ("%i." % (line_number)).rjust(width)
        return HTML(f"<strong>{text}</strong>")


while True:
    query = prompt(
        HTML("<strong>1.</strong>"),  # Initial prompt
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
    output = app.invoke({"messages": input_messages, "language": language}, config)
    json = output["messages"][-1]
    print(render(json.content))


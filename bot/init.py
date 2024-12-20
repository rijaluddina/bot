from prompt_toolkit import prompt
from prompt_toolkit.formatted_text import HTML

# def prompt_continuation(width, line_number, wrap_count):
#     if wrap_count > 0:
#         return " " * (width - 3) + "-> "
#     else:
#         text = ("%i." % (line_number)).rjust(width)
#         return HTML(f"<strong>{text}</strong>")

def prompt_continuation(width, line_number, _):
    return HTML(f"<strong>{line_number}.</strong>".rjust(width)) if line_number > 1 else " " * (width - 3) + ">>> "

def main():
    # Set the width for the prompt, aligning with the continuation prompt.
    initial_prompt_width = 5  # Adjust this value as needed.
    initial_prompt = HTML(f"<strong>{('%i.' % 1).rjust(initial_prompt_width)}</strong>")

    answer = prompt(
        initial_prompt,  # Display line number 1 directly with strong formatting
        multiline=True,
        prompt_continuation=lambda width, line_number, _: prompt_continuation(initial_prompt, line_number + 1, _),
        # prompt_continuation=lambda width, line_number, wrap_count: prompt_continuation(initial_prompt_width, line_number + 1, wrap_count),
    )

# INITIAL_PROMPT_WIDTH = 0  # Adjust this value as needed.
# initial_prompt = HTML("<strong>1.</strong>".rjust(INITIAL_PROMPT_WIDTH))
#
# if __name__ == "__main__":
#     # Set the width for the prompt, aligning with the continuation prompt.
#     # initial_prompt_width = 5  # Adjust this value as needed.
#     # initial_prompt = HTML(f"<strong>{('%i.' % 1).rjust(initial_prompt_width)}</strong>")
#
#     answer = prompt(
#         initial_prompt,  # Display line number 1 directly with strong formatting
#         multiline=True,
#         prompt_continuation=lambda width, line_number, _: prompt_continuation(INITIAL_PROMPT_WIDTH, line_number + 1, _),
#         # prompt_continuation=lambda width, line_number, wrap_count: prompt_continuation(initial_prompt_width, line_number + 1, wrap_count),
#     )
#     print(f"You said: {answer}")


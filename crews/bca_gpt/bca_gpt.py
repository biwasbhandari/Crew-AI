import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from dotenv import load_dotenv

load_dotenv()

# Define Search Tool
search_tool = SerperDevTool()

# Agent Configuration
bca_question_agent = Agent(
    role="BCA Question Searcher",
    goal=(
        "To assist BCA faculty of Tribhuvan University by searching for questions and MCQs."
        "Search is strictly limited to BCA subjects of Tribhuvan University."
    ),
    backstory=(
        "As an expert assistant for academic research, you specialize in helping Tribhuvan University"
        "BCA faculty. Your deep knowledge of the curriculum ensures that all searches are accurate and relevant."
    ),
    tools=[search_tool],
    allow_delegation=False,
    memory=True,
    verbose=True
)

# Task Examples
# chat_task = Task(
#     description=(
#         "Engage in conversation with the user. Answer their questions in a friendly and helpful manner, "
#         "without conducting external research."
#     ),
#     expected_output="A conversational response addressing the user's inquiry.",
#     agent=bca_question_agent,
# )

research_task = Task(
    description=(
        "Search for question papers, MCQs, or answers for BCA subjects under Tribhuvan University. "
        "Ensure results are specific to the given query and relevant to the curriculum."
        "Here's what the student wants:"
        "{question}"
    ),
    expected_output="A list of relevant questions, question papers, or MCQs specific to the subject.",
    tools=[search_tool],
    agent=bca_question_agent,
)

# dual_mode_task = Task(
#     description=(
#         "Retrieve both questions and answers for the specified BCA subject under Tribhuvan University. "
#         "Present the data in a clear and concise format."
#     ),
#     expected_output=(
#         "A structured response containing: \n"
#         "- Relevant questions (MCQs or question papers).\n"
#         "- Answers or suggested solutions for the questions."
#     ),
#     tools=[search_tool],
#     agent=bca_question_agent,
# )

# Crew Configuration
bca_crew = Crew(
    agents=[bca_question_agent],
    tasks=[ research_task],
    process=Process.sequential
)

question = input("Question: ")

# Example Kickoff
result = bca_crew.kickoff(inputs={"question":question})
print(result)

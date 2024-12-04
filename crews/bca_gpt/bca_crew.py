import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Define Search Tool
search_tool = SerperDevTool()

def create_bca_research_crew():
    """
    Create and configure the BCA research crew
    """
    # Agent Configuration
    bca_question_agent = Agent(
        role="BCA Question Searcher",
        goal=(
            "To assist BCA faculty of Tribhuvan University by searching for questions and MCQs. "
            "Search is strictly limited to BCA subjects of Tribhuvan University."
        ),
        backstory=(
            "As an expert assistant for academic research, you specialize in helping Tribhuvan University "
            "BCA faculty. Your deep knowledge of the curriculum ensures that all searches are accurate and relevant."
        ),
        tools=[search_tool],
        allow_delegation=False,
        memory=True,
        verbose=True
    )

    # Research Task
    research_task = Task(
        description=(
            "Search for question papers, MCQs, or answers for BCA subjects under Tribhuvan University. "
            "Ensure results are specific to the given query and relevant to the curriculum. "
            "Here's what the student wants: {question}"
        ),
        expected_output="A list of relevant questions, question papers, or MCQs specific to the subject.",
        tools=[search_tool],
        agent=bca_question_agent,
    )

    # Crew Configuration
    bca_crew = Crew(
        agents=[bca_question_agent],
        tasks=[research_task],
        process=Process.sequential
    )

    return bca_crew

def run_bca_research(question: str) -> str:
    """
    Run BCA research for a given question
    
    Args:
        question (str): The research question to search for
    
    Returns:
        str: Research results
    """
    # Create the crew
    bca_crew = create_bca_research_crew()
    
    # Run the research
    result = bca_crew.kickoff(inputs={"question": question})
    
    return result

# Optional: If you want to keep the CLI interface for local testing
if __name__ == "__main__":
    question = input("Question: ")
    result = run_bca_research(question)
    print(result)
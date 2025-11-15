import os
import logging
from adk.api.llms import Gemini
from adk.api.runners import Runner
from adk.api.sessions import InMemorySessionService

# Import your agents
from agents.orchestrator import OrchestratorAgent
from agents.persona_generator import PersonaGeneratorAgent
from agents.red_team import RedTeamAgent
from agents.report_agent import ReportAgent

# Configure logging
def setup_logging(name: str) -> logging.Logger:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    return logging.getLogger(name)

logger = setup_logging("ChitraguptaRunner")

def main():
    # Load API key from environment variable
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        logger.error("GOOGLE_API_KEY environment variable not set.")
        logger.info("Please set GOOGLE_API_KEY before running the server.")
        return

    llm = Gemini(api_key=google_api_key)
    session_service = InMemorySessionService()

    # Initialize specialist agents
    persona_generator = PersonaGeneratorAgent(llm=llm)
    red_team_agent = RedTeamAgent(llm=llm)
    report_agent = ReportAgent(llm=llm)

    # Initialize Orchestrator and inject specialist agents
    orchestrator = OrchestratorAgent(
        llm=llm,
        session_service=session_service,
        persona_agent=persona_generator,
        red_team_agent=red_team_agent,
        report_agent=report_agent,
    )

    runner = Runner(
        agents=[orchestrator], # Only the orchestrator is exposed for external calls
        llm=llm,
        session_service=session_service,
    )

    logger.info("Starting ADK Runner. Agents available at http://localhost:8080")
    logger.info("Remember to run the client.py in a separate terminal.")
    runner.run()

if __name__ == "__main__":
    main()

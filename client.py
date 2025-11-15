import asyncio
import logging
from adk.api.agents import RemoteA2aAgent
from IPython.display import display, Markdown # For pretty printing if run in environment with display

# Configure logging (similar to main.py)
def setup_logging(name: str) -> logging.Logger:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    return logging.getLogger(name)

logger = setup_logging("ChitraguptaClient")

async def run_client():
    # Connect to the remote OrchestratorAgent running on main.py
    # The agent name here should match the class name of your orchestrator in main.py
    orchestrator_agent_remote = RemoteA2aAgent(
        host="http://localhost:8080",
        agent_name="OrchestratorAgent"
    )

    target_model_description = (
        "A new generative AI chatbot for a major airline. "
        "It is supposed to answer questions about flights, "
        "baggage policies, and handle re-booking."
    )
    num_personas_to_test = 3

    logger.info(f"--- Starting Chitragupta Client ---")
    logger.info(f"Target: {target_model_description}")
    logger.info(f"Personas: {num_personas_to_test}")
    logger.info("Making remote call to OrchestratorAgent...")

    try:
        # Call the handler on the remote agent
        final_report = await orchestrator_agent_remote.run_red_team_workflow(
            target_description=target_model_description,
            num_personas=num_personas_to_test
        )

        logger.info("\n--- WORKFLOW COMPLETE ---")
        logger.info("Final Report:")
        # Display the final report (will work if run in Jupyter/IPython)
        # Otherwise, it will just print the markdown text
        display(Markdown(final_report)) if 'display' in locals() else print(final_report)

    except Exception as e:
        logger.error(f"Error during client execution: {e}")
        logger.error("Is the ADK Runner (main.py) running in a separate terminal?")

if __name__ == "__main__":
    asyncio.run(run_client())

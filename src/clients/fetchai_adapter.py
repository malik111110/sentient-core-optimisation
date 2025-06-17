from uagents import Agent, Context

class FetchAIAdapter:
    """
    An adapter to interact with the Fetch.ai uAgent ecosystem.
    This class will manage the creation, registration, and discovery of agents.
    """
    def __init__(self, name: str, seed: str):
        """
        Initializes the FetchAI adapter and creates a base agent.

        Args:
            name: The name of the agent.
            seed: The recovery phrase for the agent's identity.
        """
        self.agent = Agent(name=name, seed=seed)
        self.agent.on_event("startup")(self._on_startup)

    async def _on_startup(self, ctx: Context):
        ctx.logger.info(f"Agent '{self.agent.name}' started with address: {self.agent.address}")
        ctx.logger.info("Registered on Almanac contract.")

    def run(self):
        """
        Runs the agent, connecting it to the Fetch.ai network.
        """
        self.agent.run()

    # Placeholder for future functionality
    def discover_agents(self, query: str):
        """
        Discovers agents on the network based on a query.
        (This functionality will be built out later)
        """
        self.agent.logger.info(f"Discovery for '{query}' not yet implemented.")
        return []

# Example Usage:
if __name__ == '__main__':
    # The seed should be a unique phrase for your agent
    adapter = FetchAIAdapter(name="sentient_core_nexus", seed="sentient_core_hackathon_agent_seed_phrase")
    
    @adapter.agent.on_interval(period=10.0)
    async def say_hello(ctx: Context):
        ctx.logger.info(f"Hello from {ctx.agent.name}")

    adapter.run()

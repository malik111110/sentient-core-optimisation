# Fetch.ai uAgents - Developer Guide (Python)

This guide provides a summary of how to develop Fetch.ai uAgents (micro-agents) in Python, based on official Fetch.ai documentation. uAgents are lightweight, autonomous agents capable of communicating with each other and performing tasks.

## 1. Installation

Install the Fetch.ai uAgents library:

```bash
pip install uagents
```

## 2. Core Concepts

*   **Agent:** The fundamental building block. Represents an autonomous entity.
*   **Bureau:** A manager for running one or more agents in the same process.
*   **Context:** An object provided to agent handlers, offering access to logging, message sending, storage, etc.
*   **Model:** A Pydantic-like class (inheriting from `uagents.Model`) defining the structure of messages exchanged between agents.
*   **Protocol:** Defines a set of rules and message types for specific interactions. Useful for service discovery and standardized communication, especially when interacting with the Agentverse.

## 3. Creating and Funding an Agent

A complete, runnable example of a single agent that includes the essential funding step.

```python
from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low

# Define a message model
class MyMessage(Model):
    text: str
    value: int

# Create an agent instance
# The 'seed' is crucial for the agent's identity and cryptographic keys. Keep it secret.
# 'port' and 'endpoint' are for network communication.
alice = Agent(
    name="alice",
    seed="alice_secure_recovery_phrase",
    port=8000,
    endpoint=["http://localhost:8000/submit"]
)

# Fund the agent's wallet if it's low on funds.
# This is crucial for agents that need to transact on the network.
fund_agent_if_low(alice.wallet.address())

@alice.on_event("startup")
async def agent_startup(ctx: Context):
    ctx.logger.info(f"Hello, I'm agent {alice.name} and my address is {alice.address}")

# More handlers (on_message, on_interval) would go here

# To run a single agent, use the run() method
if __name__ == "__main__":
    alice.run()
```

## 4. Message Handling

Agents react to messages or perform tasks at intervals using handlers.

### Receiving Messages

```python
@alice.on_message(model=MyMessage)
async def alice_message_handler(ctx: Context, sender: str, msg: MyMessage):
    ctx.logger.info(f"Received message from {sender}: '{msg.text}' with value {msg.value}")
    # Optionally send a reply
    # await ctx.send(sender, AnotherMessageModel(response="Got it!"))
```

### Sending Messages Periodically

```python
@alice.on_interval(period=5.0) # Time in seconds
async def send_periodic_message(ctx: Context):
    # Replace with a valid recipient agent's address
    bob_address = "agent1q..." # Example, get actual address
    if bob_address != alice.address: # Avoid sending to self unless intended
        await ctx.send(bob_address, MyMessage(text="Periodic ping from Alice!", value=123))
        ctx.logger.info("Sent periodic message.")
```

## 5. Agent Communication

### Asynchronous Messaging

This is the standard way agents communicate.

```python
# In agent_A.py
# ...
await ctx.send(recipient_agent_address, MessageModelToSent(...))

# In agent_B.py
@agent_B.on_message(model=MessageModelToSent)
async def handle_message(ctx: Context, sender: str, msg: MessageModelToSent):
    ctx.logger.info(f"Agent B received: {msg}")
```

### Synchronous Messaging (Request-Reply)

For when an agent needs to send a message and wait for a specific reply.

```python
# In agent_A.py (requester)
class QueryMessage(Model):
    query: str

class AnswerMessage(Model):
    answer: str

# ...
try:
    response = await ctx.ask(
        destination=recipient_agent_address,
        message=QueryMessage(query="What is the weather?"),
        timeout=10.0 # Optional timeout in seconds
    )
    if isinstance(response, AnswerMessage):
        ctx.logger.info(f"Received answer: {response.answer}")
    elif isinstance(response, ErrorModel): # Assuming you have an ErrorModel
        ctx.logger.error(f"Recipient responded with error: {response.error_message}")
    else:
        ctx.logger.warning(f"Received unexpected response type: {type(response)}")
except Exception as e: # Handles timeout or other comms errors
    ctx.logger.error(f"Failed to get a timely response: {e}")


# In agent_B.py (responder)
# Agent B needs a handler for QueryMessage that can reply with AnswerMessage or ErrorModel.
# This is typically done by defining `replies` in the on_message decorator.

@agent_B.on_message(model=QueryMessage, replies={AnswerMessage, ErrorModel})
async def handle_query(ctx: Context, sender: str, msg: QueryMessage):
    if msg.query == "What is the weather?":
        await ctx.send(sender, AnswerMessage(answer="Sunny with a chance of agents!"))
    else:
        await ctx.send(sender, ErrorModel(error_message="Sorry, I can't answer that."))
```

## 6. Running Agents (Bureau)

The `Bureau` class manages and runs multiple agents.

```python
from uagents import Bureau

bob = Agent(name="bob", seed="bob_secure_recovery_phrase", port=8001, endpoint=["http://localhost:8001/submit"])
# ... define Bob's handlers ...

# Create a bureau
bureau = Bureau()
bureau.add(alice)
bureau.add(bob)

# Run the bureau (this will start all added agents)
if __name__ == "__main__":
    bureau.run()
```

## 7. Agent Storage

uAgents have a simple key-value storage mechanism.

```python
@alice.on_event("startup")
async def alice_startup(ctx: Context):
    ctx.storage.set("my_key", "my_value_123")
    retrieved_value = ctx.storage.get("my_key")
    ctx.logger.info(f"Stored and retrieved: {retrieved_value}")
```

## 8. Protocols

Protocols help define structured interactions and are important for discoverability, especially with the Agentverse.

```python
from uagents import Protocol

# Define a protocol
weather_protocol = Protocol("WeatherService", version="1.0")

@weather_protocol.on_message(model=QueryMessage, replies=AnswerMessage)
async def handle_weather_query(ctx: Context, sender: str, msg: QueryMessage):
    # Logic to get weather and send AnswerMessage
    await ctx.send(sender, AnswerMessage(answer="It's always sunny in the Agentverse!"))

# Include protocol in an agent
weather_agent = Agent(name="weather_oracle", seed="weather_seed_phrase")
weather_agent.include(weather_protocol, publish_manifest=True) # publish_manifest for Agentverse
```

## 9. Agentverse

The Agentverse is Fetch.ai's platform for hosting, discovering, and interacting with uAgents.
*   To run an agent on Agentverse, you typically need to provide a public endpoint.
*   Publishing a manifest (often done by including a Protocol with `publish_manifest=True`) makes your agent's services discoverable.

## 10. Key Considerations

*   **Seed Phrases:** These are vital for your agent's identity and security. Store them securely and never expose them publicly.
*   **Endpoints:** Ensure your agent's endpoints are correctly configured and accessible if other agents or services need to reach it over the network.
*   **Error Handling:** Implement robust error handling for message processing and communication failures.
*   **State Management:** Use agent storage or external databases for more complex state persistence.

This guide provides a foundational understanding. For advanced topics, specific examples, and the latest updates, always refer to the [official Fetch.ai Documentation](https://fetch.ai/docs).

import os
from groq import Groq

class GroqService:
    """
    A client for interacting with the Groq API to get completions from Llama 3.
    """
    def __init__(self):
        self.api_key = os.environ.get("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY environment variable not set.")
        self.client = Groq(api_key=self.api_key)

    def get_completion(self, prompt: str, model: str = "llama3-8b-8192") -> str:
        """
        Gets a completion from the specified Groq model.

        Args:
            prompt: The user's prompt.
            model: The model to use for the completion.

        Returns:
            The model's response text.
        """
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=model,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            print(f"An error occurred while communicating with Groq API: {e}")
            return "Error: Could not get completion from Groq."

# Example Usage:
if __name__ == '__main__':
    # Make sure to set the GROQ_API_KEY in your environment variables
    # export GROQ_API_KEY='your_api_key_here'
    groq_service = GroqService()
    response = groq_service.get_completion("Explain the importance of low-latency LLMs")
    print(response)

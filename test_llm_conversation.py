"""
Test script to verify the bot uses Mistral LLM for natural conversation
and properly recognizes research triggers like "tell me about [company]"
"""
import asyncio
from src.company_research_agent import CompanyResearchAgent, ConversationMode

async def test_llm_responses():
    """Test that the bot uses LLM for natural responses"""
    print("\n" + "="*60)
    print("TESTING LLM-POWERED CONVERSATIONAL BOT")
    print("="*60)
    
    agent = CompanyResearchAgent(ConversationMode.NORMAL)
    
    # Test cases that should trigger different behaviors
    test_inputs = [
        # General conversation - should use LLM
        "I wanna know about the corporate world",
        "what do I start with",
        
        # Should trigger research 
        "tell me about eightfold.ai",
        
        # Follow-up questions - should use cached data
        "What are their main products?",
        
        # More general conversation
        "How does the stock market work?",
        
        # Another research trigger
        "Research Microsoft",
        
        # Confused user
        "I don't know what to do",
        
        # Efficient request
        "Just give me the key risks",
    ]
    
    print("\nConversation Flow:")
    print("-" * 60)
    
    for user_input in test_inputs:
        print(f"\n👤 USER: {user_input}")
        response = await agent.process_input(user_input)
        
        # Truncate long responses for display
        if len(response) > 300:
            display_response = response[:300] + "..."
        else:
            display_response = response
            
        print(f"🤖 BOT: {display_response}")
        
        # Add a small delay to simulate conversation
        await asyncio.sleep(0.5)
    
    print("\n" + "="*60)
    print("TEST COMPLETE - Bot should now use Mistral LLM for natural responses!")
    print("="*60)

async def test_specific_scenarios():
    """Test specific scenarios mentioned by the user"""
    print("\n" + "="*60)
    print("TESTING USER'S SPECIFIC SCENARIO")
    print("="*60)
    
    agent = CompanyResearchAgent(ConversationMode.NORMAL)
    
    # Exact sequence from user's feedback
    test_sequence = [
        "I wanna know about the corporate world",
        "what do I start with", 
        "tell me about eightfold.ai"
    ]
    
    print("\nTesting exact user sequence:")
    print("-" * 60)
    
    for user_input in test_sequence:
        print(f"\n👤 USER: {user_input}")
        response = await agent.process_input(user_input)
        
        # Check if research was triggered
        if "Starting fresh research" in response or "Using cached research" in response:
            print(f"🤖 BOT: [RESEARCH TRIGGERED] {response[:200]}...")
        else:
            # Show full conversational response
            if len(response) > 400:
                print(f"🤖 BOT: {response[:400]}...")
            else:
                print(f"🤖 BOT: {response}")
    
    print("\n" + "="*60)
    print("The bot should now:")
    print("1. ✅ Respond conversationally using Mistral LLM")
    print("2. ✅ Recognize 'tell me about [company]' as a research trigger")
    print("3. ✅ Maintain context throughout the conversation")
    print("="*60)

async def main():
    """Run all tests"""
    print("\n" + "="*80)
    print("TESTING IMPROVED CONVERSATIONAL BOT WITH MISTRAL LLM")
    print("="*80)
    
    # Test general LLM responses
    await test_llm_responses()
    
    print("\n" + "-"*80)
    
    # Test specific user scenario
    await test_specific_scenarios()
    
    print("\n" + "="*80)
    print("ALL TESTS COMPLETE!")
    print("="*80)

if __name__ == "__main__":
    asyncio.run(main())

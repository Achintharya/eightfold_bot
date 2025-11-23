"""
Test script to demonstrate improved conversational handling for different user personas
"""
import asyncio
from src.company_research_agent import CompanyResearchAgent, ConversationMode

async def test_confused_user():
    """Test handling of confused/vague users"""
    print("\n" + "="*60)
    print("TEST: CONFUSED USER")
    print("="*60)
    
    agent = CompanyResearchAgent(ConversationMode.NORMAL)
    
    test_inputs = [
        "I want to research a company but I don't know where to start",
        "I just need something about this startup... Idk what exactly",
        "Can you tell me what I should include?",
        "Research Microsoft"  # Finally gives a clear command
    ]
    
    for user_input in test_inputs:
        print(f"\nUser: {user_input}")
        response = await agent.process_input(user_input)
        print(f"Bot: {response[:300]}...")  # Show first 300 chars

async def test_efficient_user():
    """Test handling of efficient users who want quick results"""
    print("\n" + "="*60)
    print("TEST: EFFICIENT USER")
    print("="*60)
    
    agent = CompanyResearchAgent(ConversationMode.EFFICIENT)
    
    test_inputs = [
        "Just give me the key decision-makers and top 3 risks",  # No company yet
        "Research Tesla",  # Clear, direct
        "What are their main challenges?",  # Follow-up - should use cache
        "Quick summary"  # Wants concise info
    ]
    
    for user_input in test_inputs:
        print(f"\nUser: {user_input}")
        response = await agent.process_input(user_input)
        print(f"Bot: {response[:300]}...")

async def test_chatty_user():
    """Test handling of chatty users who go off-topic"""
    print("\n" + "="*60)
    print("TEST: CHATTY USER")
    print("="*60)
    
    agent = CompanyResearchAgent(ConversationMode.CHATTY)
    
    test_inputs = [
        "Hi! I had the worst coffee today lol",
        "Anyway, I need an account plan for Apple",
        "Wait, how do you even know this stuff?",
        "Tell me about their products"  # Should answer from cache
    ]
    
    for user_input in test_inputs:
        print(f"\nUser: {user_input}")
        response = await agent.process_input(user_input)
        print(f"Bot: {response[:300]}...")

async def test_edge_cases():
    """Test handling of edge cases and invalid inputs"""
    print("\n" + "="*60)
    print("TEST: EDGE CASES")
    print("="*60)
    
    agent = CompanyResearchAgent(ConversationMode.NORMAL)
    
    test_inputs = [
        "",  # Empty input
        "😊",  # Emoji only
        "Make an account plan for asdfghjkl Pvt Ltd",  # Non-existent company
        "Give me internal sales data of Google",  # Impossible request
        "Microsoft",  # Just company name - should NOT auto-research
        "Apple is cool",  # Casual mention - should NOT auto-research
        "Research Apple"  # Explicit request - SHOULD research
    ]
    
    for user_input in test_inputs:
        print(f"\nUser: '{user_input}'")
        response = await agent.process_input(user_input)
        print(f"Bot: {response[:300]}...")

async def test_conversation_flow():
    """Test that bot is conversational until research is explicitly needed"""
    print("\n" + "="*60)
    print("TEST: CONVERSATION FLOW - NO AUTO-RESEARCH")
    print("="*60)
    
    agent = CompanyResearchAgent(ConversationMode.NORMAL)
    
    test_inputs = [
        "Tesla",  # Just mentioning company - should NOT research
        "I'm interested in Tesla",  # Still vague - should NOT research
        "Tell me about Tesla",  # Still conversational - should NOT research
        "Research Tesla",  # EXPLICIT - should research
        "What are their main products?",  # Follow-up - should use cache
        "How about their challenges?",  # Another follow-up - should use cache
    ]
    
    for user_input in test_inputs:
        print(f"\nUser: {user_input}")
        response = await agent.process_input(user_input)
        # Check if it's actually researching or just being conversational
        if "Starting fresh research" in response or "Using cached research" in response:
            print(f"Bot: [RESEARCHING] {response[:200]}...")
        else:
            print(f"Bot: [CONVERSATIONAL] {response[:200]}...")

async def main():
    """Run all test scenarios"""
    print("\n" + "="*80)
    print("TESTING IMPROVED CONVERSATIONAL BOT HANDLING")
    print("="*80)
    
    await test_confused_user()
    print("\n" + "-"*80)
    
    await test_efficient_user()
    print("\n" + "-"*80)
    
    await test_chatty_user()
    print("\n" + "-"*80)
    
    await test_edge_cases()
    print("\n" + "-"*80)
    
    await test_conversation_flow()
    
    print("\n" + "="*80)
    print("TESTS COMPLETE!")
    print("="*80)

if __name__ == "__main__":
    asyncio.run(main())

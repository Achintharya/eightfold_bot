"""
Demo Scenarios for Company Research Agent
Testing different user personas and conversation styles
"""

import asyncio
import sys
from src.company_research_agent import CompanyResearchAgent, ConversationMode

class DemoScenarios:
    """Demonstration scenarios for different user types"""
    
    def __init__(self):
        self.scenarios = {
            "confused": self.confused_user_scenario,
            "efficient": self.efficient_user_scenario,
            "chatty": self.chatty_user_scenario,
            "edge": self.edge_case_scenario
        }
    
    async def confused_user_scenario(self):
        """The Confused User - unsure what they want"""
        print("\n" + "="*60)
        print("DEMO: THE CONFUSED USER")
        print("User who is unsure what they want")
        print("="*60 + "\n")
        
        agent = CompanyResearchAgent(ConversationMode.NORMAL)
        
        # Simulate confused user interactions
        confused_inputs = [
            "um, i need to... research something?",
            "maybe a tech company?",
            "actually wait, what can you do?",
            "ok let me think... microsoft? or was it apple?",
            "Microsoft",
            "what's happening now?",
            "can you explain what you found?"
        ]
        
        for user_input in confused_inputs:
            print(f"\n[Confused User]: {user_input}")
            response = await agent.process_input(user_input)
            print(f"[Agent]: {response}")
            await asyncio.sleep(1)  # Pause for readability
    
    async def efficient_user_scenario(self):
        """The Efficient User - wants quick results"""
        print("\n" + "="*60)
        print("DEMO: THE EFFICIENT USER")
        print("User who wants quick, direct results")
        print("="*60 + "\n")
        
        agent = CompanyResearchAgent(ConversationMode.EFFICIENT)
        
        # Simulate efficient user interactions
        efficient_inputs = [
            "Tesla",
            "status",
            "edit opportunities",
            "Focus on AI and autonomous driving opportunities"
        ]
        
        for user_input in efficient_inputs:
            print(f"\n[Efficient User]: {user_input}")
            response = await agent.process_input(user_input)
            print(f"[Agent]: {response}")
            await asyncio.sleep(1)
    
    async def chatty_user_scenario(self):
        """The Chatty User - frequently goes off topic"""
        print("\n" + "="*60)
        print("DEMO: THE CHATTY USER")
        print("User who likes to chat and goes off topic")
        print("="*60 + "\n")
        
        agent = CompanyResearchAgent(ConversationMode.CHATTY)
        
        # Simulate chatty user interactions
        chatty_inputs = [
            "Hi there! How are you doing today?",
            "Oh that's nice! So I was thinking about researching this company",
            "It's called Amazon, have you heard of it?",
            "Wow, you know I actually ordered something from them yesterday!",
            "How's the research going?",
            "This is so cool! Can you tell me more about their challenges?"
        ]
        
        for user_input in chatty_inputs:
            print(f"\n[Chatty User]: {user_input}")
            response = await agent.process_input(user_input)
            print(f"[Agent]: {response}")
            await asyncio.sleep(1)
    
    async def edge_case_scenario(self):
        """Edge Case Users - unusual requests"""
        print("\n" + "="*60)
        print("DEMO: EDGE CASE USERS")
        print("Users with unusual or challenging requests")
        print("="*60 + "\n")
        
        agent = CompanyResearchAgent(ConversationMode.CONFUSED)
        
        # Simulate edge case interactions
        edge_inputs = [
            "",  # Empty input
            "SHOUTING AT YOU IN ALL CAPS",
            "research company that doesn't exist xyz123corp",
            "🚀 emoji company 🎉",
            "tell me about multiple companies: Google Apple Microsoft",
            "edit all sections at once",
            "asdfghjkl",  # Gibberish
            "help",
            "exit"
        ]
        
        for user_input in edge_inputs:
            if user_input:
                print(f"\n[Edge User]: {user_input}")
            else:
                print(f"\n[Edge User]: (empty input)")
            response = await agent.process_input(user_input)
            print(f"[Agent]: {response}")
            await asyncio.sleep(1)
    
    async def run_all_demos(self):
        """Run all demonstration scenarios"""
        print("\n" + "="*80)
        print("COMPANY RESEARCH AGENT - DEMONSTRATION SCENARIOS")
        print("="*80)
        print("\nThis demo will showcase different user personas and how the agent handles them.")
        print("Press Ctrl+C to skip to the next scenario.\n")
        
        for scenario_name, scenario_func in self.scenarios.items():
            try:
                await scenario_func()
                print("\n" + "-"*60)
                input("Press Enter to continue to the next scenario...")
            except KeyboardInterrupt:
                print("\nSkipping to next scenario...")
                continue
            except Exception as e:
                print(f"\nError in scenario: {e}")
                continue
        
        print("\n" + "="*80)
        print("DEMONSTRATION COMPLETE")
        print("="*80)
    
    async def interactive_demo(self):
        """Interactive demo where user can choose scenarios"""
        while True:
            print("\n" + "="*60)
            print("INTERACTIVE DEMO MENU")
            print("="*60)
            print("\nChoose a demo scenario:")
            print("1. Confused User - Unsure what they want")
            print("2. Efficient User - Wants quick results")
            print("3. Chatty User - Goes off topic frequently")
            print("4. Edge Cases - Unusual requests")
            print("5. Run All Demos")
            print("6. Exit")
            
            choice = input("\nEnter your choice (1-6): ").strip()
            
            if choice == "1":
                await self.confused_user_scenario()
            elif choice == "2":
                await self.efficient_user_scenario()
            elif choice == "3":
                await self.chatty_user_scenario()
            elif choice == "4":
                await self.edge_case_scenario()
            elif choice == "5":
                await self.run_all_demos()
            elif choice == "6":
                print("\nExiting demo...")
                break
            else:
                print("Invalid choice. Please try again.")


class TestCases:
    """Automated test cases for the agent"""
    
    def __init__(self):
        self.test_results = []
    
    async def test_intent_detection(self):
        """Test intent detection accuracy"""
        print("\n" + "="*60)
        print("TESTING: Intent Detection")
        print("="*60)
        
        agent = CompanyResearchAgent()
        
        test_inputs = {
            "exit": ["goodbye", "quit", "exit", "bye"],
            "help": ["help", "what can you do", "how do you work"],
            "status_check": ["status", "progress", "how's it going"],
            "company_name": ["Microsoft", "research Apple", "tell me about Google"],
        }
        
        for expected_intent, inputs in test_inputs.items():
            for test_input in inputs:
                detected = agent._detect_intent(test_input)
                result = "✅" if detected == expected_intent else "❌"
                print(f"{result} Input: '{test_input}' -> Expected: {expected_intent}, Got: {detected}")
                self.test_results.append({
                    "test": "intent_detection",
                    "input": test_input,
                    "expected": expected_intent,
                    "actual": detected,
                    "passed": detected == expected_intent
                })
    
    async def test_company_name_extraction(self):
        """Test company name extraction"""
        print("\n" + "="*60)
        print("TESTING: Company Name Extraction")
        print("="*60)
        
        agent = CompanyResearchAgent()
        
        test_cases = [
            ("research Microsoft", "Microsoft"),
            ("tell me about Apple Inc", "Apple Inc"),
            ("Google", "Google"),
            ("I want information on Tesla Motors", "Tesla Motors"),
            ("look up amazon", "Amazon"),
            ("", None),
            ("research", None)
        ]
        
        for input_text, expected in test_cases:
            extracted = agent._extract_company_name(input_text)
            result = "✅" if extracted == expected else "❌"
            print(f"{result} Input: '{input_text}' -> Expected: {expected}, Got: {extracted}")
            self.test_results.append({
                "test": "company_extraction",
                "input": input_text,
                "expected": expected,
                "actual": extracted,
                "passed": extracted == expected
            })
    
    async def test_conversation_modes(self):
        """Test different conversation modes"""
        print("\n" + "="*60)
        print("TESTING: Conversation Modes")
        print("="*60)
        
        modes = [
            ConversationMode.EFFICIENT,
            ConversationMode.CHATTY,
            ConversationMode.CONFUSED,
            ConversationMode.NORMAL
        ]
        
        for mode in modes:
            agent = CompanyResearchAgent(mode)
            greeting = agent.get_response("greeting")
            print(f"\n{mode.value.upper()} Mode Greeting:")
            print(f"  {greeting[:100]}..." if len(greeting) > 100 else f"  {greeting}")
            
            self.test_results.append({
                "test": "conversation_mode",
                "mode": mode.value,
                "greeting_length": len(greeting),
                "has_greeting": len(greeting) > 0,
                "passed": len(greeting) > 0
            })
    
    async def test_state_management(self):
        """Test state transitions"""
        print("\n" + "="*60)
        print("TESTING: State Management")
        print("="*60)
        
        agent = CompanyResearchAgent()
        
        # Test state transitions
        states_sequence = [
            ("Initial state", agent.state.value, "idle"),
            ("After company request", None, "researching"),
            ("After completion", None, "complete")
        ]
        
        print(f"Initial State: {agent.state.value}")
        
        # Trigger state changes
        await agent.process_input("Microsoft")
        print(f"After company input: {agent.state.value}")
        
        passed = agent.state.value in ["researching", "complete", "idle"]
        result = "✅" if passed else "❌"
        print(f"{result} State management test")
        
        self.test_results.append({
            "test": "state_management",
            "final_state": agent.state.value,
            "passed": passed
        })
    
    async def run_all_tests(self):
        """Run all automated tests"""
        print("\n" + "="*80)
        print("AUTOMATED TEST SUITE")
        print("="*80)
        
        await self.test_intent_detection()
        await self.test_company_name_extraction()
        await self.test_conversation_modes()
        await self.test_state_management()
        
        # Summary
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for t in self.test_results if t.get("passed", False))
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {total_tests - passed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")


async def main():
    """Main entry point for demos and tests"""
    print("\n" + "="*80)
    print("COMPANY RESEARCH AGENT - DEMO & TEST SUITE")
    print("="*80)
    
    print("\nWhat would you like to do?")
    print("1. Run Interactive Demos")
    print("2. Run Automated Tests")
    print("3. Run Everything")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        demo = DemoScenarios()
        await demo.interactive_demo()
    elif choice == "2":
        tests = TestCases()
        await tests.run_all_tests()
    elif choice == "3":
        # Run tests first
        tests = TestCases()
        await tests.run_all_tests()
        
        input("\nPress Enter to continue to demos...")
        
        # Then run demos
        demo = DemoScenarios()
        await demo.run_all_demos()
    else:
        print("Invalid choice. Exiting...")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nProgram interrupted. Goodbye!")
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)

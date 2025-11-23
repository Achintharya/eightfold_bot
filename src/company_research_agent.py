"""
Company Research & Account Plan Agent
An interactive conversational agent for company research and account plan generation
"""

import asyncio
import json
import os
import re
from typing import Dict, List, Optional
from enum import Enum
from datetime import datetime
from dotenv import load_dotenv

# Import existing modules
from src.web_context_extract import extract
from src.context_summarizer import summarize_context
from src.article_writer import generate_chat_response

load_dotenv('config/.env')

class ConversationMode(Enum):
    """Different conversation modes for the agent"""
    EFFICIENT = "efficient"  # Quick, to-the-point responses
    CHATTY = "chatty"      # Friendly, verbose responses
    CONFUSED = "confused"   # Needs clarification often
    NORMAL = "normal"       # Balanced responses

class ResearchState(Enum):
    """States of the research process"""
    IDLE = "idle"
    GATHERING_INFO = "gathering_info"
    RESEARCHING = "researching"
    SUMMARIZING = "summarizing"
    GENERATING_PLAN = "generating_plan"
    EDITING = "editing"
    COMPLETE = "complete"

class CompanyResearchAgent:
    """Interactive agent for company research and account planning"""
    
    def __init__(self, user_mode: ConversationMode = ConversationMode.NORMAL):
        self.user_mode = user_mode  # Track user's conversation style
        self.state = ResearchState.IDLE
        self.conversation_history = []
        self.current_company = None
        self.research_data = {}
        self.account_plan = {}
        self.context_summary = ""
        self.research_cache = {}  # Cache for company research data
        self.plan_cache = {}  # Cache for generated plans
        
        # Agent always responds normally/professionally
        self.response_templates = {
            "greeting": "Hello! I'm here to help you research companies and create account plans. Which company would you like to research?",
            "clarify": "Could you provide more details about {info}?",
            "update": "Update: Currently {status}",
            "complete": "I've completed the account plan. Would you like to review it?",
            "help": """I can help you with:
        
        1. **Company Research**: Just tell me a company name and I'll gather comprehensive information
        2. **Account Plan Generation**: I'll create a detailed account plan based on my research
        3. **Plan Editing**: You can ask me to edit any section of the generated plan
        4. **Status Updates**: Ask me for progress updates during research
        
        **Example commands:**
        - "Research Microsoft"
        - "Tell me about Apple"
        - "What's your progress?"
        - "Edit the executive summary"
        
        Just talk to me naturally - I'll understand!"""
        }
        
    def get_response(self, template_key: str, **kwargs) -> str:
        """Get a professional response"""
        template = self.response_templates.get(template_key, "")
        if template:
            return template.format(**kwargs)
        return ""
    
    async def process_input(self, user_input: str) -> str:
        """Process user input and return appropriate response"""
        self.conversation_history.append({"role": "user", "content": user_input})
        
        # Detect intent from user input
        intent = self._detect_intent(user_input)
        
        # Route to appropriate handler
        if intent == "company_name":
            return await self._handle_company_research(user_input)
        elif intent == "edit_request":
            return await self._handle_edit_request(user_input)
        elif intent == "save_plan":
            return await self._handle_save_plan()
        elif intent == "clarification":
            return await self._handle_clarification(user_input)
        elif intent == "status_check":
            return self._get_status_update()
        elif intent == "help":
            return self._provide_help()
        elif intent == "exit":
            return "Thank you for using the Company Research Agent. Goodbye!"
        else:
            return await self._handle_general_conversation(user_input)
    
    def _detect_intent(self, user_input: str) -> str:
        """Detect the user's intent from their input"""
        input_lower = user_input.lower()
        
        # Check for exit commands
        if any(word in input_lower for word in ["exit", "quit", "bye", "goodbye"]):
            return "exit"
        
        # Check for help requests
        if any(word in input_lower for word in ["help", "what can you do", "how do you work"]):
            return "help"
        
        # Check for save requests
        if any(word in input_lower for word in ["save", "export", "store", "keep"]) and self.account_plan:
            return "save_plan"
        
        # Check for status inquiries
        if any(word in input_lower for word in ["status", "progress", "how's it going", "update"]):
            return "status_check"
        
        # Check for edit requests
        if any(word in input_lower for word in ["edit", "change", "modify", "update", "regenerate", "improve", "refine"]) and self.account_plan:
            return "edit_request"
        
        # Check if providing clarification
        if self.state == ResearchState.GATHERING_INFO:
            return "clarification"
        
        # Check for company name patterns
        company_patterns = [
            r"research\s+(\w+[\w\s]*)",
            r"look\s+(?:up|into)\s+(\w+[\w\s]*)",
            r"information\s+(?:on|about)\s+(\w+[\w\s]*)",
            r"tell\s+me\s+about\s+(\w+[\w\s]*)",
            r"^(\w+[\w\s]*)$"  # Just the company name
        ]
        
        for pattern in company_patterns:
            match = re.search(pattern, input_lower)
            if match:
                return "company_name"
        
        return "general"
    
    async def _handle_company_research(self, user_input: str) -> str:
        """Handle company research request with caching"""
        # Extract company name
        company_name = self._extract_company_name(user_input)
        
        if not company_name:
            self.state = ResearchState.GATHERING_INFO
            return self.get_response("clarify", info="the company name")
        
        self.current_company = company_name
        
        # Check if we have cached data for this company
        if company_name in self.research_cache:
            print(f"✅ Using cached research data for {company_name}")
            response = f"I have existing research data for {company_name}. "
            
            # Check if we also have a cached plan
            if company_name in self.plan_cache:
                self.account_plan = self.plan_cache[company_name]
                self.context_summary = self.research_cache[company_name]['summary']
                self.state = ResearchState.COMPLETE
                
                response += "Loading the existing account plan.\n\n"
                response += self.get_plan_summary()
                response += "\n\nYou can:\n"
                response += "- Ask me to edit any section of the plan\n"
                response += "- Request a full view of the plan\n"
                response += "- Ask for a fresh research update\n"
                
                return response
            else:
                # Use cached research to generate a new plan
                self.context_summary = self.research_cache[company_name]['summary']
                self.research_data[company_name] = self.research_cache[company_name]['data']
                self.state = ResearchState.GENERATING_PLAN
                response += "Generating a new account plan based on existing research...\n"
                response += "\n" + await self._generate_account_plan()
                return response
        
        # No cache - perform new research
        self.state = ResearchState.RESEARCHING
        response = f"Starting fresh research on {company_name}...\n"
        response += "I'll search for information about this company and gather data from multiple sources...\n"
        
        # Perform actual research
        try:
            await self._perform_research(company_name)
            response += "\n" + self.get_response("update", status="research complete")
            
            # Cache the research data
            self.research_cache[company_name] = {
                'data': self.research_data[company_name],
                'summary': self.context_summary,
                'timestamp': datetime.now().isoformat()
            }
            
            # Generate account plan
            response += "\n" + await self._generate_account_plan()
            
            # Cache the plan
            self.plan_cache[company_name] = self.account_plan
            
        except Exception as e:
            response += f"\nError during research: {str(e)}"
            self.state = ResearchState.IDLE
        
        return response
    
    async def _perform_research(self, company_name: str) -> None:
        """Perform the actual research using existing modules"""
        print(f"🔍 Researching {company_name}...")
        
        # Create search queries for different aspects
        queries = [
            f"{company_name} company overview products services",
            f"{company_name} leadership team executives",
            f"{company_name} recent news announcements",
            f"{company_name} challenges problems issues"
        ]
        
        all_data = []
        
        for query in queries:
            # Provide progress update
            aspect = query.split(company_name)[1].strip()
            print(f"📊 Researching: {aspect}...")
            
            # Check for conflicting information scenarios
            if "challenges" in aspect or "problems" in aspect:
                print("I'm finding some conflicting information about challenges. Let me dig deeper...")
            
            # Use the simplified extract function with silent mode
            await extract(query, silent_mode=True)
            
            # Read the extracted data
            try:
                with open("data/context.json", "r") as f:
                    data = json.load(f)
                    all_data.extend(data)
            except:
                pass
        
        # Save all research data
        self.research_data[company_name] = all_data
        
        # Summarize the context (silently)
        summarize_context(silent_mode=True)
        
        # Read the summary
        try:
            with open("data/context.txt", "r") as f:
                self.context_summary = f.read()
        except:
            self.context_summary = "No summary available"
    
    async def _generate_account_plan(self) -> str:
        """Generate an account plan based on research"""
        self.state = ResearchState.GENERATING_PLAN
        
        # Create account plan structure
        plan_sections = {
            "executive_summary": "",
            "company_overview": "",
            "key_stakeholders": "",
            "business_challenges": "",
            "opportunities": "",
            "proposed_solutions": "",
            "engagement_strategy": "",
            "success_metrics": "",
            "next_steps": ""
        }
        
        # Generate each section using the article writer's capability        
        for section, _ in plan_sections.items():
            section_query = f"Based on the research about {self.current_company}, write the {section.replace('_', ' ')} section for an account plan. Write in a professional business style with clear sections and actionable insights."
            
            try:
                section_content = generate_chat_response(
                    self.context_summary,
                    section_query,
                    silent_mode=True  # Suppress output for cleaner agent interaction
                )
                plan_sections[section] = section_content
            except Exception as e:
                plan_sections[section] = f"[Section generation failed: {str(e)}]"
        
        self.account_plan = plan_sections
        self.state = ResearchState.COMPLETE
        
        # Format the plan for display
        plan_output = f"\n{'='*60}\n"
        plan_output += f"ACCOUNT PLAN: {self.current_company.upper()}\n"
        plan_output += f"{'='*60}\n\n"
        
        for section, content in plan_sections.items():
            section_title = section.replace('_', ' ').title()
            plan_output += f"## {section_title}\n"
            plan_output += f"{content}\n\n"
        
        # Save the plan to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        plan_filename = f"account_plan_{self.current_company.replace(' ', '_')}_{timestamp}.md"
        
        os.makedirs("./account_plans", exist_ok=True)
        with open(f"./account_plans/{plan_filename}", "w") as f:
            f.write(plan_output)
        
        # Generate and return a summary
        summary = self.get_plan_summary()
        
        return f"Account plan generated and saved to {plan_filename}\n\n{summary}"
    
    async def _handle_edit_request(self, user_input: str) -> str:
        """Enhanced handler for editing account plan sections with partial edits and regeneration"""
        self.state = ResearchState.EDITING
        
        # Check if this is a follow-up edit with instructions
        if hasattr(self, '_pending_edit_section'):
            section_to_edit = self._pending_edit_section
            edit_instructions = user_input
            
            # Determine edit type
            if any(word in edit_instructions.lower() for word in ["regenerate", "rewrite", "redo", "create again"]):
                # Full regeneration with optional focus
                return await self._regenerate_section(section_to_edit, edit_instructions)
            elif any(word in edit_instructions.lower() for word in ["add", "include", "focus on", "emphasize", "expand"]):
                # Partial edit - enhance existing content
                return await self._enhance_section(section_to_edit, edit_instructions)
            else:
                # Full replacement with provided content
                self.account_plan[section_to_edit] = edit_instructions
                delattr(self, '_pending_edit_section')
                self.state = ResearchState.COMPLETE
                return f"✓ {section_to_edit.replace('_', ' ').title()} has been updated.\n\nWould you like to edit another section or save the plan?"
        
        # Identify which section to edit
        section_keywords = {
            "executive": "executive_summary",
            "overview": "company_overview",
            "stakeholder": "key_stakeholders",
            "challenge": "business_challenges",
            "opportunit": "opportunities",
            "solution": "proposed_solutions",
            "strategy": "engagement_strategy",
            "metric": "success_metrics",
            "next": "next_steps"
        }
        
        section_to_edit = None
        for keyword, section in section_keywords.items():
            if keyword in user_input.lower():
                section_to_edit = section
                break
        
        if not section_to_edit:
            return "Which section would you like to edit? Available sections:\n" + \
                   "\n".join([f"- {s.replace('_', ' ').title()}" for s in self.account_plan.keys()])
        
        # Store the section being edited for follow-up
        self._pending_edit_section = section_to_edit
        
        # Show current content and options
        current_content = self.account_plan[section_to_edit]
        return f"""Current {section_to_edit.replace('_', ' ').title()} content:
{'-' * 40}
{current_content}
{'-' * 40}

You can:
1. **Replace**: Provide new content to replace this section
2. **Regenerate**: Say "regenerate with focus on [specific aspect]" 
3. **Enhance**: Say "add [what to add]" or "expand on [topic]"

What changes would you like to make?"""
    
    async def _regenerate_section(self, section: str, instructions: str) -> str:
        """Regenerate a section based on user feedback"""
        # Extract focus areas from instructions
        focus_areas = ""
        if "focus on" in instructions.lower():
            focus_areas = instructions.lower().split("focus on")[1].strip()
        elif "emphasize" in instructions.lower():
            focus_areas = instructions.lower().split("emphasize")[1].strip()
        
        # Create enhanced query with user's focus
        section_query = f"""Based on the research about {self.current_company}, regenerate the {section.replace('_', ' ')} section for an account plan. 
        {f'Focus particularly on: {focus_areas}' if focus_areas else ''}
        Write in a professional business style with clear sections and actionable insights."""
        
        try:
            # Regenerate the section
            new_content = generate_chat_response(
                self.context_summary,
                section_query,
                silent_mode=True
            )
            
            # Update the plan
            self.account_plan[section] = new_content
            delattr(self, '_pending_edit_section')
            self.state = ResearchState.COMPLETE
            
            return f"""✓ {section.replace('_', ' ').title()} has been regenerated{f' with focus on {focus_areas}' if focus_areas else ''}.

New content:
{'-' * 40}
{new_content}
{'-' * 40}

Would you like to edit another section or save the plan?"""
            
        except Exception as e:
            return f"Error regenerating section: {str(e)}"
    
    async def _enhance_section(self, section: str, instructions: str) -> str:
        """Enhance existing section with additional content"""
        current_content = self.account_plan[section]
        
        # Create query for enhancement
        enhancement_query = f"""Current {section.replace('_', ' ')} content:
{current_content}

User request: {instructions}

Based on the research about {self.current_company}, enhance this section by {instructions}.
Keep the existing content and add the requested improvements. Write in a professional business style."""
        
        try:
            # Generate enhanced content
            enhanced_content = generate_chat_response(
                self.context_summary,
                enhancement_query,
                silent_mode=True
            )
            
            # Update the plan
            self.account_plan[section] = enhanced_content
            delattr(self, '_pending_edit_section')
            self.state = ResearchState.COMPLETE
            
            return f"""✓ {section.replace('_', ' ').title()} has been enhanced.

Updated content:
{'-' * 40}
{enhanced_content}
{'-' * 40}

Would you like to edit another section or save the plan?"""
            
        except Exception as e:
            return f"Error enhancing section: {str(e)}"
    
    async def _handle_save_plan(self) -> str:
        """Save the current account plan to the data folder"""
        if not self.account_plan or not self.current_company:
            return "No account plan to save. Please research a company first."
        
        # Format the complete plan
        plan_output = f"# ACCOUNT PLAN: {self.current_company.upper()}\n\n"
        plan_output += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        plan_output += "=" * 60 + "\n\n"
        
        for section, content in self.account_plan.items():
            section_title = section.replace('_', ' ').title()
            plan_output += f"## {section_title}\n\n"
            plan_output += f"{content}\n\n"
            plan_output += "-" * 40 + "\n\n"
        
        # Save to data folder
        os.makedirs("./data", exist_ok=True)
        
        # Create filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        data_filename = f"./data/{self.current_company.replace(' ', '_')}_account_plan_{timestamp}.md"
        
        # Also save a "latest" version for easy access
        latest_filename = f"./data/{self.current_company.replace(' ', '_')}_account_plan_latest.md"
        
        try:
            # Save timestamped version
            with open(data_filename, "w", encoding="utf-8") as f:
                f.write(plan_output)
            
            # Save latest version
            with open(latest_filename, "w", encoding="utf-8") as f:
                f.write(plan_output)
            
            # Also save the raw plan data as JSON
            json_filename = f"./data/{self.current_company.replace(' ', '_')}_account_plan_{timestamp}.json"
            plan_data = {
                "company": self.current_company,
                "generated": datetime.now().isoformat(),
                "sections": self.account_plan,
                "research_summary": self.context_summary
            }
            
            with open(json_filename, "w", encoding="utf-8") as f:
                json.dump(plan_data, f, indent=2, ensure_ascii=False)
            
            return f"""✓ Account plan successfully saved to data folder!

Files created:
- {data_filename} (timestamped version)
- {latest_filename} (latest version for easy access)  
- {json_filename} (structured data)

The plan has been preserved and can be accessed anytime from the data folder."""
            
        except Exception as e:
            return f"Error saving plan: {str(e)}"
    
    async def _handle_clarification(self, user_input: str) -> str:
        """Handle clarification from user"""
        # Process the clarification and continue with research
        self.current_company = user_input.strip()
        return await self._handle_company_research(user_input)
    
    def _get_status_update(self) -> str:
        """Provide status update on current research"""
        status_messages = {
            ResearchState.IDLE: "I'm ready to start researching. Just tell me which company!",
            ResearchState.GATHERING_INFO: "I'm waiting for more information from you.",
            ResearchState.RESEARCHING: f"I'm currently researching {self.current_company}...",
            ResearchState.SUMMARIZING: "I'm summarizing the research findings...",
            ResearchState.GENERATING_PLAN: "I'm generating the account plan...",
            ResearchState.EDITING: "We're editing the account plan.",
            ResearchState.COMPLETE: f"Research complete for {self.current_company}. Account plan is ready!"
        }
        
        return status_messages.get(self.state, "I'm not sure what I'm doing right now...")
    
    def _provide_help(self) -> str:
        """Provide help information"""
        return self.response_templates.get("help", "")
    
    async def _handle_general_conversation(self, user_input: str) -> str:
        """Handle general conversation - adapt slightly based on user mode"""
        import random
        
        # Always professional, but slightly adjust based on user's conversation style
        if self.user_mode == ConversationMode.EFFICIENT:
            # User wants efficiency, be brief
            return "Which company would you like to research?"
        elif self.user_mode == ConversationMode.CHATTY:
            # User is chatty, be slightly more conversational
            responses = [
                "That's interesting! Let's focus on company research. Which company would you like me to look into?",
                "I appreciate the conversation! Now, which company should we research?",
                "Thanks for sharing! Let's dive into some company research - which company interests you?"
            ]
            return random.choice(responses)
        elif self.user_mode == ConversationMode.CONFUSED:
            # User is confused, be more guiding
            return "I understand this might be confusing. Let me help - just tell me a company name you'd like to research, and I'll handle the rest."
        else:
            # Normal response
            responses = [
                "I'm designed for company research. Would you like me to research a company?",
                "Let's focus on company research. Which company interests you?",
                "I can help you research companies. Which one should we start with?"
            ]
            return random.choice(responses)
    
    def _extract_company_name(self, user_input: str) -> Optional[str]:
        """Extract company name from user input"""
        # Remove common phrases
        clean_input = user_input.lower()
        remove_phrases = [
            "research", "look up", "look into", "tell me about",
            "information on", "information about", "find", "search for",
            "i want to know about", "can you research", "please research"
        ]
        
        for phrase in remove_phrases:
            clean_input = clean_input.replace(phrase, "")
        
        # Clean up and capitalize
        company_name = clean_input.strip()
        if company_name:
            # Capitalize each word
            company_name = ' '.join(word.capitalize() for word in company_name.split())
            return company_name
        
        return None
    
    def get_plan_summary(self) -> str:
        """Generate a concise summary of the account plan"""
        if not self.account_plan:
            return "No account plan available yet."
        
        summary = f"**📋 Account Plan Summary for {self.current_company}**\n\n"
        
        # Extract key points from each section
        key_sections = {
            "executive_summary": "**Executive Summary:**",
            "business_challenges": "**Key Challenges:**",
            "opportunities": "**Main Opportunities:**",
            "proposed_solutions": "**Proposed Solutions:**",
            "next_steps": "**Next Steps:**"
        }
        
        for section_key, section_title in key_sections.items():
            if section_key in self.account_plan:
                content = self.account_plan[section_key]
                # Take first 200 characters or first 2 sentences
                sentences = content.split('. ')[:2]
                brief = '. '.join(sentences)
                if len(brief) > 200:
                    brief = brief[:197] + "..."
                summary += f"{section_title}\n{brief}\n\n"
        
        summary += "💡 *For the complete plan, click on the plan in the sidebar or ask me to show specific sections.*"
        
        return summary
    
    def clear_cache(self, company_name: str = None) -> str:
        """Clear cache for a specific company or all companies"""
        if company_name:
            if company_name in self.research_cache:
                del self.research_cache[company_name]
            if company_name in self.plan_cache:
                del self.plan_cache[company_name]
            return f"Cache cleared for {company_name}"
        else:
            self.research_cache.clear()
            self.plan_cache.clear()
            return "All cache cleared"


class InteractiveSession:
    """Manages the interactive conversation session"""
    
    def __init__(self):
        self.agent = None
        self.running = True
        
    def select_mode(self) -> ConversationMode:
        """Let user select their conversation style"""
        print("\n" + "="*60)
        print("COMPANY RESEARCH & ACCOUNT PLAN AGENT")
        print("="*60)
        print("\nSelect your conversation style (how you prefer to interact):")
        print("1. Efficient - You want quick, direct interactions")
        print("2. Chatty - You enjoy detailed conversations")
        print("3. Confused - You might need extra guidance")
        print("4. Normal - Standard interaction (default)")
        
        choice = input("\nEnter choice (1-4): ").strip()
        
        mode_map = {
            "1": ConversationMode.EFFICIENT,
            "2": ConversationMode.CHATTY,
            "3": ConversationMode.CONFUSED,
            "4": ConversationMode.NORMAL
        }
        
        return mode_map.get(choice, ConversationMode.NORMAL)
    
    async def run(self):
        """Run the interactive session"""
        # Select user's conversation style
        user_mode = self.select_mode()
        self.agent = CompanyResearchAgent(user_mode)
        
        # Display greeting (always professional)
        print("\n" + self.agent.response_templates["greeting"])
        print("\n(Type 'help' for assistance, 'exit' to quit)\n")
        
        # Main conversation loop
        while self.running:
            try:
                # Get user input
                user_input = input("\nYou: ").strip()
                
                if not user_input:
                    continue
                
                # Process input and get response
                response = await self.agent.process_input(user_input)
                
                # Display response
                print(f"\nAgent: {response}")
                
                # Check for exit
                if "goodbye" in response.lower():
                    self.running = False
                    
            except KeyboardInterrupt:
                print("\n\nSession interrupted. Goodbye!")
                self.running = False
            except Exception as e:
                print(f"\nError: {str(e)}")
                print("Let's continue...")


async def main():
    """Main entry point"""
    session = InteractiveSession()
    await session.run()


if __name__ == "__main__":
    # Run the interactive session
    asyncio.run(main())

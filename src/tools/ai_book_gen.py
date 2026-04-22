import os
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

try:
    from langchain_ollama import ChatOllama
    import langchain.agents 
    from langchain.tools import tool
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    from langchain_community.tools import DuckDuckGoSearchRun
except ImportError:
    print("Error: Required packages not installed.")
    print("Install with: pip install langchain langchain-ollama langchain-community duckduckgo-search")
    sys.exit(1)


class BookWriterAgent:
    def __init__(self, api_key: str, output_dir: str = "./book_output"):
        """Initialize the Book Writer Agent."""
        self.llm = ChatAnthropic(
            model="claude-sonnet-4-20250514",
            api_key=api_key,
            temperature=0.7
        )
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.book_state = {
            "title": "",
            "genre": "",
            "outline": [],
            "chapters": {},
            "metadata": {}
        }
        
    def save_chapter(self, chapter_num: int, title: str, content: str) -> str:
        """Save a chapter to disk."""
        filename = f"chapter_{chapter_num:02d}_{title.replace(' ', '_')}.txt"
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"Chapter {chapter_num}: {title}\n")
            f.write("=" * 80 + "\n\n")
            f.write(content)
        
        self.book_state["chapters"][chapter_num] = {
            "title": title,
            "filepath": str(filepath),
            "word_count": len(content.split())
        }
        
        return f"Chapter {chapter_num} saved to {filename} ({len(content.split())} words)"
    
    def save_outline(self, outline: str) -> str:
        """Save the book outline."""
        filepath = self.output_dir / "outline.txt"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("BOOK OUTLINE\n")
            f.write("=" * 80 + "\n\n")
            f.write(outline)
        
        return f"Outline saved to outline.txt"
    
    def get_book_progress(self) -> str:
        """Get current progress on the book."""
        total_words = sum(ch.get("word_count", 0) for ch in self.book_state["chapters"].values())
        num_chapters = len(self.book_state["chapters"])
        
        progress = f"Book Progress:\n"
        progress += f"Title: {self.book_state.get('title', 'Not set')}\n"
        progress += f"Genre: {self.book_state.get('genre', 'Not set')}\n"
        progress += f"Chapters completed: {num_chapters}\n"
        progress += f"Total words: {total_words:,}\n\n"
        
        if self.book_state["chapters"]:
            progress += "Completed chapters:\n"
            for num in sorted(self.book_state["chapters"].keys()):
                ch = self.book_state["chapters"][num]
                progress += f"  - Chapter {num}: {ch['title']} ({ch['word_count']} words)\n"
        
        return progress
    
    def research_topic(self, query: str) -> str:
        """Research a topic using web search."""
        try:
            search = DuckDuckGoSearchRun()
            results = search.run(query)
            return f"Research results for '{query}':\n{results}"
        except Exception as e:
            return f"Research failed: {str(e)}"
    
    def compile_book(self) -> str:
        """Compile all chapters into a single manuscript."""
        if not self.book_state["chapters"]:
            return "No chapters to compile yet."
        
        manuscript_path = self.output_dir / "full_manuscript.txt"
        
        with open(manuscript_path, 'w', encoding='utf-8') as f:
            # Title page
            f.write(f"{self.book_state.get('title', 'Untitled')}\n")
            f.write("=" * 80 + "\n")
            f.write(f"Genre: {self.book_state.get('genre', 'Unknown')}\n")
            f.write(f"Completed: {datetime.now().strftime('%Y-%m-%d')}\n")
            f.write(f"Total Chapters: {len(self.book_state['chapters'])}\n")
            total_words = sum(ch.get("word_count", 0) for ch in self.book_state["chapters"].values())
            f.write(f"Total Words: {total_words:,}\n\n")
            f.write("=" * 80 + "\n\n\n")
            
            # All chapters
            for chapter_num in sorted(self.book_state["chapters"].keys()):
                chapter_info = self.book_state["chapters"][chapter_num]
                chapter_path = Path(chapter_info["filepath"])
                
                if chapter_path.exists():
                    with open(chapter_path, 'r', encoding='utf-8') as ch_file:
                        f.write(ch_file.read())
                        f.write("\n\n\n")
        
        return f"Full manuscript compiled to {manuscript_path}"
    
    def create_agent(self) -> AgentExecutor:
        """Create the LangChain agent with tools."""
        
        tools = [
            Tool(
                name="save_chapter",
                func=lambda x: self.save_chapter(
                    int(x.split("|")[0]),
                    x.split("|")[1],
                    x.split("|", 2)[2]
                ),
                description="Save a chapter. Input format: 'chapter_number|chapter_title|chapter_content'. Example: '1|The Beginning|Once upon a time...'"
            ),
            Tool(
                name="save_outline",
                func=self.save_outline,
                description="Save the book outline. Input should be the full outline text."
            ),
            Tool(
                name="get_progress",
                func=lambda x: self.get_book_progress(),
                description="Get current progress on the book including chapters completed and word count."
            ),
            Tool(
                name="research",
                func=self.research_topic,
                description="Research a topic or gather information for writing. Input should be a search query."
            ),
            Tool(
                name="compile_book",
                func=lambda x: self.compile_book(),
                description="Compile all chapters into a single manuscript file."
            )
        ]
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert book writing assistant. You help authors plan, research, and write books chapter by chapter.

Your capabilities:
- Create detailed book outlines with chapter breakdowns
- Research topics to ensure accuracy and depth
- Write engaging chapters with proper pacing and structure
- Track progress and manage the writing workflow
- Compile chapters into a complete manuscript

When writing:
- Develop compelling characters and plots
- Use vivid descriptions and engaging dialogue
- Maintain consistent tone and style
- Aim for 2000-3000 words per chapter (adjust based on genre)
- Follow standard manuscript formatting

Always save your work using the provided tools."""),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        agent = create_tool_calling_agent(self.llm, tools, prompt)
        return AgentExecutor(agent=agent, tools=tools, verbose=True)
    
    def write_book(self, book_description: str):
        """Main method to coordinate book writing."""
        agent = self.create_agent()
        
        print("\n" + "="*80)
        print("AI BOOK WRITER AGENT")
        print("="*80 + "\n")
        
        # Parse book description to set state
        if "title:" in book_description.lower():
            parts = book_description.split("title:", 1)[1].split("\n")[0].strip()
            self.book_state["title"] = parts
        
        if "genre:" in book_description.lower():
            parts = book_description.split("genre:", 1)[1].split("\n")[0].strip()
            self.book_state["genre"] = parts
        
        print(f"Starting book writing process...")
        print(f"Title: {self.book_state.get('title', 'To be determined')}")
        print(f"Genre: {self.book_state.get('genre', 'To be determined')}")
        print(f"Output directory: {self.output_dir}\n")
        
        # Step 1: Create outline
        print("\n📋 STEP 1: Creating book outline...")
        outline_prompt = f"""Based on this book description, create a detailed outline:

{book_description}

Create an outline with:
1. Book title and genre
2. 8-12 chapter breakdown with titles and brief descriptions
3. Main characters and their arcs
4. Key plot points and themes

Save the outline using the save_outline tool."""
        
        try:
            agent.invoke({"input": outline_prompt})
        except Exception as e:
            print(f"Error creating outline: {e}")
            return
        
        # Step 2: Research if needed
        print("\n🔍 STEP 2: Conducting research (if needed)...")
        research_prompt = f"""Review the book concept: {book_description}

If this book requires research (historical facts, technical details, etc.), use the research tool to gather information. Otherwise, proceed to writing."""
        
        try:
            agent.invoke({"input": research_prompt})
        except Exception as e:
            print(f"Research phase note: {e}")
        
        # Step 3: Write chapters
        print("\n✍️  STEP 3: Writing chapters...")
        
        num_chapters = int(input("\nHow many chapters would you like to write? (1-12): ").strip() or "3")
        num_chapters = max(1, min(12, num_chapters))
        
        for i in range(1, num_chapters + 1):
            print(f"\n📖 Writing Chapter {i}...")
            chapter_prompt = f"""Write Chapter {i} of the book.

Book context: {book_description}

Requirements:
- Write 2000-3000 words
- Include engaging narrative and dialogue
- Advance the plot meaningfully
- Maintain consistent tone and style
- End with a hook for the next chapter

Save the chapter using: save_chapter tool with format: {i}|Chapter Title|chapter content"""
            
            try:
                agent.invoke({"input": chapter_prompt})
                print(f"✅ Chapter {i} completed!")
            except Exception as e:
                print(f"Error writing chapter {i}: {e}")
        
        # Step 4: Compile manuscript
        print("\n📚 STEP 4: Compiling final manuscript...")
        try:
            result = agent.invoke({"input": "Compile all chapters into the final manuscript using the compile_book tool."})
            print("\n✅ Book writing complete!")
            print(f"📁 All files saved to: {self.output_dir}")
        except Exception as e:
            print(f"Error compiling manuscript: {e}")


def main():
    """Main entry point."""
    print("=" * 80)
    print("AI BOOK WRITER - LangChain Agent")
    print("=" * 80)
    
    # Get API key
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("\n❌ Error: ANTHROPIC_API_KEY environment variable not set")
        print("Set it with: export ANTHROPIC_API_KEY='your-api-key'")
        sys.exit(1)
    
    # Get book details
    print("\nLet's create a book! Please provide the following information:\n")
    
    title = input("Book Title: ").strip()
    genre = input("Genre (e.g., Fantasy, Mystery, Sci-Fi, Romance): ").strip()
    premise = input("Brief premise or plot summary: ").strip()
    
    book_description = f"""Title: {title}
Genre: {genre}
Premise: {premise}"""
    
    # Initialize agent and start writing
    writer = BookWriterAgent(api_key)
    writer.write_book(book_description)


if __name__ == "__main__":
    main()
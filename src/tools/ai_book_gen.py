import os
import sys
import json
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

class BookWriterAgent:
    def __init__(self, api_key: str = "none", output_dir: str = "./book_output"):
        """Initialize the Book Writer Agent."""
        self.model = "granite3.2:8b"
        self.base_url = "http://localhost:1337/v1"
        self.api_key = api_key
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.book_state = {
            "title": "",
            "genre": "",
            "outline": [],
            "chapters": {},
            "metadata": {}
        }

    def call_llm(self, system_prompt: str, user_prompt: str) -> str:
        """Call the local LLM API."""
        payload = json.dumps({
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.7
        }).encode('utf-8')
        
        try:
            url = f"{self.base_url}/chat/completions"
            req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
            
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
            return result['choices'][0]['message']['content']
        except Exception as e:
            print(f"Error calling LLM: {e}")
            return ""
        
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
        """Research a topic (simplified version)."""
        return f"Research results for '{query}': (Research tool simplified due to dependency removal)"

    def write_book(self, book_description: str):
        """Main method to coordinate book writing."""
        
        print("\n" + "="*80)
        print("AI BOOK WRITER")
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
        
        system_prompt = "You are an expert book writing assistant. You help authors plan, research, and write books chapter by chapter."

        # Step 1: Create outline
        print("\n📋 STEP 1: Creating book outline...")
        outline_prompt = f"""Based on this book description, create a detailed outline:

{book_description}

Create an outline with:
1. Book title and genre
2. 8-12 chapter breakdown with titles and brief descriptions
3. Main characters and their arcs
4. Key plot points and themes"""
        
        outline_content = self.call_llm(system_prompt, outline_prompt)
        if outline_content:
            print(self.save_outline(outline_content))
        
        # Step 3: Write chapters
        print("\n✍️  STEP 3: Writing chapters...")
        
        num_chapters_input = input("\nHow many chapters would you like to write? (1-12): ").strip() or "3"
        try:
            num_chapters = int(num_chapters_input)
        except ValueError:
            num_chapters = 3
        num_chapters = max(1, min(12, num_chapters))
        
        for i in range(1, num_chapters + 1):
            print(f"\n📖 Writing Chapter {i}...")
            chapter_prompt = f"""Write Chapter {i} of the book.

Book context: {book_description}
Outline: {outline_content[:1000] if outline_content else 'No outline'}...

Requirements:
- Write a substantial chapter
- Include engaging narrative and dialogue
- Advance the plot meaningfully
- Maintain consistent tone and style
- End with a hook for the next chapter

Respond with the chapter title on the first line, then the chapter content."""
            
            chapter_response = self.call_llm(system_prompt, chapter_prompt)
            if chapter_response:
                lines = chapter_response.strip().split('\n')
                chapter_title = lines[0].strip()
                chapter_content = '\n'.join(lines[1:]).strip()
                print(self.save_chapter(i, chapter_title, chapter_content))
                print(f"✅ Chapter {i} completed!")
        
        # Step 4: Compile manuscript
        print("\n📚 STEP 4: Compiling final manuscript...")
        print(self.compile_book())
        print("\n✅ Book writing complete!")
        print(f"📁 All files saved to: {self.output_dir}")


def main():
    """Main entry point."""
    print("=" * 80)
    print("AI BOOK WRITER")
    print("=" * 80)
    
    # Get API key (not strictly required for local LLM but kept for structure)
    api_key = os.getenv('OPENAI_API_KEY') or "local-key"
    
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
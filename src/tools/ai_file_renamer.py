import os
import sys
import base64
import json
from pathlib import Path
from typing import Optional
from ollama import chat

class AIFileRenamer:
    def __init__(self):
        """Initialize the AI File Renamer with Anthropic API key."""
        self.model= "gemma3:4b"
        
    def read_file_content(self, file_path: Path) -> tuple[Optional[str], Optional[str]]:
        """
        Read file content and return base64 encoding for images/PDFs or text content.
        Returns: (content_type, content_data)
        """
        suffix = file_path.suffix.lower()
        
        # Handle images
        if suffix in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
            with open(file_path, 'rb') as f:
                image_data = base64.standard_b64encode(f.read()).decode('utf-8')
            media_type = 'image/jpeg' if suffix in ['.jpg', '.jpeg'] else f'image/{suffix[1:]}'
            return 'image', json.dumps({'media_type': media_type, 'data': image_data})
        
        # Handle PDFs
        elif suffix == '.pdf':
            with open(file_path, 'rb') as f:
                pdf_data = base64.standard_b64encode(f.read()).decode('utf-8')
            return 'pdf', pdf_data
        
        # Handle text files
        elif suffix in ['.txt', '.md', '.py', '.js', '.html', '.css', '.json', '.xml', '.csv']:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read(10000)  # Read first 10KB
                return 'text', content
            except UnicodeDecodeError:
                return None, None
        
        return None, None
    
    def generate_filename(self, file_path: Path, dry_run: bool = False) -> Optional[str]:
        """
        Use Claude API to generate a descriptive filename based on file content.
        """
        content_type, content_data = self.read_file_content(file_path)
        
        if not content_type:
            print(f"⚠️  Skipping {file_path.name} - unsupported file type")
            return None
        
        # Build the message content
        message_content = []
        
        if content_type == 'image':
            img_data = json.loads(content_data)
            message_content.append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": img_data['media_type'],
                    "data": img_data['data']
                }
            })
            message_content.append({
                "type": "text",
                "text": "Analyze this image and suggest a descriptive filename (without extension). The filename should be concise (2-5 words), use hyphens between words, and describe what's in the image. Respond with ONLY the filename, no explanation."
            })
        
        elif content_type == 'pdf':
            message_content.append({
                "type": "document",
                "source": {
                    "type": "base64",
                    "media_type": "application/pdf",
                    "data": content_data
                }
            })
            message_content.append({
                "type": "text",
                "text": "Analyze this PDF and suggest a descriptive filename (without extension). The filename should be concise (2-5 words), use hyphens between words, and describe the document's content. Respond with ONLY the filename, no explanation."
            })
        
        elif content_type == 'text':
            message_content.append({
                "type": "text",
                "text": f"Analyze this file content and suggest a descriptive filename (without extension). The filename should be concise (2-5 words), use hyphens between words, and describe what the file is about. Respond with ONLY the filename, no explanation.\n\nFile content:\n{content_data}"
            })
        
        try:
            # Call Claude API
            if content_type == 'image':
                prompt = f"Suggest a descriptive filename (without extension) for an image named '{file_path.name}'. Use 2-5 words, underscore, lowercase. Respond with ONLY the filename in format (<descriptor> <tag> <label> <YYYYMMDD>). "
            elif content_type == 'pdf':
                prompt = f"Suggest a descriptive filename (without extension) for a PDF named '{file_path.name}'. Use 2-5 words, underscore, lowercase. Respond with ONLY the filename in format (<descriptor> <tag> <label> <YYYYMMDD>)."
            elif content_type == 'text':
                prompt = f"Analyze this file content and suggest a descriptive filename (without extension). Use 2-5 words, underscore, lowercase. Respond with ONLY the filename in format (<descriptor> <tag> <label> <YYYYMMDD>).\n\nFile content:\n{content_data}"
            else:
                return None


            response = chat(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )           

            
            # Extract suggested filename
            suggested_name = response.message.content
            
            # Clean the filename
            suggested_name = suggested_name.replace(' ', '-')
            suggested_name = ''.join(c for c in suggested_name if c.isalnum() or c in '-_')
            suggested_name = suggested_name.lower()
            
            # Add original extension
            new_filename = f"{suggested_name}{file_path.suffix}"
            
            if dry_run:
                print(f"📝 {file_path.name} → {new_filename}")
            else:
                new_path = file_path.parent / new_filename
                
                # Handle name conflicts
                counter = 1
                while new_path.exists():
                    new_filename = f"{suggested_name}-{counter}{file_path.suffix}"
                    new_path = file_path.parent / new_filename
                    counter += 1
                
                file_path.rename(new_path)
                print(f"✅ Renamed: {file_path.name} → {new_filename}")
            
            return new_filename
            
        except Exception as e:
            print(f"❌ Error processing {file_path.name}: {str(e)}")
            return None
    
    def rename_directory(self, directory: str, dry_run: bool = False):
        """Rename all supported files in a directory."""
        dir_path = Path(directory)
        
        if not dir_path.exists() or not dir_path.is_dir():
            print(f"Error: {directory} is not a valid directory")
            return
        
        files = [f for f in dir_path.iterdir() if f.is_file()]
        
        if not files:
            print("No files found in directory")
            return
        
        print(f"\n{'DRY RUN - ' if dry_run else ''}Processing {len(files)} files in {directory}\n")
        
        for file_path in files:
            self.generate_filename(file_path, dry_run=dry_run)


def main():
    """Main entry point for the AI File Renamer."""
    if len(sys.argv) < 2:
        print("Usage: python ai_file_renamer.py <directory> [--dry-run]")
        print("\nOptions:")
        print("  --dry-run    Show what would be renamed without actually renaming")
        sys.exit(1)
    
    directory = sys.argv[1]
    dry_run = '--dry-run' in sys.argv
    

    
    renamer = AIFileRenamer()
    renamer.rename_directory(directory, dry_run=dry_run)


if __name__ == "__main__":
    main()
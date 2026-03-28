#!/usr/bin/env python3
"""
Autoresearch Story Refinement Launcher
Fully local with LM Studio + Aider + Auto Commit
"""

import os
import subprocess
import sys
import time

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    clear_screen()
    print("=" * 85)
    print("          EXTENDED AUTORESEARCH - STORY REFINEMENT")
    print("       Fully Local • LM Studio + Aider • Karpathy Style Keep/Revert")
    print("=" * 85)
    print()

def get_user_choices():
    print("Available Writer Styles:")
    print("  1. Lee Child")
    print("  2. Stephen King")
    print("  3. J.R.R. Tolkien")
    print("  4. Arthur Conan Doyle")
    print("  5. Agatha Christie")
    print("  6. Neutral Thriller")
    
    writer_choice = input("\nChoose writer style (1-6): ").strip()
    
    print("\nAvailable Reviewer Styles:")
    print("  1. Harsh Editor")
    print("  2. Analytical Critic")
    print("  3. Mythic/Literary Reviewer")
    print("  4. Commercial Thriller Reviewer")
    print("  5. General Quality Reviewer")
    
    reviewer_choice = input("Choose reviewer style (1-5): ").strip()

    writers = {"1": "Lee Child", "2": "Stephen King", "3": "J.R.R. Tolkien",
               "4": "Arthur Conan Doyle", "5": "Agatha Christie", "6": "Neutral Thriller"}
    reviewers = {"1": "Harsh Editor", "2": "Analytical Critic", "3": "Mythic/Literary Reviewer",
                 "4": "Commercial Thriller Reviewer", "5": "General Quality Reviewer"}

    writer_name = writers.get(writer_choice, "Neutral Thriller")
    reviewer_name = reviewers.get(reviewer_choice, "General Quality Reviewer")

    print(f"\nSelected → Writer: {writer_name} | Reviewer: {reviewer_name}")
    return writer_name, reviewer_name

def main():
    print_header()

    print("Make sure LM Studio server is running on http://localhost:1234/v1")
    input("\nPress Enter when ready...")

    writer, reviewer = get_user_choices()

    print(f"\nStarting autonomous autoresearch loop...")
    print(f"Writer: {writer} | Reviewer: {reviewer}")
    print("Good edits will be automatically committed. Bad edits will be reverted.\n")

    confirm = input("Type 'yes' to start: ").strip().lower()
    if confirm != "yes":
        print("Cancelled.")
        return

    system_message = f"""You are running in extended autonomous autoresearch mode.

Writer Style: {writer}
Reviewer Style: {reviewer}

Follow program.md strictly.
- Deliberate deeply before every edit.
- Always keep the entire story in context.
- Mimic the chosen writer style when editing.
- After edit, run `python score_story.py` and parse CHILL_FACTOR.
- If chill factor improves by 0.5 or more AND reviewer approves → commit with a short message.
- Otherwise revert the change.
- Be rigorous and patient."""

    try:
        cmd = [
            "aider",
            "story.md", "program.md", "score_story.py",
            "voice.md", "canon.md", "outline.md",
            "writers.md", "reviewers.md",
            "--model", "openai/qwen3.5-9b-null-space-abliterated-i1",
            "--openai-api-base", "http://localhost:1234/v1",
            "--openai-api-key", "lm-studio",
            "--auto-commits",                    # Enable auto commit (real autoresearch feel)
            "--commit-prompt", "Improved chill factor using {writer} style",   # Simple prompt to avoid hanging
            "--message", system_message
        ]

        print("\n🚀 Launching Aider autonomous loop...\n")
        subprocess.run(cmd, check=True)

    except FileNotFoundError:
        print("\nError: aider not found. Run: pip install --upgrade aider-chat")
    except KeyboardInterrupt:
        print("\n\nStopped by user.")
    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    main()
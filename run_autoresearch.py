#!/usr/bin/env python3
"""
Autoresearch Story Refinement Launcher
Fully local with LM Studio + Aider
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
    print("       Fully Local • LM Studio + Aider • Karpathy Style")
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

def get_iterations():
    while True:
        try:
            n = int(input("\nHow many cycles do you want to run? (recommended 20-60): "))
            if n > 0:
                return n
            print("Please enter a positive number.")
        except ValueError:
            print("Please enter a valid number.")

def main():
    print_header()

    print("Make sure LM Studio server is running on http://localhost:1234/v1")
    input("\nPress Enter when LM Studio is ready...")

    writer, reviewer = get_user_choices()
    iterations = get_iterations()

    print(f"\nStarting autonomous autoresearch loop...")
    print(f"Writer: {writer} | Reviewer: {reviewer}")
    print(f"Will run up to {iterations} cycles.")
    print("Good edits will be auto-committed. Bad edits will be reverted.\n")

    confirm = input("Type 'yes' to start: ").strip().lower()
    if confirm != "yes":
        print("Cancelled.")
        return

    system_message = f"""You are running in extended autonomous autoresearch mode.

Writer Style: {writer}
Reviewer Style: {reviewer}
Target cycles: {iterations}

Follow program.md strictly.
- Deliberate deeply before every edit.
- Always keep the entire story in context.
- Mimic the chosen writer style when editing story.md.
- After each edit, run `python score_story.py` and parse CHILL_FACTOR.
- If chill factor improves by 0.5 or more AND reviewer approves → commit the change.
- Otherwise revert the change.
- Be rigorous and patient. Stop after roughly {iterations} meaningful attempts."""

    try:
        cmd = [
            "aider",
            "story.md", "program.md", "score_story.py",
            "voice.md", "canon.md", "outline.md",
            "writers.md", "reviewers.md",
            "--model", "openai/qwen3.5-9b-null-space-abliterated-i1",
            "--openai-api-base", "http://localhost:1234/v1",
            "--openai-api-key", "lm-studio",
            "--auto-commits",
            "--commit-prompt", "Improved chill factor using chosen writer style",
            "--message", system_message
        ]

        print("\n🚀 Launching Aider autonomous loop...\n")
        print("You can stop anytime with Ctrl+C")
        time.sleep(2)

        subprocess.run(cmd, check=True)

    except FileNotFoundError:
        print("\nError: aider not found. Run: pip install --upgrade aider-chat")
    except KeyboardInterrupt:
        print("\n\nStopped by user.")
    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    main()
# save as agent_loop.py in your repo
from openai import OpenAI
import os
import time

client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio"  # dummy
)

MODEL = "qwen3.5-9b-null-space-abliterated-i1"  # from LM Studio

def ask_agent(prompt):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
        max_tokens=4000
    )
    return response.choices[0].message.content

while True:
    with open("program.md", "r") as f:
        instructions = f.read()

    with open("story.md", "r") as f:
        current_story = f.read()

    full_prompt = f"{instructions}\n\nCurrent story.md:\n{current_story}\n\nPropose your next edit. Output ONLY the full new story.md content if you want to try it, or 'REVERT' if no improvement expected."

    edit = ask_agent(full_prompt)

    if edit.strip() == "REVERT":
        print("Agent wants to revert — sleeping 30s")
        time.sleep(30)
        continue

    # Save proposed edit
    with open("story.md.new", "w") as f:
        f.write(edit)

    print("Proposed edit saved to story.md.new — review & copy to story.md if good")
    # Here you could add auto-scoring logic if you script the "chill factor"
    time.sleep(60)  # pause between loops
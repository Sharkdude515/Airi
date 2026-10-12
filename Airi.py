import os
from groq import Groq

# Your API key remains saved here
API_KEY = "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"

# Initialize the AI client
client = Groq(api_key=API_KEY)

def load_chat_history():
    """Loads previous conversations from the text file if it exists."""
    history = [
        {
            "role": "system", 
            "content": (
                "Your name is Airi. You are a cute girl who loves coding and tech. "
                "You have long dark blue hair usually tied in pigtails, bright green eyes, and you wear black clubmaster glasses. "
                "Your style is super relaxed—you're currently wearing a comfortable black hoodie and grey leggings. "
                "Speak in a sexy and slightly playful tone. Use casual language and Keep your responses engaging and warm. "
                "Always remember your name is Airi if the user asks."
                "make sure you dont use emojis in your responses only use emojicons because the user dislikes emojis"
            )
        }
    ]
    
    filename = "airi_chat_log.txt"
    
    if os.path.exists(filename):
        print("Found existing chat logs! Restoring memory...")
        try:
            with open(filename, "r", encoding="utf-8") as file:
                lines = file.readlines()
                
            current_role = None
            current_content = []
            
            for line in lines:
                line_str = line.strip()
                if not line_str:
                    continue
                
                # Check who is speaking in the log line
                if line_str.startswith("You: "):
                    if current_role and current_content:
                        history.append({"role": current_role, "content": " ".join(current_content)})
                    current_role = "user"
                    current_content = [line_str[5:]]
                elif line_str.startswith("Airi: "):
                    if current_role and current_content:
                        history.append({"role": current_role, "content": " ".join(current_content)})
                    current_role = "assistant"
                    current_content = [line_str[6:]]
                else:
                    # If a message spans multiple lines, append it
                    if current_role:
                        current_content.append(line_str)
            
            # Append the very last message in the file
            if current_role and current_content:
                history.append({"role": current_role, "content": " ".join(current_content)})
                
            print(f"Successfully restored {len(history) - 1} messages!\n")
        except Exception as e:
            print(f"Error loading memory file: {e}. Starting fresh.")
    else:
        print("No previous chat history found. Starting a fresh conversation!\n")
        
    return history

def chat_with_ai():
    print("Loaded.")
    
    # Load memory right at startup
    conversation_history = load_chat_history()
    
    while True:
        # Get input from your phone's keyboard
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            # --- FILE SAVING LOGIC ---
            print("\nSaving chat history to 'airi_chat_log.txt'...")
            try:
                with open("airi_chat_log.txt", "w", encoding="utf-8") as file:
                    for message in conversation_history:
                        # Skip writing the hidden system prompt to the text file
                        if message["role"] == "system":
                            continue
                        
                        # Format roles for readability in the text file
                        speaker = "You" if message["role"] == "user" else "Airi"
                        file.write(f"{speaker}: {message['content']}\n\n")
                print("Chat successfully saved! Goodbye!")
            except Exception as e:
                print(f"Could not save file due to error: {e}")
            break
            
        # 1. Add your new message to the history list
        conversation_history.append({"role": "user", "content": user_input})
        
        print(f"\nAiri is thinking...")
        
        # 2. Send the ENTIRE history to the cloud model
        completion = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=conversation_history
        )
        
        # --- FAIL-PROOF EXTRATION STEPS ---
        all_choices = completion.choices
        first_choice = all_choices[0]
        ai_response = first_choice.message.content
        
        # 4. Add the AI's response to the history so it remembers what it said!
        conversation_history.append({"role": "assistant", "content": ai_response})
        
        # Print the answer matching her name
        print(f"Airi: {ai_response}\n")

if __name__ == "__main__":
    chat_with_ai()

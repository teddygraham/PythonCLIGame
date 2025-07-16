#!/usr/bin/env python3
"""
PyAdventure: A CLI adventure game for learning Python
Main game engine and interface
"""

import sys
import os
from typing import Dict, Any
from story import StoryManager
from player import Player
from challenges import ChallengeValidator


class PyAdventureGame:
    def __init__(self):
        self.player = Player()
        self.story_manager = StoryManager()
        self.challenge_validator = ChallengeValidator()
        self.running = True
        
    def start(self):
        """Start the game"""
        self.print_banner()
        self.story_manager.load_story("intro")
        
        while self.running:
            try:
                self.game_loop()
            except KeyboardInterrupt:
                self.quit_game()
            except Exception as e:
                print(f"\nUnexpected error: {e}")
                self.quit_game()
    
    def game_loop(self):
        """Main game loop"""
        current_scene = self.story_manager.get_current_scene()
        
        if not current_scene:
            print("Game completed! Thanks for playing PyAdventure!")
            self.running = False
            return
            
        self.display_scene(current_scene)
        
        if current_scene.get("type") == "challenge":
            self.handle_challenge(current_scene)
        else:
            self.handle_choice(current_scene)
    
    def display_scene(self, scene: Dict[str, Any]):
        """Display the current scene"""
        print("\n" + "="*50)
        print(scene.get("title", "Unknown Scene"))
        print("="*50)
        print(scene.get("description", ""))
        
        if scene.get("code_example"):
            print(f"\nCode Example:\n{scene['code_example']}")
    
    def handle_challenge(self, scene: Dict[str, Any]):
        """Handle Python coding challenges"""
        challenge = scene.get("challenge", {})
        print(f"\nChallenge: {challenge.get('prompt', 'No prompt provided')}")
        
        if challenge.get("hint"):
            print(f"Hint: {challenge['hint']}")
        
        while True:
            print("\nEnter your Python code (type 'quit' to exit, 'hint' for help):")
            user_input = input("> ")
            
            if user_input.lower() == 'quit':
                self.quit_game()
                return
            elif user_input.lower() == 'hint':
                print(f"Hint: {challenge.get('hint', 'No hint available')}")
                continue
            
            result = self.challenge_validator.validate_code(
                user_input, 
                challenge.get("expected_output"),
                challenge.get("test_cases", [])
            )
            
            if result["success"]:
                print("✅ Correct! Well done!")
                self.player.add_experience(10)
                self.story_manager.advance_to_next_scene()
                break
            else:
                print(f"❌ {result['message']}")
                if result.get("output"):
                    print(f"Your output: {result['output']}")
    
    def handle_choice(self, scene: Dict[str, Any]):
        """Handle story choices"""
        choices = scene.get("choices", [])
        
        if not choices:
            input("\nPress Enter to continue...")
            self.story_manager.advance_to_next_scene()
            return
        
        print("\nWhat do you choose?")
        for i, choice in enumerate(choices, 1):
            print(f"{i}. {choice['text']}")
        
        while True:
            try:
                choice_input = input("\nEnter your choice (number): ")
                choice_num = int(choice_input) - 1
                
                if 0 <= choice_num < len(choices):
                    selected_choice = choices[choice_num]
                    self.story_manager.advance_to_scene(selected_choice.get("next_scene"))
                    break
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a valid number.")
    
    def print_banner(self):
        """Print game banner"""
        banner = """
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║  ██████╗ ██╗   ██╗ █████╗ ██████╗ ██╗   ██╗███████╗███╗   ██╗████████╗██╗   ██╗██████╗ ███████╗ ║
║  ██╔══██╗╚██╗ ██╔╝██╔══██╗██╔══██╗██║   ██║██╔════╝████╗  ██║╚══██╔══╝██║   ██║██╔══██╗██╔════╝ ║
║  ██████╔╝ ╚████╔╝ ███████║██║  ██║██║   ██║█████╗  ██╔██╗ ██║   ██║   ██║   ██║██████╔╝█████╗   ║
║  ██╔═══╝   ╚██╔╝  ██╔══██║██║  ██║╚██╗ ██╔╝██╔══╝  ██║╚██╗██║   ██║   ██║   ██║██╔══██╗██╔══╝   ║
║  ██║        ██║   ██║  ██║██████╔╝ ╚████╔╝ ███████╗██║ ╚████║   ██║   ╚██████╔╝██║  ██║███████╗ ║
║  ╚═╝        ╚═╝   ╚═╝  ╚═╝╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═══╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝ ║
║                                                                               ║
║                    A CLI Adventure Game for Learning Python                   ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
        """
        print(banner)
        print("Welcome to PyAdventure! Learn Python through interactive storytelling.")
        print("Type 'quit' at any time to exit the game.\n")
    
    def quit_game(self):
        """Quit the game"""
        print("\nThanks for playing PyAdventure!")
        print(f"Final Score: {self.player.experience} XP")
        self.running = False
        sys.exit(0)


def main():
    """Main entry point"""
    game = PyAdventureGame()
    game.start()


if __name__ == "__main__":
    main()
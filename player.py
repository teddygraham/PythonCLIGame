#!/usr/bin/env python3
"""
PyAdventure Player Module
Handles player progress, save/load functionality, and game state management
"""

import json
import os
from typing import List, Dict, Any


class Player:
    """Player class for tracking progress and managing save/load functionality"""
    
    def __init__(self, save_file: str = "player_save.json"):
        self.save_file = save_file
        self.experience = 0
        self.completed_challenges = []
        self.current_story = "intro"
        self.current_scene = 0
        self.inventory = []
        self.achievements = []
        
        # Load existing save if it exists
        self.load_progress()
    
    def add_experience(self, amount: int):
        """Add experience points to the player"""
        self.experience += amount
        print(f"📈 Gained {amount} XP! Total: {self.experience} XP")
        self.save_progress()
    
    def complete_challenge(self, challenge_id: str):
        """Mark a challenge as completed"""
        if challenge_id not in self.completed_challenges:
            self.completed_challenges.append(challenge_id)
            print(f"🏆 Challenge '{challenge_id}' completed!")
            self.save_progress()
    
    def add_to_inventory(self, item: str):
        """Add an item to the player's inventory"""
        self.inventory.append(item)
        print(f"🎒 Added '{item}' to inventory")
        self.save_progress()
    
    def unlock_achievement(self, achievement: str):
        """Unlock an achievement"""
        if achievement not in self.achievements:
            self.achievements.append(achievement)
            print(f"🏅 Achievement unlocked: {achievement}")
            self.save_progress()
    
    def set_story_progress(self, story: str, scene: int):
        """Update story progress"""
        self.current_story = story
        self.current_scene = scene
        self.save_progress()
    
    def get_level(self) -> int:
        """Calculate player level based on experience"""
        return max(1, self.experience // 50)
    
    def save_progress(self):
        """Save player progress to JSON file"""
        try:
            save_data = {
                "experience": self.experience,
                "completed_challenges": self.completed_challenges,
                "current_story": self.current_story,
                "current_scene": self.current_scene,
                "inventory": self.inventory,
                "achievements": self.achievements
            }
            
            with open(self.save_file, 'w') as f:
                json.dump(save_data, f, indent=2)
                
        except Exception as e:
            print(f"Warning: Could not save progress: {e}")
    
    def load_progress(self):
        """Load player progress from JSON file"""
        try:
            if os.path.exists(self.save_file):
                with open(self.save_file, 'r') as f:
                    save_data = json.load(f)
                
                self.experience = save_data.get("experience", 0)
                self.completed_challenges = save_data.get("completed_challenges", [])
                self.current_story = save_data.get("current_story", "intro")
                self.current_scene = save_data.get("current_scene", 0)
                self.inventory = save_data.get("inventory", [])
                self.achievements = save_data.get("achievements", [])
                
                print(f"📂 Progress loaded: Level {self.get_level()}, {self.experience} XP")
            else:
                print("🆕 Starting new adventure!")
                
        except Exception as e:
            print(f"Warning: Could not load progress: {e}")
            print("🆕 Starting new adventure!")
    
    def reset_progress(self):
        """Reset all player progress"""
        self.experience = 0
        self.completed_challenges = []
        self.current_story = "intro"
        self.current_scene = 0
        self.inventory = []
        self.achievements = []
        
        # Remove save file
        if os.path.exists(self.save_file):
            os.remove(self.save_file)
        
        print("🔄 Progress reset successfully!")
    
    def show_status(self):
        """Display current player status"""
        print("\n" + "="*40)
        print("PLAYER STATUS")
        print("="*40)
        print(f"Level: {self.get_level()}")
        print(f"Experience: {self.experience} XP")
        print(f"Current Story: {self.current_story}")
        print(f"Current Scene: {self.current_scene}")
        print(f"Challenges Completed: {len(self.completed_challenges)}")
        print(f"Inventory Items: {len(self.inventory)}")
        print(f"Achievements: {len(self.achievements)}")
        
        if self.inventory:
            print(f"Inventory: {', '.join(self.inventory)}")
        
        if self.achievements:
            print(f"Achievements: {', '.join(self.achievements)}")
        
        print("="*40)
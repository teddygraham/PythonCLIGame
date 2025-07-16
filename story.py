#!/usr/bin/env python3
"""
Story management module for PyAdventure
Handles story loading, scene progression, and narrative flow
"""

import json
import os
from typing import Dict, Any, Optional


class StoryManager:
    """Manages story content and progression"""
    
    def __init__(self, stories_dir: str = "stories"):
        self.stories_dir = stories_dir
        self.current_story = None
        self.current_scene_index = 0
        self.story_data = {}
    
    def load_story(self, story_name: str) -> bool:
        """Load a story from the stories directory"""
        story_path = os.path.join(self.stories_dir, f"{story_name}.json")
        
        if not os.path.exists(story_path):
            # Create a basic intro story if it doesn't exist
            self.create_default_story(story_name)
            
        try:
            with open(story_path, 'r') as f:
                self.story_data = json.load(f)
            self.current_story = story_name
            self.current_scene_index = 0
            return True
        except Exception as e:
            print(f"Error loading story '{story_name}': {e}")
            return False
    
    def create_default_story(self, story_name: str):
        """Create a default intro story"""
        default_story = {
            "title": "PyAdventure: Learn Python Through Adventure",
            "description": "A beginner-friendly adventure game for learning Python",
            "scenes": [
                {
                    "id": "intro",
                    "title": "Welcome to PyAdventure!",
                    "description": "You find yourself in a mysterious digital world where Python code is the key to survival. Your journey begins here.",
                    "type": "choice",
                    "choices": [
                        {
                            "text": "Learn about variables",
                            "next_scene": "variables"
                        },
                        {
                            "text": "Explore the world",
                            "next_scene": "explore"
                        }
                    ]
                },
                {
                    "id": "variables",
                    "title": "The Variable Valley",
                    "description": "You enter a valley where data flows like rivers. To cross safely, you must understand variables.",
                    "type": "challenge",
                    "code_example": "name = 'adventurer'\nage = 25\nprint(f'Hello, {name}! You are {age} years old.')",
                    "challenge": {
                        "prompt": "Create a variable called 'message' and set it to 'Hello, Python!'",
                        "expected_output": "Hello, Python!",
                        "hint": "Use the assignment operator (=) to create a variable"
                    }
                },
                {
                    "id": "explore",
                    "title": "The Coding Forest",
                    "description": "You venture into a forest where the trees whisper secrets of programming.",
                    "type": "choice",
                    "choices": [
                        {
                            "text": "Listen to the trees",
                            "next_scene": "end"
                        },
                        {
                            "text": "Go back to the beginning",
                            "next_scene": "intro"
                        }
                    ]
                },
                {
                    "id": "end",
                    "title": "Your Adventure Continues...",
                    "description": "This is just the beginning of your Python adventure. More challenges await!",
                    "type": "ending"
                }
            ]
        }
        
        os.makedirs(self.stories_dir, exist_ok=True)
        story_path = os.path.join(self.stories_dir, f"{story_name}.json")
        
        with open(story_path, 'w') as f:
            json.dump(default_story, f, indent=2)
    
    def get_current_scene(self) -> Optional[Dict[str, Any]]:
        """Get the current scene data"""
        if not self.story_data or "scenes" not in self.story_data:
            return None
            
        scenes = self.story_data["scenes"]
        if 0 <= self.current_scene_index < len(scenes):
            return scenes[self.current_scene_index]
        return None
    
    def advance_to_next_scene(self):
        """Advance to the next scene in sequence"""
        if self.story_data and "scenes" in self.story_data:
            self.current_scene_index += 1
    
    def advance_to_scene(self, scene_id: str):
        """Advance to a specific scene by ID"""
        if not self.story_data or "scenes" not in self.story_data:
            return
            
        scenes = self.story_data["scenes"]
        for i, scene in enumerate(scenes):
            if scene.get("id") == scene_id:
                self.current_scene_index = i
                return
        
        # If scene not found, go to next scene
        self.advance_to_next_scene()
    
    def get_story_progress(self) -> Dict[str, Any]:
        """Get current story progress"""
        return {
            "current_story": self.current_story,
            "current_scene": self.current_scene_index,
            "total_scenes": len(self.story_data.get("scenes", []))
        }
from typing import Dict, List, Any

class RoadmapGenerator:
    """Generates personalized career learning roadmaps."""

    def __init__(self):
        # Skill details with learning resources
        self.skill_details = {
            "python": {
                "description": "High-level programming language for general purpose programming",
                "difficulty": "beginner",
                "estimated_hours": 40,
                "prerequisites": [],
                "resources": [
                    {"name": "Python.org Tutorial", "url": "https://docs.python.org/3/tutorial/"},
                    {"name": "FreeCodeCamp Python", "url": "https://www.freecodecamp.org/learn/scientific-computing-with-python/"},
                    {"name": "Automate the Boring Stuff", "url": "https://automatetheboringstuff.com/"}
                ]
            },
            "javascript": {
                "description": "Programming language for web development",
                "difficulty": "beginner",
                "estimated_hours": 50,
                "prerequisites": ["html", "css"],
                "resources": [
                    {"name": "MDN JavaScript Guide", "url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide"},
                    {"name": "JavaScript.info", "url": "https://javascript.info/"},
                    {"name": "FreeCodeCamp JavaScript", "url": "https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/"}
                ]
            },
            "html": {
                "description": "Standard markup language for web pages",
                "difficulty": "beginner",
                "estimated_hours": 15,
                "prerequisites": [],
                "resources": [
                    {"name": "MDN HTML Tutorial", "url": "https://developer.mozilla.org/en-US/docs/Web/HTML"},
                    {"name": "W3Schools HTML", "url": "https://www.w3schools.com/html/"}
                ]
            },
            "css": {
                "description": "Style sheet language for web page styling",
                "difficulty": "beginner",
                "estimated_hours": 20,
                "prerequisites": ["html"],
                "resources": [
                    {"name": "MDN CSS Tutorial", "url": "https://developer.mozilla.org/en-US/docs/Web/CSS"},
                    {"name": "CSS-Tricks", "url": "https://css-tricks.com/"}
                ]
            },
            "react": {
                "description": "JavaScript library for building user interfaces",
                "difficulty": "intermediate",
                "estimated_hours": 40,
                "prerequisites": ["javascript", "html", "css"],
                "resources": [
                    {"name": "React Documentation", "url": "https://react.dev/"},
                    {"name": "React Tutorial", "url": "https://react.dev/learn"},
                    {"name": "Build an App with React", "url": "https://www.freecodecamp.org/news/learn-react-by-building-an-app/"}
                ]
            },
            "node": {
                "description": "JavaScript runtime for server-side programming",
                "difficulty": "intermediate",
                "estimated_hours": 35,
                "prerequisites": ["javascript"],
                "resources": [
                    {"name": "Node.js Documentation", "url": "https://nodejs.org/docs/"},
                    {"name": "Node.js Tutorial", "url": "https://www.w3schools.com/nodejs/"}
                ]
            },
            "sql": {
                "description": "Database query language",
                "difficulty": "beginner",
                "estimated_hours": 25,
                "prerequisites": [],
                "resources": [
                    {"name": "SQL Tutorial", "url": "https://www.w3schools.com/sql/"},
                    {"name": "Mode SQL Tutorial", "url": "https://mode.com/sql-tutorial/"}
                ]
            },
            "postgresql": {
                "description": "Advanced open-source relational database",
                "difficulty": "intermediate",
                "estimated_hours": 30,
                "prerequisites": ["sql"],
                "resources": [
                    {"name": "PostgreSQL Documentation", "url": "https://www.postgresql.org/docs/"},
                    {"name": "PostgreSQL Tutorial", "url": "https://www.postgresqltutorial.com/"}
                ]
            },
            "docker": {
                "description": "Containerization platform",
                "difficulty": "intermediate",
                "estimated_hours": 25,
                "prerequisites": ["linux"],
                "resources": [
                    {"name": "Docker Documentation", "url": "https://docs.docker.com/"},
                    {"name": "Docker for Beginners", "url": "https://www.docker.com/101-tutorial/"}
                ]
            },
            "aws": {
                "description": "Amazon Web Services cloud platform",
                "difficulty": "advanced",
                "estimated_hours": 50,
                "prerequisites": ["docker"],
                "resources": [
                    {"name": "AWS Documentation", "url": "https://docs.aws.amazon.com/"},
                    {"name": "AWS Cloud Practitioner", "url": "https://aws.amazon.com/training/path-cloudpractitioner/"}
                ]
            },
            "git": {
                "description": "Version control system",
                "difficulty": "beginner",
                "estimated_hours": 10,
                "prerequisites": [],
                "resources": [
                    {"name": "Git Documentation", "url": "https://git-scm.com/doc"},
                    {"name": "Git Tutorial", "url": "https://www.atlassian.com/git/tutorials"}
                ]
            },
            "machine learning": {
                "description": "Subset of AI that enables systems to learn",
                "difficulty": "advanced",
                "estimated_hours": 80,
                "prerequisites": ["python", "statistics", "math"],
                "resources": [
                    {"name": "Andrew Ng's ML Course", "url": "https://www.coursera.org/learn/machine-learning"},
                    {"name": "scikit-learn Documentation", "url": "https://scikit-learn.org/"}
                ]
            },
            "data structures": {
                "description": "Ways of organizing and storing data",
                "difficulty": "intermediate",
                "estimated_hours": 40,
                "prerequisites": ["python"],
                "resources": [
                    {"name": "GeeksforGeeks DSA", "url": "https://www.geeksforgeeks.org/data-structures/"},
                    {"name": "CLRS Book", "url": "https://mitpress.mit.edu/books/introduction-algorithms"}
                ]
            }
        }

        # Role learning paths
        self.role_paths = {
            "software_developer": ["python", "javascript", "html", "css", "sql", "git", "data structures", "react", "node", "postgresql", "docker", "aws"],
            "full_stack_developer": ["html", "css", "javascript", "git", "react", "node", "sql", "python", "postgresql", "docker", "aws"],
            "data_scientist": ["python", "sql", "statistics", "pandas", "machine learning", "data visualization", "tensorflow", "nlp"],
            "frontend_developer": ["html", "css", "javascript", "git", "react", "typescript", "responsive design", "figma"],
            "backend_developer": ["python", "sql", "git", "api", "django", "postgresql", "docker", "aws"],
            "devops_engineer": ["linux", "bash", "git", "docker", "aws", "jenkins", "kubernetes", "terraform", "ci/cd"],
            "machine_learning_engineer": ["python", "machine learning", "tensorflow", "deep learning", "pytorch", "scikit-learn", "docker", "nlp", "computer vision"]
        }

    def generate_roadmap(self, current_skills: List[str], target_role: str) -> Dict[str, Any]:
        """Generate a personalized learning roadmap."""
        role_lower = target_role.lower()

        # Find matching role
        matched_role = None
        for role_name in self.role_paths.keys():
            if role_name.replace("_", " ") in role_lower or role_name in role_lower:
                matched_role = role_name
                break

        if not matched_role:
            matched_role = "software_developer"

        # Get learning path
        learning_path = self.role_paths[matched_role]

        # Normalize current skills
        current_skills_normalized = [s.lower().strip() for s in current_skills]

        # Determine current level
        current_level = self._assess_level(current_skills_normalized, matched_role)

        # Generate roadmap items
        roadmap_items = []
        for skill in learning_path:
            # Skip already acquired skills
            if any(skill in cur or cur in skill for cur in current_skills_normalized):
                continue

            skill_info = self.skill_details.get(skill, {
                "description": f"Learn {skill}",
                "difficulty": "intermediate",
                "estimated_hours": 20,
                "prerequisites": [],
                "resources": []
            })

            # Check if prerequisites are met
            prereqs_met = all(
                any(p in cur or cur in p for cur in current_skills_normalized)
                for p in skill_info.get("prerequisites", [])
            ) if skill_info.get("prerequisites") else True

            roadmap_items.append({
                "skill_name": skill,
                "description": skill_info.get("description", ""),
                "difficulty": skill_info.get("difficulty", "intermediate"),
                "estimated_hours": skill_info.get("estimated_hours", 20),
                "prerequisites": skill_info.get("prerequisites", []),
                "resources": skill_info.get("resources", []),
                "is_completed": False,
                "prerequisites_met": prereqs_met
            })

        return {
            "current_level": current_level,
            "target_level": "professional",
            "items": roadmap_items[:10]  # Limit to 10 items
        }

    def _assess_level(self, skills: List[str], role: str) -> str:
        """Assess user's current skill level."""
        role_path = self.role_paths.get(role, [])
        matched_skills = sum(1 for skill in role_path if any(skill in s or s in skill for s in skills))

        total_skills = len(role_path)
        percentage = (matched_skills / total_skills) * 100 if total_skills > 0 else 0

        if percentage >= 70:
            return "professional"
        elif percentage >= 40:
            return "intermediate"
        elif percentage >= 10:
            return "beginner"
        else:
            return "novice"

    def get_skill_details(self, skill_name: str) -> Dict[str, Any]:
        """Get detailed information about a specific skill."""
        return self.skill_details.get(skill_name.lower(), {
            "description": f"Learn {skill_name}",
            "difficulty": "intermediate",
            "estimated_hours": 20,
            "prerequisites": [],
            "resources": []
        })
from typing import Dict, List, Any

class SkillGapAnalyzer:
    """Analyzes skill gaps between current user skills and target role requirements."""

    def __init__(self):
        # Comprehensive role skill mappings
        self.role_skill_requirements = {
            "software_developer": {
                "required": ["python", "javascript", "sql", "git", "data structures"],
                "preferred": ["docker", "aws", "react", "postgresql", "rest api", "agile"],
                "learning_order": ["python", "javascript", "html", "css", "sql", "git", "react", "node", "postgresql", "docker", "aws"]
            },
            "full_stack_developer": {
                "required": ["javascript", "html", "css", "react", "node", "sql", "git"],
                "preferred": ["typescript", "python", "docker", "aws", "mongodb", "rest api"],
                "learning_order": ["html", "css", "javascript", "react", "node", "sql", "python", "typescript", "docker", "aws", "mongodb"]
            },
            "data_scientist": {
                "required": ["python", "statistics", "machine learning", "sql", "pandas"],
                "preferred": ["tensorflow", "scikit-learn", "data visualization", "deep learning", "nlp"],
                "learning_order": ["python", "statistics", "sql", "pandas", "machine learning", "data visualization", "tensorflow", "nlp", "deep learning"]
            },
            "frontend_developer": {
                "required": ["html", "css", "javascript", "react", "git"],
                "preferred": ["typescript", "vue", "angular", "figma", "responsive design"],
                "learning_order": ["html", "css", "javascript", "git", "react", "typescript", "responsive design", "figma", "vue"]
            },
            "backend_developer": {
                "required": ["python", "sql", "api", "git"],
                "preferred": ["django", "flask", "postgresql", "docker", "aws", "rest api"],
                "learning_order": ["python", "sql", "git", "api", "django", "postgresql", "docker", "aws", "rest api"]
            },
            "devops_engineer": {
                "required": ["linux", "docker", "git", "bash"],
                "preferred": ["kubernetes", "aws", "jenkins", "terraform", "ansible", "ci/cd"],
                "learning_order": ["linux", "bash", "git", "docker", "aws", "jenkins", "kubernetes", "terraform", "ci/cd"]
            },
            "mobile_developer": {
                "required": ["javascript", "react native", "git", "mobile development"],
                "preferred": ["flutter", "swift", "kotlin", "android", "ios"],
                "learning_order": ["javascript", "git", "mobile development", "react native", "flutter", "android", "ios"]
            },
            "machine_learning_engineer": {
                "required": ["python", "machine learning", "tensorflow", "deep learning"],
                "preferred": ["pytorch", "scikit-learn", "docker", "aws", "nlp", "computer vision"],
                "learning_order": ["python", "machine learning", "tensorflow", "deep learning", "pytorch", "scikit-learn", "docker", "nlp", "computer vision"]
            },
            "data_analyst": {
                "required": ["python", "sql", "excel", "data visualization"],
                "preferred": ["tableau", "power bi", "pandas", "statistics"],
                "learning_order": ["excel", "sql", "python", "data visualization", "pandas", "tableau", "statistics", "power bi"]
            }
        }

        # Priority thresholds
        self.priority_thresholds = {
            "high": 5,  # Missing more than 5 core skills is HIGH priority
            "medium": 3,  # Missing 3-5 core skills is MEDIUM
            "low": 1  # Missing less than 3 is LOW
        }

    def analyze_gaps(self, current_skills: List[str], target_role: str) -> Dict[str, Any]:
        """Analyze skill gaps for a target role."""
        role_lower = target_role.lower()

        # Find matching role
        matched_role = None
        for role_name, requirements in self.role_skill_requirements.items():
            if role_name.replace("_", " ") in role_lower or role_name in role_lower:
                matched_role = role_name
                break

        # If no exact match, try partial match
        if not matched_role:
            for role_name in self.role_skill_requirements.keys():
                if any(word in role_lower for word in role_name.split("_")):
                    matched_role = role_name
                    break

        # Default to software developer if no match
        if not matched_role:
            matched_role = "software_developer"

        requirements = self.role_skill_requirements[matched_role]
        required_skills = [s.lower() for s in requirements["required"]]
        preferred_skills = [s.lower() for s in requirements["preferred"]]

        # Normalize current skills
        current_skills_normalized = [s.lower().strip() for s in current_skills]

        # Find missing skills
        missing_required = []
        missing_preferred = []

        for skill in required_skills:
            if not any(skill in cur or cur in skill for cur in current_skills_normalized):
                missing_required.append(skill)

        for skill in preferred_skills:
            if not any(skill in cur or cur in skill for cur in current_skills_normalized):
                missing_preferred.append(skill)

        # Determine priority
        missing_count = len(missing_required)
        if missing_count >= self.priority_thresholds["high"]:
            priority = "high"
        elif missing_count >= self.priority_thresholds["medium"]:
            priority = "medium"
        else:
            priority = "low"

        # Get learning order for missing skills
        learning_order = requirements.get("learning_order", [])
        prioritized_gaps = []

        for skill in learning_order:
            if skill in missing_required:
                prioritized_gaps.append({"skill": skill, "priority": "required"})
            elif skill in missing_preferred:
                prioritized_gaps.append({"skill": skill, "priority": "preferred"})

        return {
            "target_role": matched_role.replace("_", " ").title(),
            "current_skills": current_skills_normalized,
            "required_skills": required_skills,
            "preferred_skills": preferred_skills,
            "missing_required_skills": missing_required,
            "missing_preferred_skills": missing_preferred,
            "all_missing_skills": missing_required + missing_preferred,
            "priority": priority,
            "priority_skills": prioritized_gaps,
            "match_percentage": round(((len(required_skills) - len(missing_required)) / len(required_skills)) * 100, 1) if required_skills else 0
        }

    def get_skill_importance(self, skill: str, role: str) -> str:
        """Determine if a skill is required or preferred for a role."""
        role_lower = role.lower()
        matched_role = None

        for role_name in self.role_skill_requirements.keys():
            if role_name.replace("_", " ") in role_lower or role_name in role_lower:
                matched_role = role_name
                break

        if not matched_role:
            return "preferred"

        requirements = self.role_skill_requirements[matched_role]
        skill_lower = skill.lower()

        if any(skill_lower in s for s in requirements["required"]):
            return "required"
        elif any(skill_lower in s for s in requirements["preferred"]):
            return "preferred"
        else:
            return "optional"

    def suggest_learning_path(self, current_skills: List[str], target_role: str) -> List[Dict[str, Any]]:
        """Suggest a prioritized learning path."""
        gap_analysis = self.analyze_gaps(current_skills, target_role)

        learning_path = []
        for skill_info in gap_analysis.get("priority_skills", []):
            learning_path.append({
                "skill": skill_info["skill"],
                "priority": skill_info["priority"],
                "importance": "must_learn" if skill_info["priority"] == "required" else "should_learn"
            })

        return learning_path
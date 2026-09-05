import re
import json
from typing import Dict, List, Any

class ResumeAnalyzer:
    def __init__(self):
        # Industry keywords for different roles
        self.role_keywords = {
            "software_developer": [
                "python", "javascript", "java", "c++", "react", "node", "sql",
                "git", "docker", "aws", "rest", "api", "agile", "scrum"
            ],
            "data_scientist": [
                "python", "r", "sql", "machine learning", "data analysis",
                "statistics", "pandas", "numpy", "scikit-learn", "tensorflow",
                "pytorch", "data visualization"
            ],
            "frontend_developer": [
                "html", "css", "javascript", "react", "angular", "vue",
                "typescript", "responsive design", "ui/ux", "figma"
            ],
            "backend_developer": [
                "python", "java", "c#", "node", "express", "django", "flask",
                "spring", "sql", "nosql", "rest", "api", "microservices", "docker"
            ],
            "devops": [
                "docker", "kubernetes", "aws", "azure", "gcp", "ci/cd", "jenkins",
                "terraform", "ansible", "linux", "bash", "shell scripting"
            ]
        }

        # ATS (Applicant Tracking System) keywords
        self.ats_keywords = [
            "achieved", "improved", "increased", "decreased", "optimized",
            "developed", "implemented", "managed", "led", "created", "designed",
            "analyzed", "resolved", "maintained", "collaborated", "delivered"
        ]

        # Measurable achievement patterns
        self.achievement_patterns = [
            r'increased.*by.*%', r'reduced.*by.*%', r'improved.*by.*%',
            r'saved.*\$', r'achieved.*\$', r'grew.*by.*%', r'decreased.*by.*%',
            r'cut.*by.*%', r'boosted.*by.*%', r'enhanced.*by.*%'
        ]

    def analyze_resume(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze resume and generate comprehensive feedback."""
        analysis = {
            "overall_score": 0,
            "skills_score": 0,
            "projects_score": 0,
            "experience_score": 0,
            "keywords_score": 0,
            "formatting_score": 0,
            "strengths": [],
            "weaknesses": [],
            "recommendations": []
        }

        # Calculate individual scores
        skills_score = self._analyze_skills(resume_data.get("skills", []))
        projects_score = self._analyze_projects(resume_data.get("projects", []))
        experience_score = self._analyze_experience(resume_data.get("experience", []))
        keywords_score = self._analyze_keywords(resume_data)
        formatting_score = self._analyze_formatting(resume_data)

        # Calculate overall weighted score
        analysis["overall_score"] = round(
            (skills_score["score"] * 0.2) +
            (projects_score["score"] * 0.2) +
            (experience_score["score"] * 0.2) +
            (keywords_score["score"] * 0.2) +
            (formatting_score["score"] * 0.2)
        )

        # Set individual scores
        analysis["skills_score"] = skills_score["score"]
        analysis["projects_score"] = projects_score["score"]
        analysis["experience_score"] = experience_score["score"]
        analysis["keywords_score"] = keywords_score["score"]
        analysis["formatting_score"] = formatting_score["score"]

        # Combine feedback
        analysis["strengths"] = self._extract_strengths(skills_score, projects_score, experience_score, keywords_score)
        analysis["weaknesses"] = self._extract_weaknesses(skills_score, projects_score, experience_score, keywords_score)
        analysis["recommendations"] = self._generate_recommendations(analysis["weaknesses"], resume_data)

        return analysis

    def _analyze_skills(self, skills: List[str]) -> Dict[str, Any]:
        """Analyze technical skills."""
        score = 0
        feedback = []

        if not skills:
            return {"score": 0, "feedback": ["No skills listed"]}

        # Score based on number of skills
        if len(skills) >= 10:
            score = 20
        elif len(skills) >= 5:
            score = 15
        elif len(skills) >= 3:
            score = 10
        else:
            score = 5

        # Check for in-demand skills
        in_demand = ["python", "javascript", "react", "sql", "aws", "docker", "git"]
        found_in_demand = sum(1 for skill in skills if any(tech in skill.lower() for tech in in_demand))

        if found_in_demand >= 3:
            score += 5
            feedback.append(f"Great! Found {found_in_demand} in-demand technologies")
        elif found_in_demand >= 1:
            score += 3
            feedback.append(f"Good start with {found_in_demand} in-demand technology")

        # Check skill diversity
        categories = {"frontend": 0, "backend": 0, "tools": 0, "cloud": 0}

        frontend_tech = ["html", "css", "javascript", "react", "angular", "vue", "typescript"]
        backend_tech = ["python", "java", "c++", "c#", "node", "express", "django", "flask", "spring", "php"]
        cloud_tech = ["aws", "azure", "gcp", "docker", "kubernetes"]
        tool_tech = ["git", "github", "gitlab", "jenkins", "jira", "confluence"]

        for skill in skills:
            skill_lower = skill.lower()
            if any(tech in skill_lower for tech in frontend_tech):
                categories["frontend"] += 1
            elif any(tech in skill_lower for tech in backend_tech):
                categories["backend"] += 1
            elif any(tech in skill_lower for tech in cloud_tech):
                categories["cloud"] += 1
            elif any(tech in skill_lower for tech in tool_tech):
                categories["tools"] += 1

        # Bonus for diverse skill set
        diverse_categories = sum(1 for count in categories.values() if count > 0)
        if diverse_categories >= 3:
            score += 5
            feedback.append("Excellent skill diversity across multiple categories")

        return {"score": min(score, 20), "feedback": feedback}

    def _analyze_projects(self, projects: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze projects section."""
        score = 0
        feedback = []

        if not projects:
            return {"score": 0, "feedback": ["No projects listed"]}

        # Score based on number of projects
        if len(projects) >= 3:
            score = 15
        elif len(projects) >= 2:
            score = 12
        else:
            score = 8

        # Analyze project quality
        quality_indicators = {
            "has_description": 0,
            "has_technologies": 0,
            "has_urls": 0,
            "has_measurable_outcomes": 0
        }

        for project in projects:
            if project.get("description") and len(project["description"]) > 30:
                quality_indicators["has_description"] += 1

            if project.get("technologies") and len(project["technologies"]) > 0:
                quality_indicators["has_technologies"] += 1

            if project.get("github_url") or project.get("live_url"):
                quality_indicators["has_urls"] += 1

            # Check for measurable outcomes
            if project.get("description"):
                desc = project["description"].lower()
                for pattern in self.achievement_patterns:
                    if re.search(pattern, desc):
                        quality_indicators["has_measurable_outcomes"] += 1
                        break

        # Calculate quality score
        quality_score = sum(quality_indicators.values()) * 1.25
        score += min(quality_score, 5)

        # Generate feedback
        if quality_indicators["has_urls"] > 0:
            feedback.append("Good job including project URLs - makes it easy to verify your work")
        if quality_indicators["has_measurable_outcomes"] > 0:
            feedback.append("Excellent use of measurable outcomes in project descriptions")

        return {"score": min(score, 20), "feedback": feedback}

    def _analyze_experience(self, experience: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze work experience section."""
        score = 0
        feedback = []

        if not experience:
            return {"score": 0, "feedback": ["No work experience listed"]}

        # Score based on number of experiences
        if len(experience) >= 3:
            score = 15
        elif len(experience) >= 2:
            score = 12
        else:
            score = 8

        # Analyze experience quality
        quality_indicators = {
            "has_duration": 0,
            "has_detailed_description": 0,
            "has_measurable_achievements": 0,
            "has_action_verbs": 0
        }

        for exp in experience:
            if exp.get("duration"):
                quality_indicators["has_duration"] += 1

            if exp.get("description") and len(exp["description"]) > 50:
                quality_indicators["has_detailed_description"] += 1

                # Check for action verbs
                description_lower = exp["description"].lower()
                for verb in self.ats_keywords:
                    if verb in description_lower:
                        quality_indicators["has_action_verbs"] += 1
                        break

                # Check for measurable achievements
                for pattern in self.achievement_patterns:
                    if re.search(pattern, description_lower):
                        quality_indicators["has_measurable_achievements"] += 1
                        break

        # Calculate quality score
        quality_score = sum(quality_indicators.values()) * 1.25
        score += min(quality_score, 5)

        # Generate feedback
        if quality_indicators["has_action_verbs"] > 0:
            feedback.append("Good use of action verbs in experience descriptions")
        if quality_indicators["has_measurable_achievements"] > 0:
            feedback.append("Excellent use of measurable achievements - recruiters love numbers!")

        return {"score": min(score, 20), "feedback": feedback}

    def _analyze_keywords(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze keyword usage for ATS optimization."""
        score = 0
        feedback = []
        keywords_found = []

        # Combine all text from resume
        all_text = ""

        if resume_data.get("personal_info"):
            all_text += " ".join(str(v) for v in resume_data["personal_info"].values())

        if resume_data.get("education"):
            for edu in resume_data["education"]:
                all_text += " ".join(str(v) for v in edu.values())

        if resume_data.get("experience"):
            for exp in resume_data["experience"]:
                all_text += " ".join(str(v) for v in exp.values())

        if resume_data.get("projects"):
            for proj in resume_data["projects"]:
                all_text += " ".join(str(v) for v in proj.values())

        all_text = all_text.lower()

        # Check for ATS keywords
        for keyword in self.ats_keywords:
            if keyword in all_text:
                keywords_found.append(keyword)

        # Score based on keyword usage
        if len(keywords_found) >= 10:
            score = 20
        elif len(keywords_found) >= 5:
            score = 15
        elif len(keywords_found) >= 3:
            score = 10
        else:
            score = 5

        # Check for role-specific keywords
        role_matches = {}
        for role, keywords in self.role_keywords.items():
            matches = sum(1 for keyword in keywords if keyword in all_text)
            role_matches[role] = matches

        # Find best matching role
        best_role = max(role_matches.items(), key=lambda x: x[1])
        if best_role[1] >= 5:
            score += 5
            feedback.append(f"Strong keyword alignment with {best_role[0].replace('_', ' ')} role")

        # Generate keyword suggestions
        if len(keywords_found) < 5:
            missing = [k for k in self.ats_keywords[:10] if k not in keywords_found]
            feedback.append(f"Consider adding more action verbs like: {', '.join(missing[:5])}")

        return {"score": min(score, 20), "feedback": feedback}

    def _analyze_formatting(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze resume formatting and structure."""
        score = 15  # Base score
        feedback = []

        # Check for all essential sections
        essential_sections = ["education", "skills", "projects"]
        missing_sections = []

        for section in essential_sections:
            if not resume_data.get(section) or len(resume_data[section]) == 0:
                missing_sections.append(section)

        if missing_sections:
            score -= len(missing_sections) * 3
            feedback.append(f"Missing sections: {', '.join(missing_sections)}")

        # Check personal info completeness
        personal_info = resume_data.get("personal_info", {})
        required_info = ["name", "email"]
        missing_info = [info for info in required_info if not personal_info.get(info)]

        if missing_info:
            score -= len(missing_info) * 2
            feedback.append(f"Missing personal information: {', '.join(missing_info)}")

        # Check for contact info
        if personal_info.get("email") and personal_info.get("phone"):
            score += 3
            feedback.append("Good contact information")

        # Check for GitHub/LinkedIn
        if personal_info.get("github") or personal_info.get("linkedin"):
            score += 2
            feedback.append("Professional links included - great for recruiters")

        return {"score": min(max(score, 0), 20), "feedback": feedback}

    def _extract_strengths(self, *scores) -> List[str]:
        """Extract strengths from all analyses."""
        strengths = []

        for score_data in scores:
            for feedback in score_data["feedback"]:
                if any(word in feedback.lower() for word in ["great", "excellent", "good", "strong", "diverse"]):
                    strengths.append(feedback)

        return strengths[:5] if len(strengths) > 5 else strengths

    def _extract_weaknesses(self, *scores) -> List[str]:
        """Extract weaknesses from all analyses."""
        weaknesses = []

        for score_data in scores:
            for feedback in score_data["feedback"]:
                if any(word in feedback.lower() for word in ["no", "missing", "few", "need", "add", "consider"]):
                    weaknesses.append(feedback)

        return weaknesses[:5] if len(weaknesses) > 5 else weaknesses

    def _generate_recommendations(self, weaknesses: List[str], resume_data: Dict[str, Any]) -> List[str]:
        """Generate personalized recommendations."""
        recommendations = []

        # General recommendations
        if "No work experience listed" in weaknesses:
            recommendations.append("Consider adding internship, volunteer work, or academic projects to the experience section")

        if "No projects listed" in weaknesses:
            recommendations.append("Create 2-3 personal projects to showcase your skills. Include GitHub links and detailed descriptions")

        if "No skills listed" in weaknesses:
            recommendations.append("Add a dedicated skills section with technical and soft skills relevant to your target role")

        # Keyword optimization
        all_text = " ".join(str(v) for section in resume_data.values() for v in (section if isinstance(section, list) else [section]))
        action_verb_count = sum(1 for verb in self.ats_keywords if verb in all_text.lower())

        if action_verb_count < 5:
            recommendations.append(f"Add more action verbs. Currently using {action_verb_count}, aim for 8-10")

        # Skill recommendations based on missing sections
        missing_skills = []
        if resume_data.get("skills"):
            current_skills = [s.lower() for s in resume_data["skills"]]
            for role, keywords in self.role_keywords.items():
                if any(keyword in all_text.lower() for keyword in keywords[:5]):
                    # This seems to be the target role
                    missing = [k for k in keywords if k not in current_skills]
                    if missing:
                        recommendations.append(f"For {role.replace('_', ' ')} roles, consider learning: {', '.join(missing[:3])}")

        return recommendations[:5] if len(recommendations) > 5 else recommendations
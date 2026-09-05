from typing import Dict, List, Any

class AIAssistant:
    """AI-powered career assistant for answering user queries."""

    def __init__(self):
        # Knowledge base for common career questions
        self.career_knowledge = {
            "python_developer": {
                "skills": ["python", "django", "flask", "sql", "git", "docker", "rest api"],
                "learning_path": [
                    "Start with Python basics (data types, control flow, functions)",
                    "Learn object-oriented programming",
                    "Study data structures and algorithms",
                    "Master a web framework (Django or Flask)",
                    "Learn SQL and database design",
                    "Understand version control with Git",
                    "Deploy applications using Docker",
                    "Build RESTful APIs"
                ],
                "internship_advice": "Focus on building real projects and contributing to open source."
            },
            "web_developer": {
                "skills": ["html", "css", "javascript", "react", "node", "sql", "git"],
                "learning_path": [
                    "Master HTML and CSS fundamentals",
                    "Learn JavaScript ES6+",
                    "Understand DOM manipulation",
                    "Study a frontend framework (React)",
                    "Learn backend basics (Node.js or Python)",
                    "Master database concepts",
                    "Build full-stack projects",
                    "Deploy and maintain web applications"
                ],
                "internship_advice": "Create a portfolio website to showcase your projects."
            },
            "data_scientist": {
                "skills": ["python", "sql", "statistics", "machine learning", "pandas", "visualization"],
                "learning_path": [
                    "Learn Python programming",
                    "Study statistics and probability",
                    "Master SQL for data querying",
                    "Learn data analysis with Pandas",
                    "Study machine learning fundamentals",
                    "Practice data visualization",
                    "Work on real-world datasets",
                    "Build a strong portfolio"
                ],
                "internship_advice": "Participate in Kaggle competitions and data science hackathons."
            },
            "devops_engineer": {
                "skills": ["linux", "docker", "aws", "kubernetes", "ci/cd", "git", "bash"],
                "learning_path": [
                    "Master Linux fundamentals",
                    "Learn bash scripting",
                    "Understand version control (Git)",
                    "Study containerization (Docker)",
                    "Learn cloud platforms (AWS/Azure)",
                    "Study CI/CD pipelines",
                    "Learn infrastructure as code",
                    "Master container orchestration (Kubernetes)"
                ],
                "internship_advice": "Set up your own homelab and practice deployments."
            }
        }

    def get_response(self, message: str, user_context: Dict[str, Any]) -> str:
        """Generate contextual response based on user query."""
        message_lower = message.lower()

        # Handle common question patterns
        if any(keyword in message_lower for keyword in ["what skills", "which skills", "skills need", "required skills"]):
            return self._get_skills_guidance(message, user_context)

        elif any(keyword in message_lower for keyword in ["learn", "learning path", "how to become", "roadmap"]):
            return self._get_learning_guidance(message, user_context)

        elif any(keyword in message_lower for keyword in ["internship", "job", "opportunity", "apply"]):
            return self._get_internship_guidance(message, user_context)

        elif any(keyword in message_lower for keyword in ["resume", "cv", "improve", "profile"]):
            return self._get_resume_guidance(message, user_context)

        elif any(keyword in message_lower for keyword in ["interview", "question", "prepare"]):
            return self._get_interview_guidance(message, user_context)

        elif any(keyword in message_lower for keyword in ["match", "score", "why low"]):
            return self._get_match_explanation(message, user_context)

        elif any(keyword in message_lower for keyword in ["missing", "gap", "what to learn"]):
            return self._get_skill_gap_guidance(message, user_context)

        else:
            return self._get_general_guidance(message, user_context)

    def _get_skills_guidance(self, message: str, user_context: Dict[str, Any]) -> str:
        """Provide guidance on required skills."""
        skills = user_context.get("skills", [])
        education = user_context.get("education", [])

        # Detect target role from message
        target_role = "python_developer"
        role_keywords = ["python", "web", "data", "devops", "mobile", "frontend", "backend"]

        for keyword in role_keywords:
            if keyword in message.lower():
                target_role = keyword + "_developer" if keyword != "data" else "data_scientist"
                break

        if target_role not in self.career_knowledge:
            target_role = "python_developer"
        role_info = self.career_knowledge[target_role]

        response = f"To become a {target_role.replace('_', ' ').title()}, you should focus on:\n\n"
        response += "Required Skills:\n"
        for skill in role_info["skills"][:7]:
            response += f"• {skill.title()}\n"

        if skills:
            matching_skills = [s for s in skills if any(s in rs.lower() for rs in role_info["skills"])]
            if matching_skills:
                response += f"\nGood news! You already have some relevant skills: {', '.join(matching_skills)}"

            missing_skills = [s for s in role_info["skills"] if s not in [us.lower() for us in skills]]
            if missing_skills:
                response += f"\n\nSkills you should learn:\n"
                for skill in missing_skills[:5]:
                    response += f"• {skill.title()}\n"

        return response

    def _get_learning_guidance(self, message: str, user_context: Dict[str, Any]) -> str:
        """Provide learning path guidance."""
        # Detect target role
        target_role = "python_developer"
        role_keywords = ["python", "web", "data", "devops", "frontend", "backend"]

        for keyword in role_keywords:
            if keyword in message.lower():
                target_role = keyword + "_developer" if keyword != "data" else "data_scientist"
                break

        if target_role not in self.career_knowledge:
            target_role = "python_developer"
        role_info = self.career_knowledge[target_role]

        response = f"Here's a learning path to become a {target_role.replace('_', ' ').title()}:\n\n"
        for i, step in enumerate(role_info["learning_path"][:8], 1):
            response += f"{i}. {step}\n"

        response += f"\n💡 {role_info['internship_advice']}"

        return response

    def _get_internship_guidance(self, message: str, user_context: Dict[str, Any]) -> str:
        """Provide internship application guidance."""
        skills = user_context.get("skills", [])
        projects = user_context.get("projects", [])

        response = "Here's how to find and apply for internships:\n\n"

        response += "1. Prepare Your Profile:\n"
        if not projects:
            response += "   • Build at least 2-3 projects\n"
            response += "   • Include GitHub links in your applications\n"
        else:
            response += f"   • Good! You have {len(projects)} projects\n"
            response += "   • Make sure they're well-documented\n"

        if not skills or len(skills) < 5:
            response += "\n2. Build Your Skills:\n"
            response += "   • Focus on in-demand technologies\n"
            response += "   • Complete online certifications\n"

        response += "\n3. Where to Find Internships:\n"
        response += "   • LinkedIn Jobs\n"
        response += "   • Company career pages\n"
        response += "   • Internshala\n"
        response += "   • AngelList\n"
        response += "   • GitHub Jobs\n"

        response += "\n4. Application Tips:\n"
        response += "   • Tailor your resume for each application\n"
        response += "   • Write a compelling cover letter\n"
        response += "   • Practice coding interviews\n"
        response += "   • Research the company thoroughly"

        return response

    def _get_resume_guidance(self, message: str, user_context: Dict[str, Any]) -> str:
        """Provide resume improvement guidance."""
        response = "Here are key tips to improve your resume:\n\n"

        response += "1. Format & Structure:\n"
        response += "   • Use clean, professional layout\n"
        response += "   • Limit resume to 1-2 pages\n"
        response += "   • Use consistent formatting\n"

        response += "\n2. Content:\n"
        response += "   • Start with a strong summary\n"
        response += "   • Quantify achievements (e.g., 'Improved performance by 40%')\n"
        response += "   • Use action verbs (developed, created, led)\n"

        response += "\n3. Technical Skills:\n"
        response += "   • List relevant technologies\n"
        response += "   • Organize by category (languages, frameworks, tools)\n"

        response += "\n4. Projects:\n"
        response += "   • Include 2-3 key projects\n"
        response += "   • Add GitHub and live demo links\n"
        response += "   • Describe your role and impact\n"

        response += "\n5. ATS Optimization:\n"
        response += "   • Use keywords from job descriptions\n"
        response += "   • Avoid images and graphics\n"
        response += "   • Use standard section headings"

        return response

    def _get_interview_guidance(self, message: str, user_context: Dict[str, Any]) -> str:
        """Provide interview preparation guidance."""
        response = "Here's how to prepare for technical interviews:\n\n"

        response += "1. Technical Preparation:\n"
        response += "   • Practice coding problems daily (LeetCode, HackerRank)\n"
        response += "   • Review data structures and algorithms\n"
        response += "   • Practice explaining your thought process\n"

        response += "\n2. Common Topics:\n"
        response += "   • Arrays and strings\n"
        response += "   • Linked lists and trees\n"
        response += "   • Sorting and searching algorithms\n"
        response += "   • Dynamic programming\n"

        response += "\n3. HR/Behavioral Questions:\n"
        response += "   • 'Tell me about yourself'\n"
        response += "   • 'Why do you want to work here?'\n"
        response += "   • 'Describe a challenging project'\n"

        response += "\n4. Practical Tips:\n"
        response += "   • Do mock interviews\n"
        response += "   • Prepare questions to ask the interviewer\n"
        response += "   • Get enough rest before the interview\n"

        response += "\n💡 Pro Tip: Use our Interview Preparation feature to practice with AI-generated questions!"

        return response

    def _get_match_explanation(self, message: str, user_context: Dict[str, Any]) -> str:
        """Explain match scores and how to improve them."""
        skills = user_context.get("skills", [])

        response = "Your match score is calculated based on:\n\n"

        response += "• Skill Match (35%): How well your skills match job requirements\n"
        response += "• Semantic Similarity (25%): How relevant your background is to the role\n"
        response += "• Education Match (10%): Degree and field of study\n"
        response += "• Experience Match (10%): Work/internship experience\n"
        response += "• Location Match (10%): Geographic preferences\n"
        response += "• Project Relevance (10%): How your projects relate to the job\n"

        response += "\n💡 To improve your score:\n"
        response += "1. Add more relevant skills to your profile\n"
        response += "2. Build projects using required technologies\n"
        response += "3. Complete certifications in your target domain\n"
        response += "4. Gain practical experience through internships\n"

        return response

    def _get_skill_gap_guidance(self, message: str, user_context: Dict[str, Any]) -> str:
        """Explain skill gaps and how to bridge them."""
        skills = user_context.get("skills", [])

        response = "To identify and close your skill gaps:\n\n"

        response += "1. Identify Target Role:\n"
        response += "   • Decide on your career direction\n"
        response += "   • Research job descriptions for desired roles\n"

        response += "\n2. Gap Analysis:\n"
        response += "   • Compare your skills to job requirements\n"
        response += "   • Identify missing skills\n"
        response += "   • Prioritize by importance\n"

        response += "\n3. Learning Strategy:\n"
        response += f"   • You currently have {len(skills)} skills listed\n"
        response += "   • Focus on 2-3 high-priority skills first\n"
        response += "   • Use our Career Roadmap feature for guided learning\n"

        response += "\n4. Resources:\n"
        response += "   • Online courses (Coursera, Udemy, edX)\n"
        response += "   • Official documentation\n"
        response += "   • Practice projects\n"
        response += "   • Open source contributions"

        return response

    def _get_general_guidance(self, message: str, user_context: Dict[str, Any]) -> str:
        """Handle general career questions."""
        return f"I can help with career-related questions! Ask me about:\n\n" \
               f"• Skills needed for specific roles\n" \
               f"• Learning paths and career roadmaps\n" \
               f"• Internship and job search tips\n" \
               f"• Resume and profile optimization\n" \
               f"• Interview preparation\n" \
               f"• Understanding match scores\n" \
               f"• Identifying skill gaps\n\n" \
               f"Just ask a specific question!"

    def provide_resume_feedback(self, skills: List[str], education: List, projects: List, experience: List) -> Dict[str, Any]:
        """Provide comprehensive resume feedback."""
        feedback = {
            "strengths": [],
            "improvements": [],
            "suggestions": []
        }

        # Analyze skills
        if len(skills) >= 5:
            feedback["strengths"].append(f"You have {len(skills)} skills listed, showing good technical breadth.")
        elif len(skills) >= 3:
            feedback["improvements"].append("Consider adding more technical skills to your profile.")

        # Analyze projects
        if len(projects) >= 3:
            feedback["strengths"].append("Your project portfolio demonstrates practical experience.")
        elif len(projects) >= 1:
            feedback["improvements"].append("Add more projects to showcase your abilities.")
        else:
            feedback["suggestions"].append("Building 2-3 quality projects should be your top priority.")

        # Analyze experience
        if experience:
            feedback["strengths"].append("Work experience section shows professional background.")
        else:
            feedback["suggestions"].append("Highlight any internships, part-time work, or volunteer experience.")

        # Analyze education
        if education:
            degree = education[0].get("degree", "")
            feedback["strengths"].append(f"Your {degree} provides a solid foundation.")

        # Provide suggestions
        feedback["suggestions"].append("Include GitHub links for all projects")
        feedback["suggestions"].append("Quantify achievements where possible")
        feedback["suggestions"].append("Tailor your resume for each application")

        return feedback

    def generate_resume_based_questions(self, projects: List[Dict], count: int = 5) -> List[str]:
        """Generate interview questions based on user projects."""
        questions = []

        for project in projects[:3]:
            if not isinstance(project, dict):
                continue

            title = project.get("title", "")
            description = project.get("description", "")
            technologies = project.get("technologies", "")

            # Generate questions based on project details
            questions.append(f"Tell me about your {title} project. What problem did you solve?")
            questions.append(f"What was your most challenging task in the {title} project?")

            if technologies:
                questions.append(f"You mentioned using {technologies}. Why did you choose these technologies for {title}?")

            if description and len(description) > 30:
                questions.append(f"You mentioned achieving results in {title}. Can you elaborate with specific metrics?")

        return questions[:count]
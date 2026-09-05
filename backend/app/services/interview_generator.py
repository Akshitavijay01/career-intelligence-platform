from typing import Dict, List, Any
import json

class InterviewGenerator:
    """Generates interview questions based on user profile and job requirements."""

    def __init__(self):
        # Question banks
        self.technical_questions = {
            "python": [
                "Explain the difference between lists and tuples in Python.",
                "What are Python decorators and how do they work?",
                "Explain the concept of list comprehensions in Python.",
                "What is the difference between .py and .pyc files?",
                "Explain Python's GIL (Global Interpreter Lock).",
                "How does Python handle memory management?",
                "What are generators and iterators in Python?",
                "Explain the difference between deep copy and shallow copy.",
                "What is the purpose of __init__ method in Python classes?",
                "How do you handle exceptions in Python?"
            ],
            "javascript": [
                "Explain the difference between let, const, and var.",
                "What is the event loop in JavaScript?",
                "Explain closures and provide an example.",
                "What is the difference between == and === in JavaScript?",
                "How does the 'this' keyword work in JavaScript?",
                "Explain Promise and async/await in JavaScript.",
                "What are arrow functions and how do they differ from regular functions?",
                "Explain the concept of hoisting in JavaScript.",
                "What is the DOM and how do you manipulate it?",
                "How do you handle asynchronous operations in JavaScript?"
            ],
            "react": [
                "What is the virtual DOM and how does it work?",
                "Explain the difference between controlled and uncontrolled components.",
                "What are React hooks and why are they used?",
                "Explain the useEffect hook and when to use it.",
                "What is the purpose of useState hook?",
                "Explain the concept of prop drilling and how to avoid it.",
                "What are Higher Order Components (HOCs)?",
                "How do you optimize React application performance?",
                "Explain the component lifecycle methods.",
                "What is the difference between class and functional components?"
            ],
            "sql": [
                "Explain the difference between INNER JOIN and LEFT JOIN.",
                "What are indexes and how do they improve query performance?",
                "Explain normalization and denormalization.",
                "What is a primary key and foreign key?",
                "Explain the ACID properties in databases.",
                "What is a subquery and how is it different from a JOIN?",
                "Explain the difference between WHERE and HAVING clauses.",
                "What are stored procedures and when to use them?",
                "How do you optimize SQL queries?",
                "Explain the concept of database transactions."
            ],
            "machine learning": [
                "Explain the difference between supervised and unsupervised learning.",
                "What is overfitting and how can it be prevented?",
                "Explain the bias-variance tradeoff.",
                "What are the main types of machine learning algorithms?",
                "Explain the difference between classification and regression.",
                "What is cross-validation and why is it important?",
                "Explain the working of linear regression.",
                "What is gradient descent and how does it work?",
                "Explain the difference between bagging and boosting.",
                "What are feature engineering and feature selection?"
            ]
        }

        self.hr_questions = [
            "Tell me about yourself and your background.",
            "Why are you interested in this position?",
            "What are your strengths and weaknesses?",
            "Where do you see yourself in 5 years?",
            "Why should we hire you for this role?",
            "Tell me about a challenging project you worked on.",
            "How do you handle conflicts with team members?",
            "What are your salary expectations?",
            "Describe a situation where you demonstrated leadership.",
            "How do you prioritize tasks when managing multiple deadlines?"
        ]

        self.general_technical = [
            "Explain REST APIs and their HTTP methods.",
            "What is the difference between SQL and NoSQL databases?",
            "Explain the concept of version control with Git.",
            "What are microservices architecture and its benefits?",
            "Explain the difference between synchronous and asynchronous programming.",
            "What is Docker and why is it used?",
            "Explain the concept of CI/CD pipelines.",
            "What is cloud computing and name some cloud providers?",
            "Explain the difference between stack and queue data structures.",
            "What are design patterns and name a few you use frequently?"
        ]

    def generate_questions(self, difficulty: str, interview_type: str,
                          skills: List[str], projects: List[Dict],
                          count: int = 10) -> List[Dict[str, str]]:
        """Generate interview questions based on user profile."""
        questions = []

        # Determine difficulty multiplier
        difficulty_map = {
            "easy": 0.8,
            "medium": 1.0,
            "hard": 1.2
        }
        difficulty_factor = difficulty_map.get(difficulty, 1.0)

        # Generate technical questions
        tech_questions = []
        if "technical" in interview_type or "mixed" in interview_type:
            # Generate skill-specific questions
            for skill in skills[:5]:  # Top 5 skills
                skill_lower = skill.lower()
                for tech_key, tech_questions_list in self.technical_questions.items():
                    if tech_key in skill_lower:
                        tech_questions.extend(tech_questions_list[:2])

            # Add general technical questions
            if len(tech_questions) < count * 0.6:
                tech_questions.extend(self.general_technical[:5])

            # Limit and shuffle
            tech_questions = tech_questions[:int(count * 0.6)]

            for q in tech_questions:
                questions.append({
                    "question": q,
                    "type": "technical",
                    "difficulty": difficulty
                })

        # Generate HR questions
        if "hr" in interview_type or "mixed" in interview_type:
            hr_needed = max(1, int(count * 0.2))
            hr_questions = self.hr_questions[:hr_needed]
            for q in hr_questions:
                questions.append({
                    "question": q,
                    "type": "hr",
                    "difficulty": "easy"
                })

        # Generate resume-based questions
        if "technical" in interview_type or "mixed" in interview_type:
            resume_questions = self._generate_resume_based_questions(projects, count)
            questions.extend(resume_questions[:int(count * 0.2)])

        # Shuffle and return
        import random
        random.shuffle(questions)
        return questions[:count]

    def _generate_resume_based_questions(self, projects: List[Dict], count: int) -> List[Dict[str, str]]:
        """Generate questions based on user's projects."""
        questions = []

        for project in projects[:3]:  # Top 3 projects
            if not isinstance(project, dict):
                continue

            title = project.get("title", "")
            description = project.get("description", "")
            technologies = project.get("technologies", "")

            # Generate questions based on project details
            questions.append({
                "question": f"Tell me about your {title} project. What was the problem you were solving?",
                "type": "resume-based",
                "difficulty": "medium"
            })

            if technologies:
                tech_list = technologies.split(", ") if isinstance(technologies, str) else technologies
                if len(tech_list) >= 2:
                    questions.append({
                        "question": f"In your {title} project, you used {tech_list[0]} and {tech_list[1]}. Why did you choose these technologies?",
                        "type": "resume-based",
                        "difficulty": "medium"
                    })

            if description and len(description) > 30:
                questions.append({
                    "question": f"You mentioned achieving results in your {title} project. Can you elaborate on the measurable outcomes?",
                    "type": "resume-based",
                    "difficulty": "hard"
                })

            questions.append({
                "question": f"What challenges did you face while working on the {title} project and how did you overcome them?",
                "type": "resume-based",
                "difficulty": "medium"
            })

        return questions

    def evaluate_answer(self, question: str, answer: str, question_type: str) -> Dict[str, Any]:
        """Evaluate user's answer and provide feedback."""
        answer_lower = answer.lower()

        # Basic keyword-based evaluation
        if len(answer) < 20:
            return {
                "score": 20,
                "feedback": "Your answer is too short. Please provide more detailed response."
            }

        if question_type == "hr":
            # Evaluate HR questions based on structure and clarity
            feedback_points = []
            if "i" in answer_lower or "me" in answer_lower:
                feedback_points.append("Good use of first-person narrative")
            if any(word in answer_lower for word in ["because", "reason", "why"]):
                feedback_points.append("Good explanation of reasoning")
            if any(word in answer_lower for word in ["example", "instance", "time"]):
                feedback_points.append("Good use of examples")

            if len(feedback_points) >= 2:
                return {
                    "score": 80,
                    "feedback": f"Well-structured answer. {' '.join(feedback_points)}"
                }
            elif len(feedback_points) >= 1:
                return {
                    "score": 60,
                    "feedback": "Adequate answer. Consider adding more specific examples."
                }
            else:
                return {
                    "score": 40,
                    "feedback": "Try to include specific examples and explain your reasoning."
                }

        else:
            # Evaluate technical questions
            technical_keywords = ["explain", "describe", "what", "how", "why", "difference"]
            has_technical_content = any(keyword in answer_lower for keyword in technical_keywords)

            if has_technical_content:
                if len(answer) > 100:
                    return {
                        "score": 85,
                        "feedback": "Excellent! Your answer is detailed and demonstrates good understanding."
                    }
                elif len(answer) > 50:
                    return {
                        "score": 70,
                        "feedback": "Good answer. You covered the main points well."
                    }
                else:
                    return {
                        "score": 55,
                        "feedback": "You have the right idea. Add more details to strengthen your answer."
                    }
            else:
                return {
                    "score": 35,
                    "feedback": "Try to explain the concepts more clearly. Use specific examples."
                }

    def get_technical_questions_for_skill(self, skill: str, count: int = 5) -> List[str]:
        """Get technical questions for a specific skill."""
        skill_lower = skill.lower()

        for tech_key, questions in self.technical_questions.items():
            if tech_key in skill_lower:
                return questions[:count]

        return self.general_technical[:count]

    def get_behavioral_questions(self, count: int = 5) -> List[str]:
        """Get behavioral/HR questions."""
        return self.hr_questions[:count]
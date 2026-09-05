from typing import Dict, List, Any
import re

class MatchingEngine:
    """AI-powered job matching engine using hybrid algorithm."""

    def __init__(self):
        # Role-based skill mapping
        self.role_skill_map = {
            "software_developer": {
                "required": ["python", "javascript", "sql", "git"],
                "preferred": ["docker", "aws", "react", "node", "postgresql"]
            },
            "full_stack_developer": {
                "required": ["javascript", "html", "css", "react", "node"],
                "preferred": ["python", "sql", "docker", "aws", "mongodb"]
            },
            "data_scientist": {
                "required": ["python", "sql", "machine learning"],
                "preferred": ["tensorflow", "pandas", "statistics", "data visualization"]
            },
            "frontend_developer": {
                "required": ["html", "css", "javascript", "react"],
                "preferred": ["typescript", "vue", "angular", "figma"]
            },
            "backend_developer": {
                "required": ["python", "sql", "api"],
                "preferred": ["django", "flask", "postgresql", "docker", "aws"]
            },
            "devops_engineer": {
                "required": ["docker", "linux", "aws"],
                "preferred": ["kubernetes", "jenkins", "terraform", "azure"]
            },
            "machine_learning_engineer": {
                "required": ["python", "machine learning", "tensorflow"],
                "preferred": ["pytorch", "scikit-learn", "docker", "aws"]
            }
        }

    def calculate_match(self, user_data: Dict[str, Any], opportunity: Any) -> Dict[str, float]:
        """Calculate match score between user and job opportunity."""
        scores = {
            "overall_score": 0,
            "skill_match": 0,
            "semantic_similarity": 0,
            "education_match": 0,
            "experience_match": 0,
            "location_match": 0,
            "project_relevance": 0,
            "matched_skills": [],
            "missing_skills": []
        }

        user_skills = [s.lower() for s in user_data.get("skills", [])]

        # Extract required skills from opportunity
        required_skills = []
        preferred_skills = []

        if hasattr(opportunity, 'skills'):
            for opp_skill in opportunity.skills:
                skill_name = opp_skill.skill.name.lower() if hasattr(opp_skill, 'skill') else str(opp_skill).lower()
                if opp_skill.is_required:
                    required_skills.append(skill_name)
                else:
                    preferred_skills.append(skill_name)

        # Skill matching (35% weight)
        skill_match_score = self._calculate_skill_match(user_skills, required_skills, preferred_skills)
        scores["skill_match"] = skill_match_score["score"]
        scores["matched_skills"] = skill_match_score["matched"]
        scores["missing_skills"] = skill_match_score["missing"]

        # Semantic similarity (25% weight)
        similarity_score = self._calculate_semantic_similarity(user_data, opportunity)
        scores["semantic_similarity"] = similarity_score

        # Education matching (10% weight)
        education_score = self._calculate_education_match(
            user_data.get("education", []),
            opportunity.education_requirements if hasattr(opportunity, 'education_requirements') else ""
        )
        scores["education_match"] = education_score

        # Experience matching (10% weight)
        experience_score = self._calculate_experience_match(
            user_data.get("experience", []),
            opportunity.experience_requirements if hasattr(opportunity, 'experience_requirements') else ""
        )
        scores["experience_match"] = experience_score

        # Location matching (10% weight)
        location_score = self._calculate_location_match(
            user_data.get("location", ""),
            opportunity.location if hasattr(opportunity, 'location') else "",
            opportunity.work_type if hasattr(opportunity, 'work_type') else ""
        )
        scores["location_match"] = location_score

        # Project relevance (10% weight)
        project_score = self._calculate_project_relevance(
            user_data.get("projects", []),
            opportunity.description if hasattr(opportunity, 'description') else ""
        )
        scores["project_relevance"] = project_score

        # Calculate weighted overall score
        scores["overall_score"] = round(
            (scores["skill_match"] * 0.35) +
            (scores["semantic_similarity"] * 0.25) +
            (scores["education_match"] * 0.10) +
            (scores["experience_match"] * 0.10) +
            (scores["location_match"] * 0.10) +
            (scores["project_relevance"] * 0.10)
        )

        return scores

    def _calculate_skill_match(self, user_skills: List[str], required: List[str], preferred: List[str]) -> Dict:
        """Calculate skill matching score."""
        score = 0
        matched = []
        missing = []

        # Check required skills
        required_match_count = 0
        for req_skill in required:
            if any(req_skill in user_skill for user_skill in user_skills):
                required_match_count += 1
                matched.append(req_skill)
            else:
                missing.append(req_skill)

        # Required skills weighted more heavily
        if required:
            required_score = (required_match_count / len(required)) * 100
            score += required_score * 0.7

        # Check preferred skills
        preferred_match_count = 0
        for pref_skill in preferred:
            if any(pref_skill in user_skill for user_skill in user_skills):
                preferred_match_count += 1
                matched.append(pref_skill)

        if preferred:
            preferred_score = (preferred_match_count / len(preferred)) * 100
            score += preferred_score * 0.3

        return {"score": min(score, 100), "matched": matched, "missing": missing}

    def _calculate_semantic_similarity(self, user_data: Dict[str, Any], opportunity: Any) -> float:
        """Calculate semantic similarity between user profile and job description."""
        # Simple keyword-based similarity
        job_description = (opportunity.description if hasattr(opportunity, 'description') else "").lower()
        job_title = (opportunity.title if hasattr(opportunity, 'title') else "").lower()

        job_text = job_title + " " + job_description

        # Create user profile text
        user_text_parts = []

        # Add skills
        user_text_parts.extend(user_data.get("skills", []))

        # Add project titles and technologies
        for project in user_data.get("projects", []):
            if isinstance(project, dict):
                user_text_parts.append(project.get("title", ""))
                user_text_parts.extend(project.get("technologies", []))
            else:
                user_text_parts.append(str(project))

        # Add experience roles
        for exp in user_data.get("experience", []):
            if isinstance(exp, dict):
                user_text_parts.append(exp.get("role", ""))
                user_text_parts.append(exp.get("company", ""))

        # Calculate overlap
        user_text = " ".join(str(p).lower() for p in user_text_parts)

        # Simple word matching
        job_words = set(re.findall(r'\b\w+\b', job_text))
        user_words = set(re.findall(r'\b\w+\b', user_text))

        # Remove common words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'my', 'your', 'his', 'her', 'its', 'our', 'their'}
        job_words = job_words - stop_words
        user_words = user_words - stop_words

        if not job_words:
            return 50

        intersection = job_words.intersection(user_words)
        similarity = (len(intersection) / len(job_words)) * 100

        return min(similarity * 1.5, 100)  # Scale up slightly

    def _calculate_education_match(self, education: List[Dict], requirements: str) -> float:
        """Calculate education match score."""
        if not requirements:
            return 80  # No specific requirements

        requirements_lower = requirements.lower()

        # Check degree requirements
        degree_keywords = {
            "bachelor": ["bca", "btech", "be", "bsc", "b.com"],
            "master": ["mca", "mtech", "me", "msc", "m.com"],
            "phd": ["phd", "doctorate"]
        }

        required_level = None
        for level, keywords in degree_keywords.items():
            if any(keyword in requirements_lower for keyword in keywords):
                required_level = level
                break

        if not required_level:
            return 80

        # Check user's education
        user_degrees = []
        for edu in education:
            degree = edu.get("degree", "").lower()
            user_degrees.append(degree)

        # Match degree level
        level_map = {"bachelor": 1, "master": 2, "phd": 3}
        required_level_value = level_map.get(required_level, 1)

        for user_degree in user_degrees:
            for level, keywords in degree_keywords.items():
                if any(keyword in user_degree for keyword in keywords):
                    user_level_value = level_map.get(level, 1)
                    if user_level_value >= required_level_value:
                        return 100

        return 50  # Education doesn't meet requirements

    def _calculate_experience_match(self, experience: List[Dict], requirements: str) -> float:
        """Calculate experience match score."""
        if not requirements:
            return 80

        requirements_lower = requirements.lower()

        # Extract years of experience required
        year_match = re.search(r'(\d+)\+?\s*(?:years?|yrs?)?\s*(?:of)?\s*experience', requirements_lower)
        years_required = int(year_match.group(1)) if year_match else 1

        # Calculate user's total experience
        total_years = 0
        for exp in experience:
            duration = exp.get("duration", "")
            # Try to extract years from duration
            duration_lower = duration.lower()
            if "year" in duration_lower:
                year_num = re.search(r'(\d+)\+?\s*year', duration_lower)
                if year_num:
                    total_years += int(year_num.group(1))
            elif "month" in duration_lower:
                month_num = re.search(r'(\d+)\+?\s*month', duration_lower)
                if month_num:
                    total_years += int(month_num.group(1)) / 12
            else:
                total_years += 0.5  # Assume 6 months if unclear

        # Calculate match percentage
        if total_years >= years_required:
            return 100
        elif total_years >= years_required * 0.5:
            return 70
        elif total_years > 0:
            return 40
        else:
            return 20

    def _calculate_location_match(self, user_location: str, job_location: str, work_type: str) -> float:
        """Calculate location match score."""
        # Check work type first
        if work_type and work_type.lower() == "remote":
            return 100

        if not job_location:
            return 80

        if not user_location:
            return 60  # User hasn't specified location

        user_location_lower = user_location.lower()
        job_location_lower = job_location.lower()

        # Exact match
        if user_location_lower == job_location_lower:
            return 100

        # Partial match (e.g., "Bangalore" in "Bangalore, Karnataka")
        if user_location_lower in job_location_lower or job_location_lower in user_location_lower:
            return 90

        # Common cities check
        common_cities = ["bangalore", "bengaluru", "delhi", "mumbai", "hyderabad", "chennai", "pune", "kolkata"]
        user_city = next((city for city in common_cities if city in user_location_lower), None)
        job_city = next((city for city in common_cities if city in job_location_lower), None)

        if user_city and job_city and user_city == job_city:
            return 85

        return 50

    def _calculate_project_relevance(self, projects: List[Dict], job_description: str) -> float:
        """Calculate project relevance score."""
        if not projects or not job_description:
            return 50

        job_keywords = set(re.findall(r'\b\w+\b', job_description.lower()))

        relevant_count = 0
        for project in projects:
            if isinstance(project, dict):
                techs = project.get("technologies", "")
                if isinstance(techs, list):
                    techs = ", ".join(techs)
                project_text = project.get("title", "") + " " + project.get("description", "") + " " + techs
            else:
                project_text = str(project)

            project_words = set(re.findall(r'\b\w+\b', project_text.lower()))

            # Check overlap
            overlap = job_keywords.intersection(project_words)
            if len(overlap) >= 3:
                relevant_count += 1

        if not projects:
            return 50

        relevance = (relevant_count / len(projects)) * 100
        return min(relevance, 100)

    def generate_explanation(self, user_data: Dict[str, Any], opportunity: Any, match_result: Dict) -> str:
        """Generate human-readable explanation for the match."""
        lines = []

        # Overall score
        lines.append(f"Overall Match: {match_result['overall_score']}%")

        # Skill match details
        matched_skills = match_result.get("matched_skills", [])
        missing_skills = match_result.get("missing_skills", [])

        if matched_skills:
            lines.append(f"✓ You match: {', '.join(matched_skills[:5])}")

        if missing_skills:
            lines.append(f"✗ Skills you are missing: {', '.join(missing_skills[:5])}")

        # Breakdown
        lines.append("\nBreakdown:")
        lines.append(f"  Skills: {match_result['skill_match']}%")
        lines.append(f"  Semantic Similarity: {match_result['semantic_similarity']}%")
        lines.append(f"  Education: {match_result['education_match']}%")
        lines.append(f"  Experience: {match_result['experience_match']}%")
        lines.append(f"  Location: {match_result['location_match']}%")
        lines.append(f"  Projects: {match_result['project_relevance']}%")

        # Recommendation
        if missing_skills:
            lines.append(f"\nRecommended action: Learn {missing_skills[0]} to improve your match score.")

        return "\n".join(lines)
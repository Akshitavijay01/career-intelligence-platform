from typing import Dict, List, Any

class CareerScoreCalculator:
    """Calculates comprehensive career readiness scores."""

    def __init__(self):
        self.weights = {
            "technical_skills": 0.25,
            "projects": 0.15,
            "resume": 0.20,
            "certifications": 0.10,
            "experience": 0.15,
            "interview_readiness": 0.15
        }

    async def calculate_score(self, user_id: int, db) -> Dict[str, Any]:
        """Calculate overall career readiness score."""
        from app.models.user import UserSkill, Skill, Project, Certification, Experience
        from app.models.resume import Resume
        from app.models.application import Application
        from app.models.interview import InterviewSession
        from app.models.recommendation import CareerScore

        # Calculate individual component scores
        technical_skills_score = await self._calculate_technical_skills_score(user_id, db)
        projects_score = self._calculate_projects_score(user_id, db)
        resume_score = self._calculate_resume_score(user_id, db)
        certifications_score = self._calculate_certifications_score(user_id, db)
        experience_score = self._calculate_experience_score(user_id, db)
        interview_readiness_score = self._calculate_interview_readiness(user_id, db)

        # Calculate weighted overall score
        overall_score = round(
            (technical_skills_score * self.weights["technical_skills"]) +
            (projects_score * self.weights["projects"]) +
            (resume_score * self.weights["resume"]) +
            (certifications_score * self.weights["certifications"]) +
            (experience_score * self.weights["experience"]) +
            (interview_readiness_score * self.weights["interview_readiness"])
        )

        return {
            "technical_skills_score": technical_skills_score,
            "projects_score": projects_score,
            "resume_score": resume_score,
            "certifications_score": certifications_score,
            "experience_score": experience_score,
            "interview_readiness_score": interview_readiness_score,
            "overall_score": overall_score
        }

    async def _calculate_technical_skills_score(self, user_id: str, db) -> float:
        """Calculate technical skills score based on skills diversity and level."""
        from app.models.user import UserSkill, Skill

        user_skills = db.query(UserSkill).filter(UserSkill.user_id == user_id).all()

        if not user_skills:
            return 0

        # Score based on number of skills
        num_skills = len(user_skills)
        if num_skills >= 15:
            skill_count_score = 30
        elif num_skills >= 10:
            skill_count_score = 25
        elif num_skills >= 5:
            skill_count_score = 20
        elif num_skills >= 3:
            skill_count_score = 15
        else:
            skill_count_score = 10

        # Score based on proficiency levels
        proficiency_scores = {
            "beginner": 1,
            "intermediate": 2,
            "advanced": 3,
            "expert": 4
        }

        proficiency_sum = sum(
            proficiency_scores.get(us.proficiency_level, 1)
            for us in user_skills
        )
        avg_proficiency = proficiency_sum / num_skills
        proficiency_score = (avg_proficiency / 4) * 30  # Scale to max 30 points

        # Score based on skill diversity
        categories_covered = set()
        for us in user_skills:
            skill = db.query(Skill).filter(Skill.id == us.skill_id).first()
            if skill and skill.category:
                categories_covered.add(skill.category)

        if len(categories_covered) >= 5:
            diversity_score = 40
        elif len(categories_covered) >= 3:
            diversity_score = 30
        elif len(categories_covered) >= 2:
            diversity_score = 20
        else:
            diversity_score = 10

        return min(skill_count_score + proficiency_score + diversity_score, 100)

    def _calculate_projects_score(self, user_id: str, db) -> float:
        """Calculate projects score based on quality and quantity."""
        from app.models.user import Project

        projects = db.query(Project).filter(Project.user_id == user_id).all()

        if not projects:
            return 0

        # Score based on number of projects
        num_projects = len(projects)
        if num_projects >= 5:
            project_count_score = 30
        elif num_projects >= 3:
            project_count_score = 25
        elif num_projects >= 2:
            project_count_score = 20
        else:
            project_count_score = 15

        # Score based on project completeness
        completeness_scores = []
        for project in projects:
            score = 0
            if project.description and len(project.description) > 50:
                score += 10
            if project.technologies:
                score += 5
            if project.github_url:
                score += 5
            if project.live_url:
                score += 5
            if project.role:
                score += 5
            completeness_scores.append(min(score, 30))

        avg_completeness = sum(completeness_scores) / len(completeness_scores) if completeness_scores else 0

        return min(project_count_score + avg_completeness, 100)

    def _calculate_resume_score(self, user_id: str, db) -> float:
        """Calculate resume score."""
        from app.models.resume import Resume
        from app.models.resume import ResumeAnalysis

        # Get latest resume
        resume = db.query(Resume).filter(Resume.user_id == user_id).order_by(Resume.uploaded_at.desc()).first()

        if not resume:
            return 0

        # Get latest analysis
        analysis = db.query(ResumeAnalysis).filter(
            ResumeAnalysis.resume_id == resume.id
        ).order_by(ResumeAnalysis.created_at.desc()).first()

        if not analysis:
            return 50  # Resume exists but not analyzed yet

        return analysis.overall_score

    def _calculate_certifications_score(self, user_id: str, db) -> float:
        """Calculate certifications score."""
        from app.models.user import Certification

        certifications = db.query(Certification).filter(Certification.user_id == user_id).all()

        if not certifications:
            return 0

        # Score based on number of certifications
        num_certs = len(certifications)
        if num_certs >= 5:
            cert_count_score = 50
        elif num_certs >= 3:
            cert_count_score = 40
        elif num_certs >= 2:
            cert_count_score = 30
        else:
            cert_count_score = 20

        # Bonus for recognized certifications
        recognized_certifications = [
            "aws", "azure", "google cloud", "oracle", "microsoft",
            "cisco", "comptia", "pmp", "agile", "scrum"
        ]

        bonus_points = 0
        for cert in certifications:
            cert_lower = cert.certificate_name.lower()
            for recognized in recognized_certifications:
                if recognized in cert_lower:
                    bonus_points += 10
                    break

        return min(cert_count_score + bonus_points, 100)

    def _calculate_experience_score(self, user_id: str, db) -> float:
        """Calculate experience score."""
        from app.models.user import Experience

        experiences = db.query(Experience).filter(Experience.user_id == user_id).all()

        if not experiences:
            return 0

        # Score based on number of experiences
        num_exp = len(experiences)
        if num_exp >= 4:
            exp_count_score = 40
        elif num_exp >= 2:
            exp_count_score = 30
        else:
            exp_count_score = 20

        # Score based on experience quality
        quality_score = 0
        for exp in experiences:
            if exp.description and len(exp.description) > 50:
                quality_score += 15
            if exp.duration:
                quality_score += 10
            if exp.role and "intern" not in exp.role.lower() and "trainee" not in exp.role.lower():
                quality_score += 10

        return min(exp_count_score + quality_score, 100)

    def _calculate_interview_readiness(self, user_id: str, db) -> float:
        """Calculate interview readiness score based on practice history."""
        from app.models.interview import InterviewSession

        # Get interview sessions
        sessions = db.query(InterviewSession).filter(
            InterviewSession.user_id == user_id
        ).all()

        if not sessions:
            return 30  # No practice yet

        # Score based on number of sessions
        num_sessions = len(sessions)
        if num_sessions >= 5:
            session_score = 30
        elif num_sessions >= 3:
            session_score = 25
        elif num_sessions >= 1:
            session_score = 20
        else:
            session_score = 15

        # Score based on performance
        completed_sessions = [s for s in sessions if s.overall_score is not None]
        if completed_sessions:
            avg_score = sum(s.overall_score for s in completed_sessions) / len(completed_sessions)
            performance_score = avg_score
        else:
            performance_score = 30  # Completed sessions but no score yet

        # Bonus for different interview types
        session_types = set(s.interview_type.value for s in sessions)
        type_bonus = min(len(session_types) * 5, 20)

        return min(session_score + performance_score + type_bonus, 100)
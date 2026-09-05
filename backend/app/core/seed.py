from sqlalchemy.orm import Session
from app.models.user import User, UserProfile, Skill, Education, Project, UserSkill
from app.models.opportunity import Opportunity, OpportunitySkill
from app.core.security import hash_password

def seed_database(db: Session):
    # 1. Create Demo User
    demo_user = db.query(User).filter(User.email == "demo@careerai.com").first()
    if not demo_user:
        demo_user = User(
            email="demo@careerai.com",
            password_hash=hash_password("demo123"),
            role="student",
            is_active=True
        )
        db.add(demo_user)
        db.commit()
        db.refresh(demo_user)

        # Create Demo Profile
        profile = UserProfile(
            user_id=demo_user.id,
            first_name="Alex",
            last_name="Jordan",
            location="Bangalore, India"
        )
        db.add(profile)
        db.commit()

        # Create Demo Skills
        skills_data = ["python", "javascript", "react", "fastapi", "sql", "git"]
        skill_objs = []
        for name in skills_data:
            skill = db.query(Skill).filter(Skill.name == name).first()
            if not skill:
                skill = Skill(name=name, category="technical")
                db.add(skill)
                db.flush()
            skill_objs.append(skill)

        # Link skills to the demo user so recommendations populate
        for skill in skill_objs:
            if not db.query(UserSkill).filter(UserSkill.user_id == demo_user.id, UserSkill.skill_id == skill.id).first():
                db.add(UserSkill(
                    user_id=demo_user.id,
                    skill_id=skill.id,
                    proficiency_level="advanced"
                ))

        db.commit()

        # Create Demo Education
        edu = Education(
            user_id=demo_user.id,
            degree="B.Tech Computer Science",
            university="Anna University"
        )
        db.add(edu)
        db.commit()

    # Backfill: link existing demo user's skills if not already linked (handles pre-fix DBs)
    existing_demo = db.query(User).filter(User.email == "demo@careerai.com").first()
    if existing_demo:
        for name in ["python", "javascript", "react", "fastapi", "sql", "git"]:
            skill = db.query(Skill).filter(Skill.name == name).first()
            if skill and not db.query(UserSkill).filter(UserSkill.user_id == existing_demo.id, UserSkill.skill_id == skill.id).first():
                db.add(UserSkill(user_id=existing_demo.id, skill_id=skill.id, proficiency_level="advanced"))
        db.commit()

    # 1b. Create Admin User
    admin_user = db.query(User).filter(User.email == "admin@careerai.com").first()
    if not admin_user:
        admin_user = User(
            email="admin@careerai.com",
            password_hash=hash_password("admin123"),
            role="admin",
            is_active=True
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)

        admin_profile = UserProfile(
            user_id=admin_user.id,
            first_name="Admin",
            last_name="User",
            location="Bangalore, India"
        )
        db.add(admin_profile)
        db.commit()

    # 2. Create Sample Opportunities
    if db.query(Opportunity).count() == 0:
        opportunities = [
            {"title": "Software Engineering Intern", "company": "Google", "location": "Hyderabad", "description": "Work on core Google products."},
            {"title": "Frontend Developer", "company": "Microsoft", "location": "Remote", "description": "Build modern web apps with React."},
            {"title": "ML Engineer", "company": "Amazon", "location": "Bangalore", "description": "Develop machine learning models at scale."},
            {"title": "Data Analyst", "company": "Netflix", "location": "Mumbai", "description": "Analyze viewer data to drive decisions."},
            {"title": "Backend Developer", "company": "Stripe", "location": "Remote", "description": "Build robust payment infrastructure."}
        ]
        for opp in opportunities:
            db_opportunity = Opportunity(**opp, status="active", employment_type="internship", work_type="hybrid")
            db.add(db_opportunity)

        db.commit()

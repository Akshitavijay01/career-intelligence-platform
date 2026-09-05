import sys
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, '.')

from app.core.database import SessionLocal
from app.models.user import User, UserProfile, Skill, UserSkill, Education, Experience, Project
from app.models.opportunity import Opportunity, OpportunitySkill
from app.services.matching_engine import MatchingEngine
import json as _json

db = SessionLocal()

# Check user profile
user = db.query(User).filter(User.email == 'demo@careerai.com').first()
print(f'User: {user.id} {user.email}')

profile = db.query(UserProfile).filter(UserProfile.user_id == user.id).first()
if profile:
    print(f'Profile: {profile.first_name} {profile.last_name}')
else:
    print('Profile: NONE - THIS IS THE BUG')

# Check opportunity skills
opps = db.query(Opportunity).filter(Opportunity.status == 'active').all()
print(f'Active opportunities: {len(opps)}')
for opp in opps:
    try:
        skills = opp.skills if hasattr(opp, 'skills') else []
        print(f'  Opp {opp.id}: {opp.title} - {len(skills)} skills')
        for s in skills[:2]:
            print(f'    skill_id={s.skill_id} name={s.skill.name if hasattr(s, "skill") and s.skill else "?"}')
    except Exception as e:
        print(f'  Opp {opp.id}: ERROR reading skills: {e}')

# Get user skill names
user_skills = db.query(UserSkill).filter(UserSkill.user_id == user.id).all()
skill_names = []
for us in user_skills:
    skill = db.query(Skill).filter(Skill.id == us.skill_id).first()
    if skill:
        skill_names.append(skill.name)
print(f'User skills: {skill_names}')

# Build user_data
user_data = {
    'skills': skill_names,
    'education': [],
    'experience': [],
    'projects': []
}

# Test matching engine
engine = MatchingEngine()
opp = opps[0]
try:
    result = engine.calculate_match(user_data, opp)
    print(f'Match score: {result["overall_score"]}')
except Exception as e:
    print(f'ERROR in calculate_match: {e}')
    import traceback
    traceback.print_exc()

# Test the full flow that recommendations endpoint does
print('\n--- Full recommendations flow ---')
if profile:
    education = db.query(Education).filter(Education.user_id == user.id).all()
    experience = db.query(Experience).filter(Experience.user_id == user.id).all()
    projects = db.query(Project).filter(Project.user_id == user.id).all()
    print(f'Education: {len(education)}')
    print(f'Experience: {len(experience)}')
    print(f'Projects: {len(projects)}')

    user_data_full = {
        'skills': skill_names,
        'education': [{"degree": e.degree, "college": e.college, "university": e.university, "graduation_year": e.graduation_year} for e in education],
        'experience': [{"company": exp.company, "role": exp.role, "duration": exp.duration} for exp in experience],
        'projects': [{"title": proj.title, "technologies": proj.technologies.split(", ") if proj.technologies else [], "description": proj.description} for proj in projects]
    }
    print(f'User data: {user_data_full}')

    for opp in opps[:2]:
        try:
            match_result = engine.calculate_match(user_data_full, opp)
            serialized = {
                k: (_json.dumps(v) if k in ("matched_skills", "missing_skills") and isinstance(v, list) else v)
                for k, v in match_result.items()
            }
            explanation = engine.generate_explanation(user_data_full, opp, match_result)
            print(f'Opp {opp.id} score: {match_result["overall_score"]}')
            print(f'  explanation: {explanation[:100]}...')
        except Exception as e:
            print(f'Opp {opp.id} ERROR: {e}')
            import traceback
            traceback.print_exc()
else:
    print('Cannot test full flow - no profile')

db.close()
print('DONE')

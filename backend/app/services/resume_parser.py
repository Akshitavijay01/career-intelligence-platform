import fitz  # PyMuPDF
from docx import Document
import re
import json
from typing import Dict, List, Any

class ResumeParser:
    def __init__(self):
        self.section_keywords = {
            "education": ["education", "academic", "degree", "university", "college", "school"],
            "experience": ["experience", "work", "employment", "professional", "career"],
            "skills": ["skills", "technical skills", "programming languages", "languages", "frameworks"],
            "projects": ["projects", "personal projects", "academic projects"],
            "certifications": ["certifications", "certificate", "courses"],
            "achievements": ["achievements", "awards", "honors", "recognition"]
        }

    def parse_resume(self, file_path: str, file_type: str) -> Dict[str, Any]:
        """Parse resume file and extract structured data."""
        text = self._extract_text(file_path, file_type)
        sections = self._identify_sections(text)

        extracted_data = {
            "personal_info": self._extract_personal_info(text),
            "education": self._extract_education(sections.get("education", "")),
            "experience": self._extract_experience(sections.get("experience", "")),
            "skills": self._extract_skills(sections.get("skills", "")),
            "projects": self._extract_projects(sections.get("projects", "")),
            "certifications": self._extract_certifications(sections.get("certifications", ""))
        }

        return extracted_data

    def _extract_text(self, file_path: str, file_type: str) -> str:
        """Extract text from PDF or DOCX file."""
        text = ""

        if file_type.lower() == "pdf":
            try:
                with fitz.open(file_path) as doc:
                    for page in doc:
                        text += page.get_text()
            except Exception as e:
                raise Exception(f"Error reading PDF: {str(e)}")

        elif file_type.lower() in ["doc", "docx"]:
            try:
                doc = Document(file_path)
                for paragraph in doc.paragraphs:
                    text += paragraph.text + "\n"
            except Exception as e:
                raise Exception(f"Error reading DOCX: {str(e)}")

        return text

    def _identify_sections(self, text: str) -> Dict[str, str]:
        """Identify and separate resume sections."""
        lines = text.split('\n')
        sections = {}
        current_section = None
        current_content = []

        for i, line in enumerate(lines):
            line_lower = line.strip().lower()
            section_found = False

            # Check if line is a section header
            for section, keywords in self.section_keywords.items():
                for keyword in keywords:
                    if keyword in line_lower and len(line_lower.split()) <= 4:
                        # Start new section
                        if current_section:
                            sections[current_section] = "\n".join(current_content).strip()
                        current_section = section
                        current_content = []
                        section_found = True
                        break
                if section_found:
                    break

            if not section_found and line.strip():
                if current_section:
                    current_content.append(line)
                elif not any(keyword in line_lower for keywords in self.section_keywords.values() for keyword in keywords):
                    # This is likely personal info or summary
                    if "personal" not in sections:
                        sections["personal"] = []
                    sections["personal"].append(line)

        # Add the last section
        if current_section and current_content:
            sections[current_section] = "\n".join(current_content).strip()

        return sections

    def _extract_personal_info(self, text: str) -> Dict[str, str]:
        """Extract personal information from resume."""
        personal_info = {}
        lines = text.split('\n')

        # Email pattern
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        emails = re.findall(email_pattern, text)
        if emails:
            personal_info["email"] = emails[0]

        # Phone pattern (Indian and international)
        phone_patterns = [
            r'\+?[0-9]{1,4}[-.\s]?\(?[0-9]{1,4}\)?[-.\s]?[0-9]{1,4}[-.\s]?[0-9]{1,4}[-.\s]?[0-9]{1,9}',
            r'[0-9]{10}',
            r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b'
        ]

        for pattern in phone_patterns:
            phones = re.findall(pattern, text)
            if phones:
                personal_info["phone"] = phones[0]
                break

        # Name - assume first non-empty line is name
        for line in lines:
            if line.strip() and not re.search(email_pattern, line) and not re.search(r'[0-9]{10}', line):
                personal_info["name"] = line.strip()
                break

        # LinkedIn and GitHub URLs
        linkedin_pattern = r'linkedin\.com/in/[a-zA-Z0-9\-]+'
        github_pattern = r'github\.com/[a-zA-Z0-9\-]+'

        linkedin_matches = re.findall(linkedin_pattern, text)
        if linkedin_matches:
            personal_info["linkedin"] = "https://" + linkedin_matches[0]

        github_matches = re.findall(github_pattern, text)
        if github_matches:
            personal_info["github"] = "https://" + github_matches[0]

        return personal_info

    def _extract_education(self, text: str) -> List[Dict[str, str]]:
        """Extract education details."""
        education_list = []
        lines = text.split('\n')

        current_edu = {}
        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Check for degree patterns
            degree_patterns = [
                r'(B\.?C\.?A\.?|B\.?Tech\.?|B\.?E\.?|M\.?C\.?A\.?|M\.?Tech\.?|B\.?S\.?c\.?|M\.?S\.?c\.?)',
                r'Bachelor.*Computer.*Application',
                r'Bachelor.*Technology',
                r'Master.*Computer.*Application'
            ]

            for pattern in degree_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    if current_edu:
                        education_list.append(current_edu)
                    current_edu = {"degree": line}
                    break

            # Check for college/university
            if "university" in line.lower() or "college" in line.lower():
                current_edu["college"] = line

            # Check for CGPA/percentage
            cgpa_match = re.search(r'(CGPA|GPA|Percentage|%)\s*[:\.]?\s*([0-9\.]+)', line, re.IGNORECASE)
            if cgpa_match:
                current_edu["cgpa"] = cgpa_match.group(2)

            # Check for year
            year_match = re.search(r'(20[0-9]{2}[-–]20[0-9]{2}|20[0-9]{2})', line)
            if year_match:
                years = year_match.group(1).split('-')
                if len(years) == 2:
                    current_edu["start_date"] = years[0]
                    current_edu["end_date"] = years[1]
                    current_edu["graduation_year"] = years[1]

        if current_edu:
            education_list.append(current_edu)

        return education_list

    def _extract_experience(self, text: str) -> List[Dict[str, str]]:
        """Extract work experience."""
        experience_list = []
        lines = text.split('\n')

        current_exp = {}
        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Check for company/role patterns
            if re.search(r'(@|at|company|Corp|Ltd|Pvt|Inc|Tech)', line, re.IGNORECASE):
                if current_exp and current_exp.get("company"):
                    experience_list.append(current_exp)
                    current_exp = {}
                parts = line.split('|')
                if len(parts) >= 2:
                    current_exp["role"] = parts[0].strip()
                    current_exp["company"] = parts[1].strip()
                else:
                    current_exp["company"] = line

            # Check for duration
            duration_match = re.search(r'([A-Za-z]+ \d{4} - [A-Za-z]+ \d{4}|\d{4} - \d{4})', line)
            if duration_match:
                current_exp["duration"] = duration_match.group(1)

            # If line looks like description and we have a company
            elif current_exp.get("company") and len(line) > 20:
                current_exp["description"] = line

        if current_exp and current_exp.get("company"):
            experience_list.append(current_exp)

        return experience_list

    def _extract_skills(self, text: str) -> List[str]:
        """Extract technical skills."""
        skills = []

        # Common skill patterns
        skill_keywords = [
            "python", "javascript", "java", "c++", "c#", "php", "ruby", "swift", "kotlin",
            "react", "angular", "vue", "node", "express", "django", "flask", "spring",
            "sql", "mysql", "postgresql", "mongodb", "redis", "aws", "docker", "kubernetes",
            "git", "github", "gitlab", "jenkins", "linux", "html", "css", "typescript"
        ]

        # Split by commas, semicolons, or bullets
        skill_parts = re.split(r'[,;•\n]', text.lower())

        for part in skill_parts:
            part = part.strip()
            if not part:
                continue

            # Check if part contains any known skill
            for skill in skill_keywords:
                if skill in part and skill not in skills:
                    skills.append(skill)

            # Also add the part if it looks like a skill
            if len(part.split()) <= 3 and any(char.isalpha() for char in part):
                if part not in skills and part not in ["and", "or", "etc"]:
                    skills.append(part)

        return skills

    def _extract_projects(self, text: str) -> List[Dict[str, str]]:
        """Extract project information."""
        projects = []
        lines = text.split('\n')

        current_project = {}
        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Check if line is a project title (short, capitalized)
            if len(line) < 50 and not line.endswith('.') and line[0].isupper():
                if current_project and current_project.get("title"):
                    projects.append(current_project)
                current_project = {"title": line}

            # Check for technologies
            elif "technologies" in line.lower() or "tech stack" in line.lower():
                tech_part = line.lower().replace("technologies:", "").replace("tech stack:", "").strip()
                current_project["technologies"] = [t.strip() for t in tech_part.split(',') if t.strip()]

            # Check for URLs
            elif "github.com" in line.lower():
                current_project["github_url"] = line.strip()
            elif "live demo" in line.lower() or "http" in line.lower():
                urls = re.findall(r'https?://[^\s]+', line)
                if urls:
                    current_project["live_url"] = urls[0]

            # Assume longer text is description
            elif len(line) > 30 and "title" in current_project:
                if "description" not in current_project:
                    current_project["description"] = line
                else:
                    current_project["description"] += " " + line

        if current_project and current_project.get("title"):
            projects.append(current_project)

        return projects

    def _extract_certifications(self, text: str) -> List[Dict[str, str]]:
        """Extract certification information."""
        certifications = []
        lines = text.split('\n')

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Look for certification names
            if any(keyword in line.lower() for keyword in ["certified", "certificate", "course", "training", "udemy", "coursera"]):
                cert = {"certificate_name": line}

                # Try to find issuer
                issuer_patterns = [
                    "by", "from", "issued by", "certified by"
                ]
                for pattern in issuer_patterns:
                    if pattern in line.lower():
                        parts = line.lower().split(pattern)
                        if len(parts) > 1:
                            cert["issuer"] = parts[1].strip()
                            break

                # Try to find date
                date_match = re.search(r'([A-Za-z]+ \d{4}|\d{4})', line)
                if date_match:
                    cert["issue_date"] = date_match.group(1)

                certifications.append(cert)

        return certifications
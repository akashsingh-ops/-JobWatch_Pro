import re
from typing import Dict, List, Any

class ResumeParserService:
    """
    Parses resume text into structured candidate profile data.
    """
    KNOWN_SKILLS = [
        'React', 'TypeScript', 'JavaScript', 'Python', 'Django', 'FastAPI', 'Node.js',
        'PostgreSQL', 'MySQL', 'MongoDB', 'Redis', 'Docker', 'Kubernetes', 'AWS',
        'GCP', 'Azure', 'GraphQL', 'REST API', 'Tailwind CSS', 'Next.js', 'PyTorch',
        'TensorFlow', 'CI/CD', 'Git', 'Linux', 'Security', 'Kafka', 'Elasticsearch'
    ]

    @classmethod
    def parse_resume(cls, text: str) -> Dict[str, Any]:
        found_skills = []
        for skill in cls.KNOWN_SKILLS:
            pattern = rf'\b{re.escape(skill)}\b'
            if re.search(pattern, text, re.IGNORECASE):
                found_skills.append(skill)

        # Estimate experience
        exp_match = re.search(r'(\d+)\+?\s*(?:years|yrs)', text, re.IGNORECASE)
        years = int(exp_match.group(1)) if exp_match else 3

        return {
            'detected_skills': found_skills or ['TypeScript', 'React', 'Python', 'PostgreSQL'],
            'estimated_experience_years': min(years, 20),
            'summary': text[:300].strip() if text else "Candidate resume"
        }

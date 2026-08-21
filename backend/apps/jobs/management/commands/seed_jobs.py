from django.core.management.base import BaseCommand
from apps.companies.models import Company
from apps.skills.models import Skill
from apps.jobs.models import Job

class Command(BaseCommand):
    help = 'Seeds initial companies, skills, and industry jobs into Neon PostgreSQL'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding initial data into Neon PostgreSQL...')

        # 1. Companies
        companies_data = [
            {'name': 'Nexus Technologies', 'industry': 'Cloud Infrastructure', 'location': 'San Francisco, CA', 'website': 'https://example.com/nexus', 'logo_url': 'https://images.unsplash.com/photo-1542744094-3a31f272c490?w=128&auto=format&fit=crop&q=60'},
            {'name': 'Cortex Data Labs', 'industry': 'Artificial Intelligence', 'location': 'New York, NY', 'website': 'https://example.com/cortex', 'logo_url': 'https://images.unsplash.com/photo-1551434678-e076c223a692?w=128&auto=format&fit=crop&q=60'},
            {'name': 'Aether Dynamics', 'industry': 'Developer Tooling', 'location': 'Austin, TX', 'website': 'https://example.com/aether', 'logo_url': 'https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=128&auto=format&fit=crop&q=60'},
            {'name': 'Pulse Platform', 'industry': 'Financial Tech', 'location': 'Seattle, WA', 'website': 'https://example.com/pulse', 'logo_url': 'https://images.unsplash.com/photo-1573164713988-8665fc963095?w=128&auto=format&fit=crop&q=60'},
            {'name': 'Vanguard Security', 'industry': 'Cybersecurity', 'location': 'Boston, MA', 'website': 'https://example.com/vanguard', 'logo_url': 'https://images.unsplash.com/photo-1563986768609-322da13575f3?w=128&auto=format&fit=crop&q=60'},
            {'name': 'Orbit Media', 'industry': 'Digital Product & Design', 'location': 'Remote / US', 'website': 'https://example.com/orbit', 'logo_url': 'https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=128&auto=format&fit=crop&q=60'},
        ]

        company_map = {}
        for cdata in companies_data:
            c, created = Company.objects.get_or_create(
                name=cdata['name'],
                defaults=cdata
            )
            company_map[c.name] = c

        # 2. Skills
        skills_data = [
            ('React', 'frontend'), ('TypeScript', 'languages'), ('Python', 'languages'),
            ('Django', 'backend'), ('PostgreSQL', 'database'), ('Node.js', 'backend'),
            ('Docker', 'cloud_devops'), ('Kubernetes', 'cloud_devops'), ('AWS', 'cloud_devops'),
            ('PyTorch', 'ai_ml'), ('Tailwind CSS', 'frontend'), ('GraphQL', 'backend'),
            ('Next.js', 'frontend'), ('Figma', 'frontend'), ('Go', 'languages'),
            ('Terraform', 'cloud_devops'), ('FastAPI', 'backend'), ('Rust', 'languages')
        ]

        skill_map = {}
        for name, cat in skills_data:
            s, _ = Skill.objects.get_or_create(
                name=name,
                defaults={'category': cat, 'normalized_name': name.lower()}
            )
            skill_map[name] = s

        # 3. Seed Jobs
        jobs_seed = [
            {
                'id': 'job-1',
                'company': 'Nexus Technologies',
                'title': 'Senior Full Stack Engineer (React / Python)',
                'location': 'San Francisco, CA (Hybrid)',
                'category': 'Engineering',
                'type': 'Full-time',
                'remote_type': 'hybrid',
                'experienceLevel': 'Senior',
                'salary': '$165,000 - $195,000',
                'featured': True,
                'description': 'Join Nexus Technologies to architect high-throughput web telemetry platforms. You will design scalable React frontends and Django/PostgreSQL microservices processing real-time developer metrics.',
                'requirements': [
                    '5+ years experience building production React and TypeScript applications',
                    'Proficiency in Python backend frameworks (Django, FastAPI)',
                    'Strong database optimization skills in PostgreSQL',
                    'Experience with containerized CI/CD workflows (Docker, GitHub Actions)'
                ],
                'skills': ['React', 'TypeScript', 'Python', 'Django', 'PostgreSQL', 'Docker']
            },
            {
                'id': 'job-2',
                'company': 'Cortex Data Labs',
                'title': 'Staff AI & Machine Learning Researcher',
                'location': 'Remote / US',
                'category': 'AI & Data Science',
                'type': 'Remote',
                'remote_type': 'remote',
                'experienceLevel': 'Lead',
                'salary': '$210,000 - $260,000',
                'featured': True,
                'description': 'Lead our core AI intelligence group developing foundation model fine-tuning and retrieval-augmented generation pipelines for automated talent telemetry.',
                'requirements': [
                    'M.S. or Ph.D. in Computer Science, Machine Learning, or related field',
                    'Deep expertise with PyTorch, Transformer architectures, and vector search',
                    'Track record of deploying LLM systems in high-availability environments',
                    'Strong Python software engineering practices'
                ],
                'skills': ['Python', 'PyTorch', 'AWS', 'PostgreSQL']
            },
            {
                'id': 'job-3',
                'company': 'Aether Dynamics',
                'title': 'Lead Cloud Infrastructure / DevOps Architect',
                'location': 'Austin, TX (On-site)',
                'category': 'DevOps',
                'type': 'Full-time',
                'remote_type': 'onsite',
                'experienceLevel': 'Lead',
                'salary': '$180,000 - $220,000',
                'featured': False,
                'description': 'Scale multi-region Kubernetes clusters across AWS and GCP. Build resilient infrastructure-as-code and automated canary deployments.',
                'requirements': [
                    '6+ years in DevOps / Platform engineering',
                    'Mastery of Terraform, Kubernetes, and Helm',
                    'Deep understanding of network security, VPC peering, and observability'
                ],
                'skills': ['Kubernetes', 'Docker', 'AWS', 'Terraform']
            },
            {
                'id': 'job-4',
                'company': 'Orbit Media',
                'title': 'Principal Product Designer (Design Systems)',
                'location': 'Remote / Global',
                'category': 'Design',
                'type': 'Remote',
                'remote_type': 'remote',
                'experienceLevel': 'Senior',
                'salary': '$145,000 - $175,000',
                'featured': True,
                'description': 'Design intuitive, accessible UI component ecosystems and telemetry dashboards for enterprise recruitment teams.',
                'requirements': [
                    'Portfolio demonstrating end-to-end design systems in Figma',
                    'Strong understanding of HTML/CSS, Tailwind, and React design tokens',
                    'Proven experience in rapid prototyping and user research'
                ],
                'skills': ['Figma', 'Tailwind CSS', 'React']
            },
            {
                'id': 'job-5',
                'company': 'Pulse Platform',
                'title': 'Senior Backend Engineer (Go / PostgreSQL)',
                'location': 'Seattle, WA (Hybrid)',
                'category': 'Engineering',
                'type': 'Full-time',
                'remote_type': 'hybrid',
                'experienceLevel': 'Senior',
                'salary': '$170,000 - $205,000',
                'featured': False,
                'description': 'Architect low-latency financial transaction pipelines and distributed event streams handling millions of events per hour.',
                'requirements': [
                    '4+ years building high-throughput systems in Go or Rust',
                    'Advanced PostgreSQL indexing, partitioning, and connection pooling',
                    'Experience with event streams and Redis caching'
                ],
                'skills': ['Go', 'PostgreSQL', 'Docker']
            },
            {
                'id': 'job-6',
                'company': 'Vanguard Security',
                'title': 'Application Security & Pen-Testing Specialist',
                'location': 'Boston, MA (Hybrid)',
                'category': 'Security',
                'type': 'Full-time',
                'remote_type': 'hybrid',
                'experienceLevel': 'Mid',
                'salary': '$150,000 - $185,000',
                'featured': False,
                'description': 'Lead threat modeling, automated vulnerability scans, and security audits across our SaaS infrastructure.',
                'requirements': [
                    'Experience conducting SAST/DAST reviews in CI/CD pipelines',
                    'Knowledge of OWASP Top 10, OAuth2, and zero-trust architectures',
                    'Certifications like OSCP, CISSP, or equivalent experience'
                ],
                'skills': ['Python', 'Docker', 'AWS']
            },
            {
                'id': 'job-7',
                'company': 'Nexus Technologies',
                'title': 'Frontend Developer (React / Next.js)',
                'location': 'San Francisco, CA (Hybrid)',
                'category': 'Engineering',
                'type': 'Full-time',
                'remote_type': 'hybrid',
                'experienceLevel': 'Mid',
                'salary': '$130,000 - $160,000',
                'featured': False,
                'description': 'Craft snappy, accessible web experiences using React, TypeScript, and modern styling libraries.',
                'requirements': [
                    '3+ years React and TypeScript experience',
                    'Familiarity with TanStack Query and state management',
                    'Passion for UI animations and micro-interactions'
                ],
                'skills': ['React', 'TypeScript', 'Next.js', 'Tailwind CSS']
            },
            {
                'id': 'job-8',
                'company': 'Cortex Data Labs',
                'title': 'Senior Product Manager — AI Intelligence',
                'location': 'New York, NY (Hybrid)',
                'category': 'Product',
                'type': 'Full-time',
                'remote_type': 'hybrid',
                'experienceLevel': 'Senior',
                'salary': '$175,000 - $215,000',
                'featured': True,
                'description': 'Define product roadmap for AI-assisted talent search, smart skill graphs, and career trajectory intelligence.',
                'requirements': [
                    '4+ years product management experience in B2B SaaS or AI products',
                    'Technical background with ability to engage with ML engineering teams',
                    'Customer-centric discovery and roadmap prioritization skills'
                ],
                'skills': ['Python']
            }
        ]

        for jdata in jobs_seed:
            company = company_map.get(jdata['company'])
            skills_names = jdata.pop('skills', [])
            job, created = Job.objects.update_or_create(
                id=jdata['id'],
                defaults={
                    'company': company,
                    'title': jdata['title'],
                    'location': jdata['location'],
                    'category': jdata['category'],
                    'employment_type': jdata['type'],
                    'experience_level': jdata['experienceLevel'],
                    'remote_type': jdata['remote_type'],
                    'salary': jdata['salary'],
                    'featured': jdata['featured'],
                    'description': jdata['description'],
                    'requirements': jdata['requirements'],
                    'application_url': 'https://example.com/apply',
                    'source': 'direct',
                    'is_active': True,
                }
            )
            job_skill_objs = [skill_map[s] for s in skills_names if s in skill_map]
            job.required_skills.set(job_skill_objs)

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {len(jobs_seed)} jobs into Neon PostgreSQL!'))

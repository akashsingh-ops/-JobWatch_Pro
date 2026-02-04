"""
Job application domain entity with comprehensive tracking
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum
import uuid


class ApplicationStatus(Enum):
    """Application status"""
    DRAFT = "draft"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    SHORTLISTED = "shortlisted"
    INTERVIEW_SCHEDULED = "interview_scheduled"
    INTERVIEW_COMPLETED = "interview_completed"
    OFFER_EXTENDED = "offer_extended"
    OFFER_ACCEPTED = "offer_accepted"
    OFFER_DECLINED = "offer_declined"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"
    HIRED = "hired"


class InterviewType(Enum):
    """Interview type"""
    PHONE_SCREEN = "phone_screen"
    TECHNICAL = "technical"
    BEHAVIORAL = "behavioral"
    SYSTEM_DESIGN = "system_design"
    FINAL = "final"
    CULTURE_FIT = "culture_fit"


@dataclass
class Interview:
    """Interview value object"""
    interview_id: str
    interview_type: InterviewType
    scheduled_at: datetime
    duration_minutes: int = 60
    interviewers: List[str] = field(default_factory=list)
    location: Optional[str] = None  # physical location or virtual link
    is_virtual: bool = True
    notes: Optional[str] = None
    feedback: Optional[str] = None
    rating: Optional[int] = None  # 1-5 scale
    status: str = "scheduled"  # scheduled, completed, cancelled, rescheduled


@dataclass
class ApplicationResponse:
    """Application question response"""
    question_id: str
    response: str
    response_type: str  # text, file_url, etc.


@dataclass
class OfferDetails:
    """Job offer details"""
    salary_offered: Optional[int] = None
    equity_offered: Optional[str] = None
    benefits: List[str] = field(default_factory=list)
    start_date: Optional[datetime] = None
    offer_deadline: Optional[datetime] = None
    notes: Optional[str] = None


class JobApplication:
    """Job application domain entity"""

    def __init__(self, application_id: str, user_id: str, job_id: str):
        self.id = application_id
        self.user_id = user_id
        self.job_id = job_id

        # Application content
        self.cover_letter: Optional[str] = None
        self.resume_url: Optional[str] = None
        self.portfolio_url: Optional[str] = None
        self.linkedin_url: Optional[str] = None
        self.github_url: Optional[str] = None
        self.website_url: Optional[str] = None

        # Custom question responses
        self.question_responses: List[ApplicationResponse] = []

        # Status and tracking
        self.status = ApplicationStatus.SUBMITTED
        self.status_history: List[Dict[str, Any]] = [
            {
                "status": ApplicationStatus.SUBMITTED.value,
                "changed_at": datetime.utcnow(),
                "changed_by": user_id,
                "notes": "Application submitted"
            }
        ]

        # Interview process
        self.interviews: List[Interview] = []

        # Offer details
        self.offer_details: Optional[OfferDetails] = None

        # Timestamps
        self.applied_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.last_status_change = datetime.utcnow()

        # Internal notes (for employers)
        self.internal_notes: List[Dict[str, Any]] = []

        # Scoring and ranking
        self.compatibility_score: Optional[float] = None
        self.employer_rating: Optional[int] = None  # 1-5 scale
        self.priority_level: str = "normal"  # low, normal, high, urgent

    def update_status(self, new_status: ApplicationStatus, changed_by: str,
                     notes: str = "") -> 'ApplicationStatusChanged':
        """Update application status"""
        if self.status == new_status:
            return None

        # Validate status transitions
        if not self._is_valid_status_transition(self.status, new_status):
            raise ValueError(f"Invalid status transition from {self.status.value} to {new_status.value}")

        old_status = self.status
        self.status = new_status
        self.updated_at = datetime.utcnow()
        self.last_status_change = datetime.utcnow()

        # Add to status history
        self.status_history.append({
            "status": new_status.value,
            "changed_at": self.last_status_change,
            "changed_by": changed_by,
            "notes": notes
        })

        from ..events.application_events import ApplicationStatusChanged
        return ApplicationStatusChanged(
            self.id, old_status.value, new_status.value, changed_by, notes
        )

    def _is_valid_status_transition(self, from_status: ApplicationStatus,
                                  to_status: ApplicationStatus) -> bool:
        """Validate status transition logic"""
        # Define valid transitions
        valid_transitions = {
            ApplicationStatus.SUBMITTED: [
                ApplicationStatus.UNDER_REVIEW, ApplicationStatus.REJECTED, ApplicationStatus.WITHDRAWN
            ],
            ApplicationStatus.UNDER_REVIEW: [
                ApplicationStatus.SHORTLISTED, ApplicationStatus.REJECTED,
                ApplicationStatus.INTERVIEW_SCHEDULED, ApplicationStatus.WITHDRAWN
            ],
            ApplicationStatus.SHORTLISTED: [
                ApplicationStatus.INTERVIEW_SCHEDULED, ApplicationStatus.REJECTED, ApplicationStatus.WITHDRAWN
            ],
            ApplicationStatus.INTERVIEW_SCHEDULED: [
                ApplicationStatus.INTERVIEW_COMPLETED, ApplicationStatus.REJECTED, ApplicationStatus.WITHDRAWN
            ],
            ApplicationStatus.INTERVIEW_COMPLETED: [
                ApplicationStatus.OFFER_EXTENDED, ApplicationStatus.REJECTED, ApplicationStatus.WITHDRAWN
            ],
            ApplicationStatus.OFFER_EXTENDED: [
                ApplicationStatus.OFFER_ACCEPTED, ApplicationStatus.OFFER_DECLINED, ApplicationStatus.WITHDRAWN
            ],
            ApplicationStatus.OFFER_ACCEPTED: [ApplicationStatus.HIRED],
            # Terminal states
            ApplicationStatus.REJECTED: [],
            ApplicationStatus.WITHDRAWN: [],
            ApplicationStatus.OFFER_DECLINED: [],
            ApplicationStatus.HIRED: []
        }

        return to_status in valid_transitions.get(from_status, [])

    def schedule_interview(self, interview_data: Dict[str, Any], scheduled_by: str) -> 'InterviewScheduled':
        """Schedule an interview"""
        interview_id = str(uuid.uuid4())
        interview = Interview(
            interview_id=interview_id,
            interview_type=InterviewType(interview_data['interview_type']),
            scheduled_at=interview_data['scheduled_at'],
            duration_minutes=interview_data.get('duration_minutes', 60),
            interviewers=interview_data.get('interviewers', []),
            location=interview_data.get('location'),
            is_virtual=interview_data.get('is_virtual', True)
        )

        self.interviews.append(interview)
        self.updated_at = datetime.utcnow()

        from ..events.application_events import InterviewScheduled
        return InterviewScheduled(self.id, interview_id, scheduled_by)

    def complete_interview(self, interview_id: str, feedback: str,
                          rating: int, completed_by: str) -> 'InterviewCompleted':
        """Mark interview as completed"""
        interview = next((i for i in self.interviews if i.interview_id == interview_id), None)
        if not interview:
            raise ValueError("Interview not found")

        interview.status = "completed"
        interview.feedback = feedback
        interview.rating = rating
        interview.notes = f"Completed by {completed_by} at {datetime.utcnow()}"

        self.updated_at = datetime.utcnow()

        from ..events.application_events import InterviewCompleted
        return InterviewCompleted(self.id, interview_id, rating, completed_by)

    def extend_offer(self, offer_data: Dict[str, Any], offered_by: str) -> 'OfferExtended':
        """Extend job offer"""
        self.offer_details = OfferDetails(**offer_data)
        self.update_status(ApplicationStatus.OFFER_EXTENDED, offered_by, "Job offer extended")

        from ..events.application_events import OfferExtended
        return OfferExtended(self.id, offered_by)

    def accept_offer(self) -> 'OfferAccepted':
        """Accept job offer"""
        if self.status != ApplicationStatus.OFFER_EXTENDED:
            raise ValueError("No offer to accept")

        self.update_status(ApplicationStatus.OFFER_ACCEPTED, self.user_id, "Offer accepted by candidate")

        from ..events.application_events import OfferAccepted
        return OfferAccepted(self.id)

    def decline_offer(self, reason: str = "") -> 'OfferDeclined':
        """Decline job offer"""
        if self.status != ApplicationStatus.OFFER_EXTENDED:
            raise ValueError("No offer to decline")

        notes = f"Offer declined by candidate. Reason: {reason}" if reason else "Offer declined by candidate"
        self.update_status(ApplicationStatus.OFFER_DECLINED, self.user_id, notes)

        from ..events.application_events import OfferDeclined
        return OfferDeclined(self.id, reason)

    def withdraw_application(self, reason: str = "") -> 'ApplicationWithdrawn':
        """Withdraw application"""
        notes = f"Application withdrawn by candidate. Reason: {reason}" if reason else "Application withdrawn by candidate"
        self.update_status(ApplicationStatus.WITHDRAWN, self.user_id, notes)

        from ..events.application_events import ApplicationWithdrawn
        return ApplicationWithdrawn(self.id, reason)

    def add_internal_note(self, note: str, added_by: str) -> None:
        """Add internal note for employers"""
        self.internal_notes.append({
            "note": note,
            "added_by": added_by,
            "added_at": datetime.utcnow()
        })
        self.updated_at = datetime.utcnow()

    def set_compatibility_score(self, score: float) -> None:
        """Set AI-calculated compatibility score"""
        self.compatibility_score = max(0.0, min(1.0, score))  # Ensure 0-1 range

    def set_employer_rating(self, rating: int) -> None:
        """Set employer rating (1-5 scale)"""
        self.employer_rating = max(1, min(5, rating))

    def set_priority_level(self, level: str) -> None:
        """Set priority level"""
        if level in ["low", "normal", "high", "urgent"]:
            self.priority_level = level

    def get_days_since_application(self) -> int:
        """Get days since application was submitted"""
        return (datetime.utcnow() - self.applied_at).days

    def get_days_since_last_update(self) -> int:
        """Get days since last status update"""
        return (datetime.utcnow() - self.last_status_change).days

    def is_active(self) -> bool:
        """Check if application is still active"""
        return self.status not in [
            ApplicationStatus.REJECTED,
            ApplicationStatus.WITHDRAWN,
            ApplicationStatus.OFFER_DECLINED
        ]

    def can_be_withdrawn_by_candidate(self) -> bool:
        """Check if candidate can still withdraw application"""
        return self.status in [
            ApplicationStatus.SUBMITTED,
            ApplicationStatus.UNDER_REVIEW,
            ApplicationStatus.SHORTLISTED,
            ApplicationStatus.INTERVIEW_SCHEDULED,
            ApplicationStatus.INTERVIEW_COMPLETED
        ]

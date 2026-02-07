"""
Legal Case Metadata Extractor
Senior Legal Data Engineer & Jurimetric Analysis Tool

Extracts structured metadata from unstructured U.S. court case opinions.
Outputs JSON conforming to the defined legal data schema.
"""

import re
import json
from datetime import datetime
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, asdict, field


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class Party:
    """Represents a plaintiff or defendant."""
    name: str
    type: str  # "Individual" | "Corporation" | "Government"


@dataclass
class CaseMetadata:
    """Complete case metadata schema."""
    # Case Identity
    case_name: Optional[str] = None
    citation: Optional[str] = None
    date_filed: Optional[str] = None
    court_name: Optional[str] = None
    jurisdiction_level: Optional[str] = None
    
    # Actors
    judges: List[str] = field(default_factory=list)
    plaintiffs: List[Dict[str, str]] = field(default_factory=list)
    defendants: List[Dict[str, str]] = field(default_factory=list)
    counsel_plaintiff: List[str] = field(default_factory=list)
    counsel_defense: List[str] = field(default_factory=list)
    
    # Subject Matter
    primary_topic: Optional[str] = None
    specific_cause_of_action: Optional[str] = None
    industry_sector: Optional[str] = None
    
    # Outcome & Procedure
    procedural_posture: Optional[str] = None
    disposition: Optional[str] = None
    prevailing_party: Optional[str] = None
    monetary_damages: Optional[float] = None
    
    # Evidence
    evidence_types: List[str] = field(default_factory=list)
    
    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(asdict(self), indent=2, default=str)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


# ============================================================================
# PATTERN DEFINITIONS
# ============================================================================

class LegalPatterns:
    """Regex patterns for legal document parsing."""
    
    # Case name patterns (e.g., "Roe v. Wade", "Smith vs. Jones", "APPLE INC. v. QUALCOMM INC.")
    CASE_NAME = re.compile(
        r'([A-Z][a-zA-Z\.\s&,\'-]+)\s+v\.?\s*(?:vs?\.?\s*)?([A-Z][a-zA-Z\.\s&,\'-]+)',
        re.IGNORECASE
    )
    
    # Alternative pattern for labeled parties
    LABELED_PARTY = re.compile(
        r'([A-Z][^,\n]+?),?\s*(?:a\s+\w+\s+corporation)?\s*,?\s*\n\s*(?:Plaintiff|Defendant|Petitioner|Respondent|Appellant|Appellee)',
        re.IGNORECASE
    )
    
    # Citation patterns
    CITATION_PATTERNS = [
        re.compile(r'(\d+)\s+U\.?S\.?\s+(\d+)'),  # U.S. Reports: 410 U.S. 113
        re.compile(r'(\d+)\s+S\.?\s*Ct\.?\s+(\d+)'),  # Supreme Court Reporter
        re.compile(r'(\d+)\s+F\.?\s*(?:2d|3d|4th)?\s+(\d+)'),  # Federal Reporter
        re.compile(r'(\d+)\s+F\.?\s*Supp\.?\s*(?:2d|3d)?\s+(\d+)'),  # F. Supp.
        re.compile(r'(\d+)\s+L\.?\s*Ed\.?\s*(?:2d)?\s+(\d+)'),  # Lawyers Edition
    ]
    
    # Date patterns
    DATE_PATTERNS = [
        re.compile(r'(?:decided|filed|dated|argued)[\s:]+([A-Za-z]+\s+\d{1,2},?\s+\d{4})', re.I),
        re.compile(r'(\d{1,2}/\d{1,2}/\d{4})'),
        re.compile(r'(\d{4}-\d{2}-\d{2})'),
        re.compile(r'([A-Za-z]+\s+\d{1,2},?\s+\d{4})'),
    ]
    
    # Court patterns
    COURT_PATTERNS = [
        (re.compile(r'Supreme\s+Court\s+of\s+the\s+United\s+States', re.I), 
         "Supreme Court of the United States", "Federal"),
        (re.compile(r'UNITED\s+STATES\s+COURT\s+OF\s+APPEALS\s+FOR\s+THE\s+(\w+)\s+CIRCUIT', re.I),
         "U.S. Court of Appeals for the {} Circuit", "Federal"),
        (re.compile(r'U\.?S\.?\s+Court\s+of\s+Appeals.*?(?:for\s+the\s+)?(\w+)\s+Circuit', re.I), 
         "U.S. Court of Appeals for the {} Circuit", "Federal"),
        (re.compile(r'United\s+States\s+District\s+Court.*?(?:for\s+the\s+)?(?:Southern|Northern|Eastern|Western|Central)?\s*District\s+of\s+(\w+)', re.I),
         "U.S. District Court for the District of {}", "Federal"),
        (re.compile(r'(\w+)\s+Circuit\s+Court\s+of\s+Appeals', re.I),
         "U.S. Court of Appeals for the {} Circuit", "Federal"),
        (re.compile(r'(\w+),?\s+(?:HURWITZ|NGUYEN|and\s+\w+),?\s+Circuit\s+Judges', re.I),
         "U.S. Court of Appeals for the {} Circuit", "Federal"),
        (re.compile(r'Supreme\s+Court\s+of\s+(\w+)', re.I),
         "Supreme Court of {}", "State"),
        (re.compile(r'Court\s+of\s+Appeals?\s+of\s+(\w+)', re.I),
         "Court of Appeals of {}", "State"),
    ]
    
    # Judge patterns
    JUDGE_PATTERNS = [
        re.compile(r'(?:Before|Per Curiam|Opinion by|Judge|Justice|JUDGE|JUSTICE)[:\s]+([A-Z][a-z]+(?:\s+[A-Z]\.?\s*)?[A-Z][a-z]+)', re.I),
        re.compile(r'([A-Z][a-z]+),\s*(?:C\.?)?J\.?,?\s*(?:delivered|wrote|authored)', re.I),
        re.compile(r'(?:Chief\s+)?Justice\s+([A-Z][a-z]+(?:\s+[A-Z]\.?\s*)?[A-Z][a-z]+)', re.I),
        re.compile(r'(?:Circuit|District)\s+Judge\s+([A-Z][a-z]+(?:\s+[A-Z]\.?\s*)?[A-Z][a-z]+)', re.I),
    ]
    
    # Attorney/Counsel patterns
    COUNSEL_PATTERNS = [
        re.compile(r'(?:for\s+(?:the\s+)?(?:plaintiff|petitioner|appellant))[\s:,]+([A-Z][a-zA-Z\.\s,&]+?)(?:\.|;|$)', re.I),
        re.compile(r'(?:for\s+(?:the\s+)?(?:defendant|respondent|appellee))[\s:,]+([A-Z][a-zA-Z\.\s,&]+?)(?:\.|;|$)', re.I),
        re.compile(r'([A-Z][a-z]+(?:\s+[A-Z]\.?\s*)?[A-Z][a-z]+),?\s+(?:Esq\.?|Attorney|Counsel)', re.I),
    ]
    
    # Disposition patterns
    DISPOSITION_KEYWORDS = {
        'affirmed': 'Affirmed',
        'reversed': 'Reversed',
        'remanded': 'Remanded',
        'vacated': 'Vacated',
        'dismissed': 'Dismissed',
        'denied': 'Denied',
        'granted': 'Granted',
        'modified': 'Modified',
        'affirmed in part': 'Affirmed in Part',
        'reversed in part': 'Reversed in Part',
    }
    
    # Procedural posture patterns
    POSTURE_KEYWORDS = {
        'motion to dismiss': 'Motion to Dismiss',
        'summary judgment': 'Summary Judgment',
        'appeal': 'Appeal',
        'certiorari': 'Certiorari',
        'habeas corpus': 'Habeas Corpus',
        'preliminary injunction': 'Preliminary Injunction',
        'class action': 'Class Action',
        'trial': 'Trial',
        'bench trial': 'Bench Trial',
        'jury trial': 'Jury Trial',
    }
    
    # Legal topics
    TOPIC_KEYWORDS = {
        # Intellectual Property
        'patent': ('Intellectual Property', 'Patent Infringement'),
        'trademark': ('Intellectual Property', 'Trademark Infringement'),
        'copyright': ('Intellectual Property', 'Copyright Infringement'),
        'trade secret': ('Intellectual Property', 'Trade Secret Misappropriation'),
        
        # Contract
        'breach of contract': ('Contract', 'Breach of Contract'),
        'contract dispute': ('Contract', 'Contract Dispute'),
        'specific performance': ('Contract', 'Specific Performance'),
        
        # Tort
        'negligence': ('Tort', 'Negligence'),
        'malpractice': ('Tort', 'Professional Malpractice'),
        'defamation': ('Tort', 'Defamation'),
        'fraud': ('Tort', 'Fraud'),
        'product liability': ('Tort', 'Product Liability'),
        
        # Constitutional
        'first amendment': ('Constitutional Law', 'First Amendment'),
        'fourth amendment': ('Constitutional Law', 'Fourth Amendment'),
        'due process': ('Constitutional Law', 'Due Process'),
        'equal protection': ('Constitutional Law', 'Equal Protection'),
        
        # Employment
        'discrimination': ('Employment', 'Employment Discrimination'),
        'wrongful termination': ('Employment', 'Wrongful Termination'),
        'title vii': ('Employment', 'Title VII Discrimination'),
        
        # Criminal
        'criminal': ('Criminal', 'Criminal Prosecution'),
        'murder': ('Criminal', 'Murder'),
        'robbery': ('Criminal', 'Robbery'),
        
        # Antitrust
        'antitrust': ('Antitrust', 'Antitrust Violation'),
        'sherman act': ('Antitrust', 'Sherman Act Violation'),
        
        # Securities
        'securities': ('Securities', 'Securities Fraud'),
        '10b-5': ('Securities', 'Rule 10b-5 Violation'),
        
        # Environmental
        'environmental': ('Environmental', 'Environmental Violation'),
        'clean air': ('Environmental', 'Clean Air Act Violation'),
        'clean water': ('Environmental', 'Clean Water Act Violation'),
    }
    
    # Industry keywords
    INDUSTRY_KEYWORDS = {
        'pharmaceutical': 'Pharmaceuticals',
        'drug': 'Pharmaceuticals',
        'medicine': 'Pharmaceuticals',
        'technology': 'Technology',
        'software': 'Technology',
        'computer': 'Technology',
        'telecommunication': 'Telecommunications',
        'wireless': 'Telecommunications',
        'bank': 'Banking & Finance',
        'financial': 'Banking & Finance',
        'insurance': 'Insurance',
        'healthcare': 'Healthcare',
        'hospital': 'Healthcare',
        'automobile': 'Automotive',
        'vehicle': 'Automotive',
        'energy': 'Energy',
        'oil': 'Energy',
        'gas': 'Energy',
        'retail': 'Retail',
        'manufacturing': 'Manufacturing',
        'construction': 'Construction',
        'real estate': 'Real Estate',
        'entertainment': 'Entertainment',
        'media': 'Media',
        'airline': 'Aviation',
        'aviation': 'Aviation',
        'agriculture': 'Agriculture',
        'food': 'Food & Beverage',
    }
    
    # Monetary patterns
    MONEY_PATTERN = re.compile(
        r'\$\s*([\d,]+(?:\.\d{2})?)\s*(?:million|billion)?|'
        r'([\d,]+(?:\.\d{2})?)\s*(?:million|billion)?\s*dollars',
        re.I
    )
    
    # Evidence type keywords
    EVIDENCE_KEYWORDS = {
        # Documentary Evidence
        'document': 'Documentary Evidence',
        'documents': 'Documentary Evidence',
        'contract': 'Documentary Evidence',
        'email': 'Documentary Evidence',
        'emails': 'Documentary Evidence',
        'letter': 'Documentary Evidence',
        'memo': 'Documentary Evidence',
        'memorandum': 'Documentary Evidence',
        'record': 'Documentary Evidence',
        'records': 'Documentary Evidence',
        'written agreement': 'Documentary Evidence',
        'invoice': 'Documentary Evidence',
        'receipt': 'Documentary Evidence',
        'financial statement': 'Documentary Evidence',
        'bank statement': 'Documentary Evidence',
        
        # Testimonial Evidence
        'testimony': 'Testimonial Evidence',
        'testified': 'Testimonial Evidence',
        'witness': 'Testimonial Evidence',
        'witnesses': 'Testimonial Evidence',
        'deposition': 'Testimonial Evidence',
        'affidavit': 'Testimonial Evidence',
        'declaration': 'Testimonial Evidence',
        'sworn statement': 'Testimonial Evidence',
        'eyewitness': 'Testimonial Evidence',
        
        # Expert Evidence
        'expert witness': 'Expert Testimony',
        'expert testimony': 'Expert Testimony',
        'expert opinion': 'Expert Testimony',
        'expert report': 'Expert Testimony',
        'forensic': 'Expert Testimony',
        'forensic analysis': 'Expert Testimony',
        'forensic expert': 'Expert Testimony',
        'medical expert': 'Expert Testimony',
        'technical expert': 'Expert Testimony',
        'economist': 'Expert Testimony',
        
        # Physical Evidence
        'physical evidence': 'Physical Evidence',
        'exhibit': 'Physical Evidence',
        'exhibits': 'Physical Evidence',
        'photograph': 'Physical Evidence',
        'photographs': 'Physical Evidence',
        'video': 'Physical Evidence',
        'video recording': 'Physical Evidence',
        'surveillance': 'Physical Evidence',
        'dna': 'Physical Evidence',
        'fingerprint': 'Physical Evidence',
        'weapon': 'Physical Evidence',
        
        # Digital Evidence
        'digital evidence': 'Digital Evidence',
        'electronic record': 'Digital Evidence',
        'electronic records': 'Digital Evidence',
        'metadata': 'Digital Evidence',
        'computer record': 'Digital Evidence',
        'server log': 'Digital Evidence',
        'database': 'Digital Evidence',
        'text message': 'Digital Evidence',
        'social media': 'Digital Evidence',
        'ip address': 'Digital Evidence',
        'electronic communication': 'Digital Evidence',
        
        # Statistical Evidence
        'statistical': 'Statistical Evidence',
        'statistical analysis': 'Statistical Evidence',
        'data analysis': 'Statistical Evidence',
        'regression analysis': 'Statistical Evidence',
        'survey': 'Statistical Evidence',
        'poll': 'Statistical Evidence',
        
        # Circumstantial Evidence
        'circumstantial': 'Circumstantial Evidence',
        'inference': 'Circumstantial Evidence',
        'motive': 'Circumstantial Evidence',
        'opportunity': 'Circumstantial Evidence',
        
        # Character Evidence
        'character evidence': 'Character Evidence',
        'prior conviction': 'Character Evidence',
        'criminal history': 'Character Evidence',
        'reputation': 'Character Evidence',
    }


# ============================================================================
# EXTRACTOR CLASS
# ============================================================================

class LegalCaseExtractor:
    """
    Extracts structured metadata from court case opinions.
    """
    
    def __init__(self):
        self.patterns = LegalPatterns()
    
    def extract(self, text: str) -> CaseMetadata:
        """
        Main extraction method.
        
        Args:
            text: Raw court case opinion text
            
        Returns:
            CaseMetadata object with extracted fields
        """
        metadata = CaseMetadata()
        
        # Normalize text
        text_lower = text.lower()
        
        # Extract all components
        metadata.case_name = self._extract_case_name(text)
        metadata.citation = self._extract_citation(text)
        metadata.date_filed = self._extract_date(text)
        court_info = self._extract_court(text)
        metadata.court_name = court_info[0]
        metadata.jurisdiction_level = court_info[1]
        
        metadata.judges = self._extract_judges(text)
        parties = self._extract_parties(text)
        metadata.plaintiffs = parties['plaintiffs']
        metadata.defendants = parties['defendants']
        counsel = self._extract_counsel(text)
        metadata.counsel_plaintiff = counsel['plaintiff']
        metadata.counsel_defense = counsel['defense']
        
        topics = self._extract_topics(text_lower)
        metadata.primary_topic = topics[0]
        metadata.specific_cause_of_action = topics[1]
        metadata.industry_sector = self._extract_industry(text_lower)
        
        metadata.procedural_posture = self._extract_posture(text_lower)
        metadata.disposition = self._extract_disposition(text_lower)
        metadata.prevailing_party = self._extract_prevailing_party(text, metadata.disposition)
        metadata.monetary_damages = self._extract_damages(text)
        metadata.evidence_types = self._extract_evidence_types(text_lower)
        
        return metadata
    
    def _extract_case_name(self, text: str) -> Optional[str]:
        """Extract case name (e.g., 'Roe v. Wade')."""
        # Method 1: Look for labeled Plaintiff/Defendant pattern
        plaintiff_match = re.search(
            r'([A-Z][^,\n]+?)(?:,\s*(?:a\s+\w+\s+corporation|Inc\.|Corp\.|LLC))?\s*,?\s*\n\s*(?:Plaintiff|Petitioner|Appellant)',
            text, re.I
        )
        defendant_match = re.search(
            r'v\.?\s*\n\s*([A-Z][^,\n]+?)(?:,\s*(?:a\s+\w+\s+corporation|Inc\.|Corp\.|LLC))?\s*,?\s*\n\s*(?:Defendant|Respondent|Appellee)',
            text, re.I
        )
        
        if plaintiff_match and defendant_match:
            plaintiff = plaintiff_match.group(1).strip()
            defendant = defendant_match.group(1).strip()
            # Clean up
            plaintiff = re.sub(r'\s+', ' ', plaintiff).strip(' ,.')
            defendant = re.sub(r'\s+', ' ', defendant).strip(' ,.')
            if len(plaintiff) > 2 and len(defendant) > 2:
                return f"{plaintiff} v. {defendant}"
        
        # Method 2: Look for explicit case caption with v.
        lines = text.split('\n')[:30]  # Check first 30 lines
        
        for line in lines:
            match = self.patterns.CASE_NAME.search(line)
            if match:
                plaintiff = match.group(1).strip()
                defendant = match.group(2).strip()
                # Clean up
                plaintiff = re.sub(r'\s+', ' ', plaintiff).strip(' ,.')
                defendant = re.sub(r'\s+', ' ', defendant).strip(' ,.')
                if len(plaintiff) > 2 and len(defendant) > 2:
                    return f"{plaintiff} v. {defendant}"
        
        return None
    
    def _extract_citation(self, text: str) -> Optional[str]:
        """Extract official reporter citation."""
        for pattern in self.patterns.CITATION_PATTERNS:
            match = pattern.search(text)
            if match:
                # Reconstruct citation based on pattern type
                groups = match.groups()
                full_match = match.group(0)
                return full_match.strip()
        return None
    
    def _extract_date(self, text: str) -> Optional[str]:
        """Extract date and convert to ISO 8601 format."""
        for pattern in self.patterns.DATE_PATTERNS:
            match = pattern.search(text)
            if match:
                date_str = match.group(1)
                try:
                    # Try various date formats
                    for fmt in ['%B %d, %Y', '%B %d %Y', '%m/%d/%Y', '%Y-%m-%d']:
                        try:
                            dt = datetime.strptime(date_str, fmt)
                            return dt.strftime('%Y-%m-%d')
                        except ValueError:
                            continue
                except Exception:
                    pass
        return None
    
    def _extract_court(self, text: str) -> tuple:
        """Extract court name and jurisdiction level."""
        for pattern, template, jurisdiction in self.patterns.COURT_PATTERNS:
            match = pattern.search(text)
            if match:
                if '{}' in template and match.groups():
                    court_name = template.format(match.group(1))
                else:
                    court_name = template
                return (court_name, jurisdiction)
        return (None, None)
    
    def _extract_judges(self, text: str) -> List[str]:
        """Extract list of judges/justices."""
        judges = set()
        
        # Common false positives to filter out
        false_positives = ['court', 'state', 'united', 'this case', 'the case', 'case involves']
        
        for pattern in self.patterns.JUDGE_PATTERNS:
            matches = pattern.findall(text)
            for match in matches:
                name = match.strip() if isinstance(match, str) else match[0].strip()
                # Filter out common false positives
                if len(name) > 3 and not any(x in name.lower() for x in false_positives):
                    judges.add(name)
        
        return list(judges)[:10]  # Limit to 10 judges
    
    def _extract_parties(self, text: str) -> Dict[str, List[Dict]]:
        """Extract plaintiffs and defendants."""
        result = {'plaintiffs': [], 'defendants': []}
        
        # Try to find case name first
        case_name = self._extract_case_name(text)
        if case_name and ' v. ' in case_name:
            parts = case_name.split(' v. ')
            if len(parts) == 2:
                result['plaintiffs'].append({
                    'name': parts[0].strip(),
                    'type': self._classify_party_type(parts[0])
                })
                result['defendants'].append({
                    'name': parts[1].strip(),
                    'type': self._classify_party_type(parts[1])
                })
        
        return result
    
    def _classify_party_type(self, name: str) -> str:
        """Classify party as Individual, Corporation, or Government."""
        name_lower = name.lower()
        
        # Government indicators
        gov_keywords = ['united states', 'state of', 'city of', 'county of', 
                       'department', 'agency', 'commission', 'board', 'authority',
                       'secretary', 'attorney general', 'commissioner']
        if any(kw in name_lower for kw in gov_keywords):
            return 'Government'
        
        # Corporation indicators
        corp_keywords = ['inc', 'corp', 'llc', 'llp', 'ltd', 'company', 'co.',
                        'corporation', 'incorporated', 'limited', 'partners',
                        'association', 'foundation', 'group', 'holdings']
        if any(kw in name_lower for kw in corp_keywords):
            return 'Corporation'
        
        return 'Individual'
    
    def _extract_counsel(self, text: str) -> Dict[str, List[str]]:
        """Extract counsel for plaintiff and defense."""
        result = {'plaintiff': [], 'defense': []}
        
        # Look for "for plaintiff" or "for petitioner"
        plaintiff_pattern = re.compile(
            r'(?:for\s+(?:the\s+)?(?:plaintiff|petitioner|appellant)[s]?)[\s:,]+([A-Z][a-zA-Z\.\s,&]+?)(?:\.|;|\n|for\s+(?:the\s+)?(?:defendant|respondent))',
            re.I | re.DOTALL
        )
        match = plaintiff_pattern.search(text)
        if match:
            names = self._parse_attorney_names(match.group(1))
            result['plaintiff'] = names
        
        # Look for "for defendant" or "for respondent"
        defense_pattern = re.compile(
            r'(?:for\s+(?:the\s+)?(?:defendant|respondent|appellee)[s]?)[\s:,]+([A-Z][a-zA-Z\.\s,&]+?)(?:\.|;|\n|$)',
            re.I | re.DOTALL
        )
        match = defense_pattern.search(text)
        if match:
            names = self._parse_attorney_names(match.group(1))
            result['defense'] = names
        
        return result
    
    def _parse_attorney_names(self, text: str) -> List[str]:
        """Parse attorney names from a text block."""
        names = []
        # Split by common delimiters
        parts = re.split(r'[;,]|\band\b', text)
        for part in parts:
            part = part.strip()
            if len(part) > 3 and not part.lower().startswith(('for ', 'the ')):
                # Clean up
                part = re.sub(r'\s+', ' ', part).strip()
                if part:
                    names.append(part)
        return names[:5]  # Limit to 5 attorneys per side
    
    def _extract_topics(self, text_lower: str) -> tuple:
        """Extract primary topic and specific cause of action."""
        for keyword, (topic, cause) in self.patterns.TOPIC_KEYWORDS.items():
            if keyword in text_lower:
                return (topic, cause)
        return (None, None)
    
    def _extract_industry(self, text_lower: str) -> Optional[str]:
        """Infer industry sector from text."""
        for keyword, industry in self.patterns.INDUSTRY_KEYWORDS.items():
            if keyword in text_lower:
                return industry
        return None
    
    def _extract_posture(self, text_lower: str) -> Optional[str]:
        """Extract procedural posture."""
        for keyword, posture in self.patterns.POSTURE_KEYWORDS.items():
            if keyword in text_lower:
                return posture
        return None
    
    def _extract_disposition(self, text_lower: str) -> Optional[str]:
        """Extract court's disposition."""
        # Look for disposition near the end of the document
        last_section = text_lower[-2000:]  # Last 2000 characters
        
        for keyword, disposition in self.patterns.DISPOSITION_KEYWORDS.items():
            if keyword in last_section:
                return disposition
        
        # Also check full text for explicit judgment statements
        for keyword, disposition in self.patterns.DISPOSITION_KEYWORDS.items():
            pattern = re.compile(rf'(?:judgment|order|decision)\s+(?:is\s+)?{keyword}', re.I)
            if pattern.search(text_lower):
                return disposition
        
        return None
    
    def _extract_prevailing_party(self, text: str, disposition: Optional[str]) -> Optional[str]:
        """Determine the prevailing party."""
        text_lower = text.lower()
        last_section = text_lower[-2000:]
        
        # Check for explicit statements
        if 'plaintiff prevails' in last_section or 'judgment for plaintiff' in last_section:
            return 'Plaintiff'
        if 'defendant prevails' in last_section or 'judgment for defendant' in last_section:
            return 'Defendant'
        
        # Infer from disposition
        if disposition:
            # In appeals context
            if 'appellant' in text_lower[:1000]:  # If plaintiff was appellant
                if disposition in ['Reversed', 'Vacated', 'Reversed in Part']:
                    return 'Plaintiff'
                elif disposition in ['Affirmed', 'Dismissed']:
                    return 'Defendant'
            # In trial context
            if disposition in ['Granted']:
                # Check what was granted
                if 'motion to dismiss' in text_lower:
                    return 'Defendant'
                if 'summary judgment' in text_lower:
                    return 'Mixed'  # Need more context
        
        return None
    
    def _extract_damages(self, text: str) -> Optional[float]:
        """Extract monetary damages amount."""
        matches = self.patterns.MONEY_PATTERN.findall(text)
        
        max_amount = None
        for match in matches:
            amount_str = match[0] or match[1]
            if amount_str:
                try:
                    amount = float(amount_str.replace(',', ''))
                    # Check for million/billion
                    context = text[max(0, text.find(amount_str)-50):text.find(amount_str)+50].lower()
                    if 'billion' in context:
                        amount *= 1_000_000_000
                    elif 'million' in context:
                        amount *= 1_000_000
                    
                    if max_amount is None or amount > max_amount:
                        max_amount = amount
                except ValueError:
                    continue
        
        return max_amount
    
    def _extract_evidence_types(self, text_lower: str) -> List[str]:
        """Extract types of evidence presented in the case."""
        evidence_found = set()
        
        for keyword, evidence_type in self.patterns.EVIDENCE_KEYWORDS.items():
            if keyword in text_lower:
                evidence_found.add(evidence_type)
        
        return sorted(list(evidence_found))


# ============================================================================
# MAIN INTERFACE
# ============================================================================

def extract_case_metadata(text: str) -> str:
    """
    Main entry point for case metadata extraction.
    
    Args:
        text: Raw court case opinion text
        
    Returns:
        JSON string with extracted metadata
    """
    extractor = LegalCaseExtractor()
    metadata = extractor.extract(text)
    return metadata.to_json()


def process_file(filepath: str) -> str:
    """
    Process a case file and return JSON metadata.
    
    Args:
        filepath: Path to text file containing case opinion
        
    Returns:
        JSON string with extracted metadata
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    return extract_case_metadata(text)


# ============================================================================
# CLI INTERFACE
# ============================================================================

if __name__ == '__main__':
    import sys
    
    print("=" * 70)
    print("  LEGAL CASE METADATA EXTRACTOR")
    print("  Jurimetric Analysis Tool v1.0")
    print("=" * 70)
    
    if len(sys.argv) > 1:
        # Process file from command line
        filepath = sys.argv[1]
        print(f"\nProcessing: {filepath}")
        result = process_file(filepath)
        print("\nExtracted Metadata:")
        print(result)
    else:
        # Demo mode with sample text
        sample_text = """
        SUPREME COURT OF THE UNITED STATES
        
        No. 410 U.S. 113
        
        ROE v. WADE
        
        APPEAL FROM THE UNITED STATES DISTRICT COURT FOR THE 
        NORTHERN DISTRICT OF TEXAS
        
        Argued December 13, 1971 — Decided January 22, 1973
        
        Before BURGER, C.J., and DOUGLAS, BRENNAN, STEWART, WHITE, 
        MARSHALL, BLACKMUN, POWELL, and REHNQUIST, JJ.
        
        BLACKMUN, J., delivered the opinion of the Court.
        
        Sarah Weddington argued for the plaintiff.
        Jay Floyd argued for the defendant.
        
        This case involves a challenge to the Texas criminal abortion statutes...
        The constitutional right to privacy extends to a woman's decision 
        whether or not to terminate her pregnancy...
        
        We, therefore, conclude that the right of personal privacy includes 
        the abortion decision, but that this right is not unqualified...
        
        Reversed and remanded.
        """
        
        print("\n[DEMO MODE - Using sample case text]")
        print("-" * 70)
        result = extract_case_metadata(sample_text)
        print("\nExtracted Metadata:")
        print(result)
        
        print("\n" + "-" * 70)
        print("Usage: python legal_case_extractor.py <path_to_case_file.txt>")
        print("-" * 70)

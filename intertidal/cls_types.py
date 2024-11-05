from django.db import models

class ClsTypes(models.TextChoices):
    ARTICLE = "article", "Article"
    ARTICLE_JOURNAL = "article_journal", "Article Journal"
    ARTICLE_MAGAZINE = "article_magazine", "Article Magazine"
    ARTICLE_NEWSPAPER = "article_newspaper", "Article Newspaper"
    BILL = "bill", "Bill"
    BOOK = "book", "Book"
    BROADCAST = "broadcast", "Broadcast"
    CHAPTER = "chapter", "Chapter"
    CLASSIC = "classic", "Classic"
    COLLECTION = "collection", "Collection"
    DATASET = "dataset", "Dataset"
    DOCUMENT = "document", "Document"
    ENTRY = "entry", "Entry"
    ENTRY_DICTIONARY = "entry_dictionary", "Entry Dictionary"
    ENTRY_ENCYCLOPEDIA = "entry_encyclopedia", "Entry Encyclopedia"
    EVENT = "event", "Event"
    FIGURE = "figure", "Figure"
    GRAPHIC = "graphic", "Graphic"
    HEARING = "hearing", "Hearing"
    INTERVIEW = "interview", "Interview"
    LEGAL_CASE = "legal_case", "Legal Case"
    LEGISLATION = "legislation", "Legislation"
    MANUSCRIPT = "manuscript", "Manuscript"
    MAP = "map", "Map"
    MOTION_PICTURE = "motion_picture", "Motion Picture"
    MUSICAL_SCORE = "musical_score", "Musical Score"
    PAMPHLET = "pamphlet", "Pamphlet"
    PAPER_CONFERENCE = "paper_conference", "Paper Conference"
    PATENT = "patent", "Patent"
    PERFORMANCE = "performance", "Performance"
    PERIODICAL = "periodical", "Periodical"
    PERSONAL_COMMUNICATION = "personal_communication", "Personal Communication"
    POST = "post", "Post"
    POST_WEBLOG = "post_weblog", "Post Weblog"
    REGULATION = "regulation", "Regulation"
    REPORT = "report", "Report"
    REVIEW = "review", "Review"
    REVIEW_BOOK = "review_book", "Review Book"
    SOFTWARE = "software", "Software"
    SONG = "song", "Song"
    SPEECH = "speech", "Speech"
    STANDARD = "standard", "Standard"
    THESIS = "thesis", "Thesis"
    TREATY = "treaty", "Treaty"
    WEBPAGE = "webpage", "Webpage"

import sqlite3

from clinical_trials_gov_data.data_extraction.protcol_extractor import ProtocolExtractor


def build_processed_studies_set(
    data: dict, extract_protocol_text: bool = True
) -> list[ProtocolExtractor]:
    processed_studies = [
        ProtocolExtractor(study, extract_protocol_text=extract_protocol_text)
        for study in data
    ]
    return processed_studies


def _list_to_text(lst: list[str], sep: str = " | ") -> str:
    return f"{sep}".join(str(e) for e in lst)


def build_db_cursor(db_path: str):
    db_connection = sqlite3.connect(db_path)
    db_cursor = db_connection.cursor()
    return db_cursor, db_connection


def create_study_database(db_cursor: sqlite3.Cursor):
    # Create table for General study info
    db_cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS studies
        (
            study_id TEXT PRIMARY KEY,
            conditions TEXT,
            short_description TEXT,
            long_description TEXT,
            protocol_url TEXT,
            status TEXT
        ) WITHOUT ROWID"""
    )

    # Create table for study design
    db_cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS study_design
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            study_id TEXT,
            study_type TEXT,
            phases TEXT,
            allocation TEXT,
            enrollment_target INTEGER,
            FOREIGN KEY (study_id) REFERENCES STUDIES(study_id)
        ) """
    )


def build_db_tuples(processed_studies: list[ProtocolExtractor]) -> tuple:
    # TODO -> this function should be separate by table without damaging performance
    # first create data tuples
    studies_sql_tuples: list = []
    study_design_sql_tuples: list = []

    for ps in processed_studies:
        studies_tuple = (
            ps.study_id,
            _list_to_text(ps.study_conditions),
            ps.study_short_description,
            ps.study_description,
            _list_to_text(ps.protocol_urls),
            ps.study_status,
        )
        # append necessary data to the study tuples
        studies_sql_tuples.append(studies_tuple)
        # now get the data for the design
        # extract design info for handling
        design_study_info = ps.study_design
        phases = _list_to_text(design_study_info.get("phases", []))
        alloc_info = design_study_info.get("designInfo", {}).get("allocation")
        # Get enrolment target
        enrollment_target = design_study_info.get("enrollmentInfo", {}).get("count")

        study_design_tuple = (
            ps.study_id,
            design_study_info.get("studyType", ""),
            phases,
            alloc_info,
            enrollment_target,
        )

        study_design_sql_tuples.append(study_design_tuple)

    return (studies_sql_tuples, study_design_sql_tuples)

from clinical_trials_gov_data.data_extraction.create_sqlite import (
    build_db_cursor,
    create_study_database,
    build_db_tuples,
    build_processed_studies_set,
)

from clinical_trials_gov_data.data_extraction.extract_protocol_text import (
    extract_pdfs_parallel,
)

# TODO -> split what's under if __name... to functions and add a main()

if __name__ == "__main__":
    import json

    data_path = "./data/raw/ctg-studies.json"
    db_file_path = "./data/processed/study_protocols.db"
    protocol_text_json_path = "./data/processed/procotol_text_json.json"

    N = 20  # sample of studies -> this can be removed by I leave for testing
    # load the data
    with open(data_path) as json_file:
        data = json.load(json_file)
        data = data["studies"]

    print("creating Data Base")
    # build db connection
    db_cursor, db_connection = build_db_cursor(db_file_path)
    # Create the DB
    create_study_database(db_cursor)
    print("DB created")
    # Get the data in the right format
    # Extract protocol text requires connection to the internet
    # Warning -> Remove the [: N] if you want to run in the whole set
    processed_studies = build_processed_studies_set(
        data[:N], extract_protocol_text=True
    )
    # populate the tuples
    studies_sql_tuples, study_design_sql_tuples = build_db_tuples(processed_studies)
    print(f"Adding data to DB at {db_file_path}")
    # finally, add the data
    # TODO -> create a function for this??
    db_cursor.executemany(
        """
        REPLACE INTO Studies (
            study_id,
            conditions,
            short_description,
            long_description,
            protocol_url,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """,
        studies_sql_tuples,
    )

    db_cursor.executemany(
        """
        REPLACE INTO Study_design (
            study_id,
            study_type,
            phases,
            allocation,
            enrollment_target
        )
        VALUES (?, ?, ?, ?, ?)
    """,
        study_design_sql_tuples,
    )

    db_connection.commit()
    db_connection.close()
    print("Data Added into DB")

    # Now get the protocol text from the internet
    print("Extracting texts from protocol's urls")
    procotol_txt_json = extract_pdfs_parallel(processed_studies)
    # Save the output json
    with open(protocol_text_json_path, "w") as f:
        json.dump(procotol_txt_json, f, indent=4)
    print(f"Protocol Text Json File saved at {protocol_text_json_path}")

import concurrent.futures
from clinical_trials_gov_data.data_extraction.protcol_extractor import ProtocolExtractor


# This function creates a simple JSON object that includes the Protocol text.


def _extract_studies_protocols(protocol_extractor_obj: ProtocolExtractor):
    try:
        study_data: dict = {}
        # Build the ProtocolExtractor object
        study_data[protocol_extractor_obj.study_id] = {
            "conditions": protocol_extractor_obj.study_conditions,
            "description": protocol_extractor_obj.study_description,
            "protocol_text": protocol_extractor_obj._protocol_text_dict,
        }
    except Exception as e:
        study_id = protocol_extractor_obj.study_id
        # if information found return nctID
        print(f"Failed extracting Protocol data for {study_id}", e)

    return study_data


def extract_pdfs_parallel(processed_studies: list[ProtocolExtractor]):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Create futures that will be processed by multi-thread
        futures = {
            executor.submit(_extract_studies_protocols, study)
            for study in processed_studies
        }
        results = {}
        for future in concurrent.futures.as_completed(futures):
            try:
                # Get the results. This will create the data result dict
                study_data = future.result()
                results.update(study_data)
            except Exception as e:
                print("Failed to extract Protocol", e)
    return results

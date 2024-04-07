import requests
from dataclasses import dataclass

import io
import PyPDF2


@dataclass
class ProtocolExtractor:
    BASE_URL = "https://cdn.clinicaltrials.gov/large-docs/"

    def __init__(self, study_data: dict[str, str], extract_protocol_text: bool = False):
        self.study_data = study_data
        self.study_id = self._getstudy_id
        self.study_conditions = self._get_study_condition
        self.study_description = self._get_study_long_description
        self.study_design = self._get_study_design
        self.study_short_description = self._get_study_short_description
        self.protocol_urls = self._build_study_url
        self.study_status = self._get_study_status

        # init protocol text dict.
        # If extract_protocol_text is true, download it from urls.
        self._protocol_text_dict = {}
        # extract the text from the online PDFS
        if extract_protocol_text:
            self._protocol_text_dict = self._get_protocol_text()

    @property
    def _getstudy_id(self) -> str | None:
        # Get ID information
        id_info = self.study_data.get("protocolSection").get("identificationModule")
        # if information found return nctID
        if id_info:
            return id_info.get("nctId")

    @property
    def _get_study_status(self) -> str | None:
        protocol_info = self.study_data.get("protocolSection")
        # Get condition info
        condition_info = protocol_info.get("statusModule").get("overallStatus")
        return condition_info

    @property
    def _get_study_condition(self) -> str | None:
        protocol_info = self.study_data.get("protocolSection")
        # Get condition info
        condition_info = protocol_info.get("conditionsModule").get("conditions")
        return condition_info

    @property
    def _get_study_long_description(self) -> str:
        description = ""
        protocol_info = self.study_data.get("protocolSection")
        for section in ["briefSummary", "detailedDescription"]:
            description = (
                description
                + "\n"
                + protocol_info.get("descriptionModule").get(section, "")
            )

        return description

    @property
    def _get_study_short_description(self) -> str:
        description = ""
        protocol_info = self.study_data.get("protocolSection")
        # get the short description if added.
        description = (
            description
            + "\n"
            + protocol_info.get("descriptionModule").get("briefSummary", "")
        )

        return description

    @property
    def _build_study_url(self) -> list[str]:
        urls: list[str] = []  # set by default a blank url
        if "documentSection" in self.study_data and self.study_id:
            document_section = self.study_data.get("documentSection")

            for document in document_section.get("largeDocumentModule").get(
                "largeDocs"
            ):
                if document.get("hasProtocol"):  # If HasProtocol is True, then get it
                    doc_name = document.get("filename")
                    # Build the url
                    url = f"{self.BASE_URL}{self.study_id[-2:]}/{self.study_id}/{doc_name}"
                    urls.append(url)
        return urls

    @property
    def _get_eligibility_criteria(self) -> dict[str, str]:
        protocol_info = self.study_data.get("protocolSection")

        return protocol_info.get("eligibilityModule")

    @property
    def _get_study_design(self) -> dict | None:
        protocol_info = self.study_data.get("protocolSection")
        design_info = protocol_info.get("designModule")
        return design_info

    @staticmethod
    def _extract_text_from_pdf_url(url: str) -> str:
        """Wrapper for the PyPDF2.Reader

        Extracts the text from an online pdf from a url
        provided.

        Args:
            url (str): URL of the pdf

        Returns:
            str: Protocol Text if found.
        """
        text: str = ""
        try:
            r = requests.get(url)
            f = io.BytesIO(r.content)

            reader = PyPDF2.PdfReader(f)
            pages = reader.pages
            # get all pages data
            text = "\n".join([page.extract_text() for page in pages])
        except Exception as e:
            print(f"Problem extracting text from {url}", e)
        return text

    def _get_protocol_text(self) -> dict:
        text_dict: dict[str, str] = {}
        if len(self.protocol_urls) > 0:
            for url in self.protocol_urls:
                text_dict[url] = ProtocolExtractor._extract_text_from_pdf_url(url)

        return text_dict

    def info(self):
        print(f"Study ID: {self.study_id}")
        print(f" Condition: {self._study_conditions}")
        print(f" urls: {self.protocol_urls} ")

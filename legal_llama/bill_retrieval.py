import requests
import streamlit as st
import xml.etree.ElementTree as ET


class BillRetriever:
    """
    A class used to retrieve bills using the ProPublica Congress API & United States Congress API.
    """
    PROPUBLICA_URL = "https://api.propublica.org/congress/v1/bills/search.json"
    CONGRESS_URL_BASE = "https://api.congress.gov/v3/bill/{congress}/{billType}/{billNumber}/text"

    def __init__(self, api_key=None):
        """
        Initialize the BillRetriever with API keys.

        Parameters:
            api_key (str, optional): The API key to be used for authentication. Default is None.
        """
        self.pro_publica_api_key = st.secrets["PRO_PUBLICA_API_KEY"]
        self.congress_api_key = st.secrets["CONGRESS_API_KEY"]

    def make_api_call(self, api_url, api_key, params=None):
        """
        Make an API call to the specified URL with optional parameters and API key.

        Parameters:
            api_url (str): The URL of the API endpoint.
            api_key (str): The API Key for the API
            params (dict, optional): Optional parameters to pass with the API call. Default is None.

        Returns:
            dict: JSON response data if the request is successful, None otherwise.
        """
        headers = {"X-API-Key": api_key} if api_key else {}

        try:
            response = requests.get(api_url, params=params, headers=headers)
            response.raise_for_status()  # Raise an exception for non-2xx status codes
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error occurred: {e}")
            return None
        except ValueError as e:
            print(f"Invalid response received: {e}")
            return None

    def search_bill_propublica(self, query):
        """
        Search for a bill using the ProPublica Congress API.

        Parameters:
            query (str): The query string to search for.

        Returns:
            dict: JSON response data if the request is successful, None otherwise.
        """
        params = {"query": query, "sort": "date", "dir": "desc"}
        return self.make_api_call(self.PROPUBLICA_URL, params=params, api_key=self.pro_publica_api_key)

    def get_bill_text_congress(self, congress, bill_type, bill_number):
        """
        Retrieve the text of a bill using the Congress API.

        Parameters:
            congress (str): The number of the congress.
            bill_type (str): The type of the bill.
            bill_number (str): The number of the bill.

        Returns:
            dict: JSON response data if the request is successful, None otherwise.
        """
        url = self.CONGRESS_URL_BASE.format(congress=congress, billType=bill_type, billNumber=bill_number)
        return self.make_api_call(url, api_key=self.congress_api_key)

    def get_bill_by_query(self, query):
        """
        Search for a bill by query and retrieve its text.

        Parameters:
            query (str): The query string to search for.

        Returns:
            str: The text of the bill if the request is successful, None otherwise.
        """
        # First search for the bill using the ProPublica API
        propublica_data = self.search_bill_propublica(query)
        if propublica_data and 'results' in propublica_data:
            # Iterate over the list of bills, till we find the bill which has text available on Congress Website
            for bill_data in propublica_data['results'][0]['bills']:
                congress = bill_data['bill_id'].split('-')[1]
                bill_type = bill_data['bill_type']
                bill_number = bill_data['number'].split('.')[-1]

                # Then get the text of the bill using the Congress API
                congress_data = self.get_bill_text_congress(congress, bill_type, bill_number)
                if congress_data and 'textVersions' in congress_data and congress_data['textVersions']:
                    # Check if textVersions list is not empty
                    xml_url = congress_data['textVersions'][0]['formats'][2]['url']
                    return self.extract_bill_text(xml_url)
        return None

    def extract_bill_text(self, url):
        """
        Extract the text content from a bill's XML data.

        Parameters:
            url (str): The URL of the bill's XML data.

        Returns:
            str: The text content of the bill.
        """
        # Get the XML data from the URL
        try:
            xml_data = requests.get(url).content
        except requests.exceptions.RequestException as e:
            print(f"Error occurred: {e}")
            return None

        # Decode bytes to string and parse XML
        try:
            root = ET.fromstring(xml_data.decode('utf-8'))
        except ET.ParseError as e:
            print(f"Error parsing XML: {e}")
            return None

        return self.get_all_text(root)

    @staticmethod
    def get_all_text(element):
        """
        Recursively extract text from an XML element and its children.

        Parameters:
            element (xml.etree.ElementTree.Element): An XML element.

        Returns:
            str: The concatenated text from the element and its children.
        """
        text = element.text or ''  # Get the text of the current element, if it exists
        for child in element:
            text += BillRetriever.get_all_text(child)  # Recursively get the text of all child elements
            if child.tail:
                text += child.tail  # Add any trailing text of the child element
        return text

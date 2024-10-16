PRODUCT_DETAILS_MAP = {
    "Reg 29 Addressee Tracker Database": {
        "path": "src/analyse/counts/data/sent/sent_to_yearly.csv",
        "features": [
            "Track PFDs addressed to specific organisations",
            "Access over a decade of data, since July 2013",
            "Explore if organisations have responded to PFDs",
        ],
        "description": "download of the latest version of the Preventable Deaths Tracker's Regulation 29 Addressee "
                       "Tracker Database. This database tracks who has been addressed PFDs since 2013",
    },
    "Coroner Area Tracker Database": {
        "path": "src/analyse/counts/data/sent/area-statuses.csv",
        "features": [
            "Track the number of PFDs published in specific coroners' areas",
            "Access over a decade of data, since July 2013",
            "Explore if PFDs have responses published",
        ],
        "description": "download of the latest version of data from the Preventable Deaths Tracker by coroners' "
                       "areas since July 2013",
    },
    "Coroner Tracker Database": {
        "path": "src/analyse/counts/data/sent/name-statuses.csv",
        "features": [
            "Track the number of PFDs published by individual coroners",
            "Access over a decade of data, since July 2013",
            "Explore if PFDs have responses published",
        ],
        "description": "download of the latest version of data from the Preventable Deaths Tracker by coroners' "
                       "names since July 2013",
    },
    "Data by the Judiciary's PFD report type": {
        "path": "src/analyse/counts/data/category/category-years.csv",
        "features": [
            "Track how PFDs are categorised on the Judiciary's website",
            "Access over a decade of data, since July 2013",
            "Analyse categories overtime by year of report",
        ],
        "description": "download of the latest version of data from the Preventable Deaths Tracker for PFDs by "
                       "category (i.e. the Judiciary's PFD report type) over time since July 2013",
    },
    "Reg 28 Reports Tracker Database": {
        "path": "src/analyse/counts/data/sent/database.csv",
        "features": [
            "Track the number of PFDs published on the Judiciary website every week",
            "Access over a decade of data, since July 2013",
            "Explore if PFDs have responses published",
        ],
        "description": "download of the latest version of the Preventable Deaths Tracker Regulation 28 Reports "
                       "Tracker Database. This database collects all published PFDs from the Judiciary website "
                       "since 2013 and corrects the data so it's ready for analysis",
    },
    "One month - Reg 28 Reports Tracker": {
        "path": "src/analyse/counts/data/sent/last_month_reports.csv",
        "features": [
            "Track the number of PFDs published on the Judiciary website every week",
            "Access the last month of data",
            "Explore if PFDs have responses published",
        ],
        "description": "download the last month of data from the Preventable Deaths Tracker Regulation 28 Reports "
                       "Database, which collects coroners' PFDs published on the Judiciary website and corrects the "
                       "data so it's ready for analysis",
    },
    "3 months of the Reg 28 Reports Tracker Database": {
        "path": "src/analyse/counts/data/sent/last_quarter_reports.csv",
        "features": [
            "Track the number of PFDs published on the Judiciary website every week",
            "Access the last quarter of data",
            "Explore if PFDs have responses published",
        ],
        "description": "download the last quarter of data (i.e. 3 months) from the Preventable Deaths Tracker "
                       "Regulation 28 Reports Database, which collects coroners' PFDs published on the Judiciary "
                       "website and corrects the data so it's ready for analysis",
    },
    "Reg 28 Database - Overdue responses": {
        "path": "src/analyse/counts/data/sent/reg28_by_status/overdue.csv",
        "features": [
            "Track the number of PFDs that have overdue responses",
            "Understand the number of days each report is overdue",
            "Access over a decade of data, collated since July 2013",
            "Use the most up-to-date information, with updates every Sunday!"
        ],
        "description": "",  # TODO: add description
    },
    "Reg 28 Database - Pending responses only": {
        "path": "src/analyse/counts/data/sent/reg28_by_status/pending.csv",
        "features": [
            "Track the number of PFDs that have upcoming responses due",
            "Understand the number of days left until a response is due",
            "Access over a decade of data, collated since July 2013",
            "Use the most up-to-date information, with updates every Sunday!"
        ],
        "description": "",  # TODO: add description
    },
    "Reg 28 Database - Completed responses only": {
        "path": "src/analyse/counts/data/sent/reg28_by_status/completed.csv",
        "features": [
            "Track the number of PFDs that have all published responses",
            "Access over a decade of data, collated since July 2013",
            "Use the most up-to-date information, with updates every Sunday!"
        ],
        "description": "",  # TODO: add description
    },
}

SUPPORT_EMAIL = "georgiarichardscebm@gmail.com"
WEBSITE_URL = "https://preventabledeathstracker.net/"
DESCRIPTION_KEY = "description"
FEATURES_KEY = "features"
PATH_KEY = "path"
LOGO_PATH = (
    "https://substack-post-media.s3.amazonaws.com/public/images/30d9b718-f65e-4e04-bac5-73e5b0cb3c4c_1280x224.png"
)

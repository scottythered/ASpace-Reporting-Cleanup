# ArchivesSpace Reporting and Cleanup Python Scripts

To run these scripts, you will need the following libraries installed:
* [ArchivesSnake](https://github.com/archivesspace-labs/ArchivesSnake)
* [Pandas](https://pandas.pydata.org/)
* [TQDM](https://github.com/tqdm/tqdm)


You will also need to edit the script with your credentials here:
```
client = ASnakeClient(baseurl='xxx',
                      username='xxx',
                      password='xxx')
```
Includes:
* **accessions_reporting.py**: reports the physical extent of a local ASpace instance's Accessions entered in a fiscal year as a CSV file. (This goes by the creation date of the record, not the accession identifier itself.)
* **legacy_html_hunter.py**: reports the presence of bracketed HTML code in resource record titles, object record titles, and notes texts as CSV files.
* **location_grabber.py**: reports the high level storage locations for each collection in a local ASpace instance as a CSV file. The report is a master list detailing which collections are stored where (for example, on-site vs local storage vs Iron Mountain), as well as determines if the finding aid  includes that data correctly in the "Conditions Governing Access" field.
* See also **[Aspace Comma Endings](https://github.com/scottythered/aspace-comma-endings)**: looks for resource/digital object titles that end with a comma and changes all of the matching titles found.

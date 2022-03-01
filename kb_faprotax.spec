/*
A KBase module: kb_faprotax
*/

module kb_faprotax {
    typedef structure {
        string report_name;
        string report_ref;
    } ReportResults;

    funcdef run_amplicon_workflow(mapping<string,UnspecifiedObject> params) returns (ReportResults output) authentication required;

    funcdef run_genome_workflow(mapping<string,UnspecifiedObject> params) returns (ReportResults output) authentication required;
};

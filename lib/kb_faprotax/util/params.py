import json


class Params:

    def __init__(self, params):
        self.params = params
        self.validate()
        self.set_defaults()

    def __getitem__(self, key):
        return self.params[key]

    def validate(self):
        # TODO use jsonschema
        for p in self.params:
            if p not in self.VALID:
                raise Exception(f"Unknown param {p}")

    def set_defaults(self):
        for k, v in self.DEFAULTS.items():
            self.params.setdefault(k, v)

    def __repr__(self) -> str:
        return (
            "Wrapper for params:\n%s" % (json.dumps(self.params, indent=4))
        )


class AmpliconWorkflowParams(Params):

    DEFAULTS = {}
    VALID = [
        "input_upa",
        "tax_field",
        "output_amplicon_matrix_name",
        # ---
        "workspace_id",
        "workspace_name",
    ]

    def __init__(self, params):
        super().__init__(params)
        self.custom_transform()

    def custom_transform(self):
        if isinstance(self.params["tax_field"], list):
            self.params["tax_field"] = self.params["tax_field"][0]


class GenomeWorkflowParams(Params):

    DEFAULTS = {}
    VALID = [
        "input_upa",
        # ---
        "workspace_id",
        "workspace_name",
    ]

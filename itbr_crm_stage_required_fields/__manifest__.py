{
    "name": "IT Brasil CRM Stage Required Fields",
    "summary": "Required fields to change stage in CRM",
    "version": "1.0.0",
    "category": "Technical",
    "license": "LGPL-3",
    "author": "IT Brasil",
    "website": "https://www.itbrasil.com.br",
    "depends": ["crm", "crm_security_group"],
    "data": [
        "security/ir.model.access.csv",
        "views/crm_stage_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}

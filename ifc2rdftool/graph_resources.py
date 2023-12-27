# pylint: disable=C0114

from rdflib import Namespace

# URI's
LIFECYCLE_URI = "https://w3id.org/digitalconstruction/0.5/Lifecycle#"
INSTANCE_URI = "https://w3id.org/digitalconstruction/instance#"
BOT_URI = "https://w3id.org/bot#"
GEO_URI = "http://www.w3.org/2003/01/geo/wgs84_pos#"
XSD_URI = "http://www.w3.org/2001/XMLSchema#"

# Namespaces
LIFECYCLE_NAMESPACE = Namespace(LIFECYCLE_URI)
INSTANCE_NAMESPACE = Namespace(INSTANCE_URI)
BOT_NAMESPACE = Namespace(BOT_URI)
GEO_NAMESPACE = Namespace(GEO_URI)

# Prefixes
PREFIXES = f"""
    @prefix dicl: <{LIFECYCLE_URI}> .
    @prefix inst: <{INSTANCE_URI}> .
    @prefix bot: <{BOT_URI}> .
    @prefix geo: <{GEO_URI}> .
    @prefix xsd: <{XSD_URI}> .
"""

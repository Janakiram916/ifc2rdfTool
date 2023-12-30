# pylint: disable=C0114

from rdflib import Namespace

# URI's
LIFECYCLE_URI = "https://w3id.org/digitalconstruction/0.5/Lifecycle#"
CORE_URI = "https://w3id.org/digitalconstruction/core#"
INSTANCE_URI = "https://w3id.org/digitalconstruction/instance#"
BOT_URI = "https://w3id.org/bot#"
GEO_URI = "http://www.w3.org/2003/01/geo/wgs84_pos#"
XSD_URI = "http://www.w3.org/2001/XMLSchema#"
BEO_URI = "https://pi.pauwel.be/voc/buildingelement#"
DICM_URI = "https://w3id.org/digitalconstruction/0.5/Materials#"
DICV_URI = "https://w3id.org/digitalconstruction/0.5/Variables#"

# Namespaces
CORE_NAMESPACE = Namespace(CORE_URI)
LIFECYCLE_NAMESPACE = Namespace(LIFECYCLE_URI)
INSTANCE_NAMESPACE = Namespace(INSTANCE_URI)
BOT_NAMESPACE = Namespace(BOT_URI)
GEO_NAMESPACE = Namespace(GEO_URI)
BEO_NAMESPACE = Namespace(BEO_URI)
DICM_NAMESPACE = Namespace(DICM_URI)
DICV_NAMESPACE = Namespace(DICV_URI)

# Prefixes
PREFIXES = f"""
    @prefix core: <{CORE_URI}> .
    @prefix inst: <{INSTANCE_URI}> .
    @prefix bot: <{BOT_URI}> .
    @prefix geo: <{GEO_URI}> .
    @prefix xsd: <{XSD_URI}> .
    @prefix beo: <{BEO_URI}> .
    @prefix dicm: <{DICM_URI}> .
    @prefix dicv: <{DICV_URI}> .
"""

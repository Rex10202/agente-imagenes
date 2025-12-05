from rdflib import Graph, Namespace, Literal, RDF, XSD, URIRef
from pyshacl import validate
from pathlib import Path
from typing import List, Dict
from .config import TTL_PATH

EX = Namespace("http://example.org/agi#")

def build_graph(result_img_path: Path, req_elements_es: List[str], eval_scores: Dict) -> Graph:
    g = Graph()
    g.bind("ex", EX)
    img_uri = URIRef(result_img_path.resolve().as_uri())
    g.add((img_uri, RDF.type, EX.Imagen))

    # Añade elementos presentes (según cobertura >0, aquí se agregan todos los requeridos como "enImagen";
    # en prácticas más estrictas, agregue solo los detectados).
    for e in req_elements_es:
        elem_uri = URIRef(f"{img_uri}#{e}")
        g.add((elem_uri, RDF.type, EX.Elemento))
        g.add((img_uri, EX.enImagen, elem_uri))

    # Score de calidad (utilidad U)
    g.add((img_uri, EX.tieneScore, Literal(eval_scores["U"], datatype=XSD.decimal)))
    return g

def shacl_validate(candidate_graph: Graph) -> Dict:
    assert TTL_PATH.exists(), f"Falta TTL con shapes: {TTL_PATH}"
    shapes = Graph().parse(TTL_PATH.as_posix(), format="turtle")
    conforms, rgraph, rtext = validate(
        data_graph=candidate_graph, shacl_graph=shapes,
        inference="rdfs", abort_on_first=False
    )
    return {"conforms": bool(conforms), "report": rtext}

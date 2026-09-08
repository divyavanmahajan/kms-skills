"""In-memory cosine search over embeddings stored in the Kuzu graph.

The corpus is small (hundreds of items), so exact brute-force search with
numpy is faster and simpler than an ANN index. Vectors are L2-normalised at
build time; similarity = dot product.
"""

from dataclasses import dataclass

import numpy as np

from .embeddings import embed_query


@dataclass
class Hit:
    id: str        # nugget uid / section sid / source path
    kind: str      # nugget | section | source
    score: float
    title: str     # claim / heading / source title
    detail: dict


class SearchIndex:
    def __init__(self, conn):
        """Load all embedded nodes from an open Kuzu connection."""
        ids: list[str] = []
        kinds: list[str] = []
        titles: list[str] = []
        details: list[dict] = []
        vectors: list[list[float]] = []

        for row in _rows(conn,
                "MATCH (s:Source)-[:HAS_NUGGET]->(n:Nugget) "
                "RETURN n.uid, n.claim, n.confidence, n.status, n.embedding, s.path"):
            uid, claim, confidence, status, vec, src = row
            if vec is None:
                continue
            ids.append(uid); kinds.append("nugget"); titles.append(claim)
            details.append({"confidence": confidence, "status": status, "source": src})
            vectors.append(vec)

        for row in _rows(conn,
                "MATCH (p:Page)-[:HAS_SECTION]->(s:Section) "
                "RETURN s.sid, s.heading, s.embedding, p.path, p.title"):
            sid, heading, vec, path, ptitle = row
            if vec is None:
                continue
            ids.append(sid); kinds.append("section")
            titles.append(f"{ptitle} › {heading}" if heading else ptitle)
            details.append({"page": path})
            vectors.append(vec)

        for row in _rows(conn,
                "MATCH (s:Source) WHERE s.embedding IS NOT NULL "
                "RETURN s.path, s.title, s.published, s.stype, s.embedding"):
            path, title, published, stype, vec = row
            ids.append(path); kinds.append("source"); titles.append(title)
            details.append({"published": published, "type": stype})
            vectors.append(vec)

        self.ids = ids
        self.kinds = np.array(kinds)
        self.titles = titles
        self.details = details
        self.matrix = (np.array(vectors, dtype=np.float32)
                       if vectors else np.zeros((0, 1), dtype=np.float32))

    def search(self, query: str, limit: int = 10,
               kinds: list[str] | None = None,
               min_score: float = 0.0) -> list[Hit]:
        if not self.ids:
            return []
        scores = self.matrix @ embed_query(query)
        if kinds:
            mask = np.isin(self.kinds, kinds)
            scores = np.where(mask, scores, -1.0)
        order = np.argsort(-scores)
        hits = []
        for i in order:
            if len(hits) >= limit or scores[i] < min_score or scores[i] < 0:
                break
            hits.append(Hit(id=self.ids[i], kind=str(self.kinds[i]),
                            score=round(float(scores[i]), 4),
                            title=self.titles[i], detail=self.details[i]))
        return hits


def _rows(conn, query: str):
    result = conn.execute(query)
    while result.has_next():
        yield result.get_next()

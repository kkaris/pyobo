# -*- coding: utf-8 -*-

"""Getters for OBO content."""

from typing import Iterable, Mapping, Optional, Tuple

import networkx as nx

from ..cache_utils import cached_mapping
from ..getters import get_obo_graph
from ..path_utils import prefix_directory_join

__all__ = [
    'get_id_name_mapping',
    'get_name_id_mapping',
]


def get_id_name_mapping(prefix: str, url: Optional[str] = None) -> Mapping[str, str]:
    """Get an identifier to name mapping for the OBO file."""
    path = prefix_directory_join(prefix, f"{prefix}.mapping.tsv")

    @cached_mapping(path=path, header=[f'{prefix}_id', 'name'])
    def _get_id_name_mapping() -> Mapping[str, str]:
        graph = get_obo_graph(prefix, url=url)
        return dict(_iterate_identifier_names(graph, prefix))

    return _get_id_name_mapping()


def get_name_id_mapping(prefix: str, url: Optional[str] = None) -> Mapping[str, str]:
    """Get a name to identifier mapping for the OBO file."""
    d = get_id_name_mapping(prefix=prefix, url=url)
    return {v: k for k, v in d.items()}


def _iterate_identifier_names(graph: nx.MultiDiGraph, prefix: str) -> Iterable[Tuple[str, str]]:
    for node, data in graph.nodes(data=True):
        identifier = node[len(f'{prefix}:'):]
        name = data.get('name')
        if name is None:
            continue
        yield identifier, name

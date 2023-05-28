from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Tag:
    name: str
    values: List[str]
    grouped: Optional[bool] = None
    dynamic: Optional[bool] = None


@dataclass
class Stream:
    metric: str
    tags: List[Tag]
    composite: Optional[str] = None
    group_function: Optional[str] = None
    summary_function: Optional[str] = None
    downsample_function: Optional[str] = None
    color: Optional[str] = None
    name: Optional[str] = None
    units_short: Optional[str] = None
    units_long: Optional[str] = None
    min: Optional[int] = None
    max: Optional[int] = None
    transform_function: Optional[str] = None
    period: Optional[int] = None


@dataclass
class Threshold:
    operator: str
    value: int
    type: str


@dataclass
class Chart:
    name: str
    type: str
    streams: List[Stream]
    min: Optional[int] = None
    max: Optional[int] = None
    label: Optional[str] = None
    related_space: Optional[int] = None
    thresholds: Optional[List[Threshold]] = None
    id: Optional[int] = field(default=None, compare=False)


@dataclass
class Dashboard:
    name: str
    charts: List[Chart]
    id: Optional[int] = field(default=None, compare=False)
    dynamic_tags: Optional[List[Tag]] = None

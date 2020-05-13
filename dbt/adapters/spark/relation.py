from dataclasses import dataclass

from dbt.adapters.base.relation import BaseRelation, Policy
from dbt.exceptions import RuntimeException


@dataclass
class SparkQuotePolicy(Policy):
    database: bool = False
    schema: bool = False
    identifier: bool = False


@dataclass
class SparkIncludePolicy(Policy):
    database: bool = False
    schema: bool = True
    identifier: bool = True


@dataclass(frozen=True, eq=False, repr=False)
class SparkRelation(BaseRelation):
    quote_policy: SparkQuotePolicy = SparkQuotePolicy()
    include_policy: SparkIncludePolicy = SparkIncludePolicy()
    quote_character: str = '`'

    def __post_init__(self):
        # some core things set database='', which we should ignore.
        if self.database and self.database != self.schema:
            raise RuntimeException(
                f'In relation with identifier={self.identifier}, '
                f'schema={self.schema}: got database={self.database}, but it '
                f'should not be set'
            )

    def render(self):
        if self.include_policy.database and self.include_policy.schema:
            raise RuntimeException(
                'Got a spark relation with schema and database set to '
                'include, but only one can be set'
            )
        return super().render()

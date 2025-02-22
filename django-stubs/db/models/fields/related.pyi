from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    Iterable,
    List,
    Optional,
    Protocol,
    Sequence,
    Tuple,
    Type,
    TypeVar,
    Union,
    overload,
)
from uuid import UUID

from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import Collector
from django.db.models.fields import Field
from django.db.models.fields.mixins import FieldCacheMixin
from django.db.models.fields.related_descriptors import (
    ForwardManyToOneDescriptor as ForwardManyToOneDescriptor,
)
from django.db.models.fields.related_descriptors import (  # noqa: F401
    ForwardOneToOneDescriptor as ForwardOneToOneDescriptor,
)
from django.db.models.fields.related_descriptors import (
    ManyToManyDescriptor as ManyToManyDescriptor,
)
from django.db.models.fields.related_descriptors import (
    ReverseManyToOneDescriptor as ReverseManyToOneDescriptor,
)
from django.db.models.fields.related_descriptors import (
    ReverseOneToOneDescriptor as ReverseOneToOneDescriptor,
)
from django.db.models.fields.reverse_related import (  # noqa: F401
    ForeignObjectRel as ForeignObjectRel,
)
from django.db.models.fields.reverse_related import ManyToManyRel as ManyToManyRel
from django.db.models.fields.reverse_related import ManyToOneRel as ManyToOneRel
from django.db.models.fields.reverse_related import OneToOneRel as OneToOneRel
from django.db.models.manager import ManyToManyRelatedManager
from django.db.models.query_utils import PathInfo, Q
from typing_extensions import Literal

class _DeleteProtocol(Protocol):
    def __call__(
        self,
        collector: Collector,
        field: Field[Any, Any],
        sub_objs: Sequence[Model],
        using: str,
    ) -> None: ...

_F = TypeVar("_F", bound=models.Field[Any, Any])
_Choice = Tuple[Any, str]
_ChoiceNamedGroup = Tuple[str, Iterable[_Choice]]
_FieldChoices = Iterable[Union[_Choice, _ChoiceNamedGroup]]
_ChoicesLimit = Union[Dict[str, Any], Q, Callable[[], Q]]
_OnDeleteOptions = Union[_DeleteProtocol, Callable[[Any], _DeleteProtocol]]

_ValidatorCallable = Callable[..., None]
_ErrorMessagesToOverride = Dict[str, Any]

RECURSIVE_RELATIONSHIP_CONSTANT: str = ...

# __set__ value type
_ST = TypeVar("_ST")
# __get__ return type
_GT = TypeVar("_GT")

class RelatedField(FieldCacheMixin, Field[_ST, _GT]):
    one_to_many: bool = ...
    one_to_one: bool = ...
    many_to_many: bool = ...
    many_to_one: bool = ...
    related_model: Type[_GT] = ...
    opts: Any = ...
    def get_forward_related_filter(self, obj: Model) -> Dict[str, Union[int, UUID]]: ...
    def get_reverse_related_filter(self, obj: Model) -> Q: ...
    @property
    def swappable_setting(self) -> Optional[str]: ...
    def set_attributes_from_rel(self) -> None: ...
    def do_related_class(self, other: Type[Model], cls: Type[Model]) -> None: ...
    def get_limit_choices_to(self) -> Dict[str, int]: ...
    def related_query_name(self) -> str: ...
    @property
    def target_field(self) -> Field[Any, Any]: ...
    @overload
    def __init__(
        self: RelatedField[_ST, _GT],
        related_name: Optional[str] = ...,
        related_query_name: Optional[str] = ...,
        limit_choices_to: Optional[_ChoicesLimit] = ...,
        verbose_name: Optional[str] = ...,
        name: Optional[str] = ...,
        primary_key: bool = ...,
        max_length: Optional[int] = ...,
        unique: bool = ...,
        blank: bool = ...,
        null: Literal[False] = ...,
        db_index: bool = ...,
        default: Optional[Union[_GT, Callable[[], _GT]]] = ...,
        editable: bool = ...,
        auto_created: bool = ...,
        serialize: bool = ...,
        unique_for_date: Optional[str] = ...,
        unique_for_month: Optional[str] = ...,
        unique_for_year: Optional[str] = ...,
        choices: Optional[_FieldChoices] = ...,
        help_text: str = ...,
        db_column: Optional[str] = ...,
        db_tablespace: Optional[str] = ...,
        validators: Iterable[_ValidatorCallable] = ...,
        error_messages: Optional[_ErrorMessagesToOverride] = ...,
    ) -> None: ...
    @overload
    def __init__(
        self: RelatedField[Optional[_ST], Optional[_GT]],
        related_name: Optional[str] = ...,
        related_query_name: Optional[str] = ...,
        limit_choices_to: Optional[_ChoicesLimit] = ...,
        verbose_name: Optional[str] = ...,
        name: Optional[str] = ...,
        primary_key: bool = ...,
        max_length: Optional[int] = ...,
        unique: bool = ...,
        blank: bool = ...,
        null: Literal[True] = ...,
        db_index: bool = ...,
        default: Optional[Union[_GT, Callable[[], _GT]]] = ...,
        editable: bool = ...,
        auto_created: bool = ...,
        serialize: bool = ...,
        unique_for_date: Optional[str] = ...,
        unique_for_month: Optional[str] = ...,
        unique_for_year: Optional[str] = ...,
        choices: Optional[_FieldChoices] = ...,
        help_text: str = ...,
        db_column: Optional[str] = ...,
        db_tablespace: Optional[str] = ...,
        validators: Iterable[_ValidatorCallable] = ...,
        error_messages: Optional[_ErrorMessagesToOverride] = ...,
    ) -> None: ...
    @overload
    def __new__(
        cls,
        *args: Any,
        null: Literal[False] = ...,
        **kwargs: Any,
    ) -> RelatedField[_ST, _GT]: ...
    @overload
    def __new__(
        cls,
        *args: Any,
        null: Literal[True],
        **kwargs: Any,
    ) -> RelatedField[Optional[_ST], Optional[_GT]]: ...

_M = TypeVar("_M", bound=Optional[Model])

class ForeignObject(RelatedField[_M, _M]):
    one_to_many: bool = False
    one_to_one: bool = False
    many_to_many: bool = False
    many_to_one: bool = True
    related_model: Type[_M] = ...
    @overload
    def __init__(
        self: ForeignObject[_M],
        to: Union[Type[_M], str],
        on_delete: _OnDeleteOptions,
        from_fields: Sequence[str],
        to_fields: Sequence[str],
        rel: Optional[ForeignObjectRel] = ...,
        related_name: Optional[str] = ...,
        related_query_name: Optional[str] = ...,
        limit_choices_to: Optional[_ChoicesLimit] = ...,
        parent_link: bool = ...,
        db_constraint: bool = ...,
        swappable: bool = ...,
        verbose_name: Optional[str] = ...,
        name: Optional[str] = ...,
        primary_key: bool = ...,
        unique: bool = ...,
        blank: bool = ...,
        null: Literal[False] = ...,
        db_index: bool = ...,
        default: Any = ...,
        editable: bool = ...,
        auto_created: bool = ...,
        serialize: bool = ...,
        choices: Optional[_FieldChoices] = ...,
        help_text: str = ...,
        db_column: Optional[str] = ...,
        db_tablespace: Optional[str] = ...,
        validators: Iterable[_ValidatorCallable] = ...,
        error_messages: Optional[_ErrorMessagesToOverride] = ...,
    ) -> None: ...
    @overload
    def __init__(
        self: ForeignObject[Optional[_M]],
        to: Union[Type[_M], str],
        on_delete: _OnDeleteOptions,
        from_fields: Sequence[str],
        to_fields: Sequence[str],
        rel: Optional[ForeignObjectRel] = ...,
        related_name: Optional[str] = ...,
        related_query_name: Optional[str] = ...,
        limit_choices_to: Optional[_ChoicesLimit] = ...,
        parent_link: bool = ...,
        db_constraint: bool = ...,
        swappable: bool = ...,
        verbose_name: Optional[str] = ...,
        name: Optional[str] = ...,
        primary_key: bool = ...,
        unique: bool = ...,
        blank: bool = ...,
        null: Literal[True] = ...,
        db_index: bool = ...,
        default: Any = ...,
        editable: bool = ...,
        auto_created: bool = ...,
        serialize: bool = ...,
        choices: Optional[_FieldChoices] = ...,
        help_text: str = ...,
        db_column: Optional[str] = ...,
        db_tablespace: Optional[str] = ...,
        validators: Iterable[_ValidatorCallable] = ...,
        error_messages: Optional[_ErrorMessagesToOverride] = ...,
    ) -> None: ...
    def __new__(
        cls,
        to: Union[Type[_M], str],
        on_delete: _OnDeleteOptions,
        from_fields: Sequence[str],
        to_fields: Sequence[str],
        rel: Optional[ForeignObjectRel] = ...,
        related_name: Optional[str] = ...,
        related_query_name: Optional[str] = ...,
        limit_choices_to: Optional[_ChoicesLimit] = ...,
        parent_link: bool = ...,
        db_constraint: bool = ...,
        swappable: bool = ...,
        verbose_name: Optional[str] = ...,
        name: Optional[str] = ...,
        primary_key: bool = ...,
        unique: bool = ...,
        blank: bool = ...,
        null: bool = ...,
        db_index: bool = ...,
        default: Any = ...,
        editable: bool = ...,
        auto_created: bool = ...,
        serialize: bool = ...,
        choices: Optional[_FieldChoices] = ...,
        help_text: str = ...,
        db_column: Optional[str] = ...,
        db_tablespace: Optional[str] = ...,
        validators: Iterable[_ValidatorCallable] = ...,
        error_messages: Optional[_ErrorMessagesToOverride] = ...,
    ) -> ForeignObject[_M]: ...

class ForeignKey(Generic[_M], ForeignObject[_M]):
    one_to_many: bool = False
    one_to_one: bool = False
    many_to_many: bool = False
    many_to_one: bool = True
    related_model: Type[_M] = ...
    @overload
    def __new__(
        cls,
        to: Union[Type[_M], str],
        on_delete: _OnDeleteOptions,
        *args: Any,
        null: Literal[False] = ...,
        **kwargs: Any,
    ) -> ForeignKey[_M]: ...
    @overload
    def __new__(
        cls,
        to: Union[Type[_M], str],
        on_delete: _OnDeleteOptions,
        *args: Any,
        null: Literal[True],
        **kwargs: Any,
    ) -> ForeignKey[Optional[_M]]: ...
    @overload
    def __init__(
        self: ForeignKey[_M],
        to: Union[Type[_M], str],
        on_delete: _OnDeleteOptions,
        to_field: Optional[str] = ...,
        related_name: Optional[str] = ...,
        related_query_name: Optional[str] = ...,
        limit_choices_to: Optional[_ChoicesLimit] = ...,
        parent_link: bool = ...,
        db_constraint: bool = ...,
        swappable: bool = ...,
        verbose_name: Optional[str] = ...,
        name: Optional[str] = ...,
        primary_key: bool = ...,
        unique: bool = ...,
        blank: bool = ...,
        null: Literal[False] = ...,
        db_index: bool = ...,
        default: Any = ...,
        editable: bool = ...,
        auto_created: bool = ...,
        serialize: bool = ...,
        choices: Optional[_FieldChoices] = ...,
        help_text: str = ...,
        db_column: Optional[str] = ...,
        db_tablespace: Optional[str] = ...,
        validators: Iterable[_ValidatorCallable] = ...,
        error_messages: Optional[_ErrorMessagesToOverride] = ...,
    ) -> None: ...
    @overload
    def __init__(
        self: ForeignKey[Optional[_M]],
        to: Union[Type[_M], str],
        on_delete: _OnDeleteOptions,
        to_field: Optional[str] = ...,
        related_name: Optional[str] = ...,
        related_query_name: Optional[str] = ...,
        limit_choices_to: Optional[_ChoicesLimit] = ...,
        parent_link: bool = ...,
        db_constraint: bool = ...,
        swappable: bool = ...,
        verbose_name: Optional[str] = ...,
        name: Optional[str] = ...,
        primary_key: bool = ...,
        unique: bool = ...,
        blank: bool = ...,
        null: Literal[True] = ...,
        db_index: bool = ...,
        default: Any = ...,
        editable: bool = ...,
        auto_created: bool = ...,
        serialize: bool = ...,
        choices: Optional[_FieldChoices] = ...,
        help_text: str = ...,
        db_column: Optional[str] = ...,
        db_tablespace: Optional[str] = ...,
        validators: Iterable[_ValidatorCallable] = ...,
        error_messages: Optional[_ErrorMessagesToOverride] = ...,
    ) -> None: ...
    # class access
    @overload  # type: ignore
    def __get__(self, instance: None, owner: Any) -> ForwardManyToOneDescriptor: ...
    # Model instance access
    @overload
    def __get__(self: ForeignKey[_M], instance: Any, owner: Any) -> _M: ...
    @overload
    def __get__(
        self: ForeignKey[Optional[_M]], instance: Any, owner: Any
    ) -> Optional[_M]: ...
    # non-Model instances
    @overload
    def __get__(self: _F, instance: Any, owner: Any) -> _F: ...

class OneToOneField(ForeignKey[_M]):
    one_to_many: bool = False
    one_to_one: bool = True
    many_to_many: bool = False
    many_to_one: bool = False
    related_model: Type[_M] = ...
    @overload
    def __new__(
        cls,
        to: Union[Type[_M], str],
        on_delete: _OnDeleteOptions,
        *args: Any,
        null: Literal[False] = ...,
        **kwargs: Any,
    ) -> OneToOneField[_M]: ...
    @overload
    def __new__(
        cls,
        to: Union[Type[_M], str],
        on_delete: _OnDeleteOptions,
        *args: Any,
        null: Literal[True],
        **kwargs: Any,
    ) -> OneToOneField[Optional[_M]]: ...
    # class access
    @overload  # type: ignore
    def __get__(self, instance: None, owner: Any) -> ForwardOneToOneDescriptor: ...
    # Model instance access
    @overload
    def __get__(self: OneToOneField[_M], instance: Any, owner: Any) -> _M: ...
    @overload
    def __get__(
        self: OneToOneField[Optional[_M]], instance: Any, owner: Any
    ) -> Optional[_M]: ...
    # non-Model instances
    @overload
    def __get__(self: _F, instance: Any, owner: Any) -> _F: ...

_MM = TypeVar("_MM", bound=Model)
_MN = TypeVar("_MN", bound=Model)

class ManyToManyField(
    Generic[_MM, _MN], RelatedField[Sequence[_MN], ManyToManyRelatedManager[_MM, _MN]]
):

    one_to_many: bool = False
    one_to_one: bool = False
    many_to_many: bool = False
    many_to_one: bool = True
    rel_class: Any = ...
    description: Any = ...
    has_null_arg: Any = ...
    swappable: bool = ...
    related_model: Type[_MM] = ...  # type: ignore [assignment]
    @overload
    def __new__(
        cls,
        to: Type[_MM],
        through: Type[_MN],
        *args: Any,
        **kwargs: Any,
    ) -> ManyToManyField[_MM, _MN]: ...
    @overload
    def __new__(
        cls,
        to: Type[_MM],
        through: Optional[str] = ...,
        *args: Any,
        **kwargs: Any,
    ) -> ManyToManyField[_MM, Any]: ...
    @overload
    def __new__(
        cls,
        to: str,
        through: Optional[str] = ...,
        *args: Any,
        **kwargs: Any,
    ) -> ManyToManyField[Any, Any]: ...
    def __init__(
        self,
        to: Union[Type[_MM], str],
        through: Optional[Union[Type[_MN], str]] = ...,
        to_field: Optional[str] = ...,
        related_name: Optional[str] = ...,
        related_query_name: Optional[str] = ...,
        limit_choices_to: Optional[_ChoicesLimit] = ...,
        symmetrical: Optional[bool] = ...,
        through_fields: Optional[Tuple[str, str]] = ...,
        db_constraint: bool = ...,
        swappable: bool = ...,
        verbose_name: Optional[str] = ...,
        name: Optional[str] = ...,
        primary_key: bool = ...,
        unique: bool = ...,
        blank: bool = ...,
        db_index: bool = ...,
        default: Any = ...,
        editable: bool = ...,
        auto_created: bool = ...,
        serialize: bool = ...,
        choices: Optional[_FieldChoices] = ...,
        help_text: str = ...,
        db_column: Optional[str] = ...,
        db_tablespace: Optional[str] = ...,
        validators: Iterable[_ValidatorCallable] = ...,
        error_messages: Optional[_ErrorMessagesToOverride] = ...,
    ) -> None: ...
    def get_path_info(self, filtered_relation: None = ...) -> List[PathInfo]: ...
    def get_reverse_path_info(
        self, filtered_relation: None = ...
    ) -> List[PathInfo]: ...
    def contribute_to_related_class(
        self, cls: Type[Model], related: RelatedField[Any, Any]
    ) -> None: ...
    def m2m_db_table(self) -> str: ...
    def m2m_column_name(self) -> str: ...
    def m2m_reverse_name(self) -> str: ...
    def m2m_reverse_field_name(self) -> str: ...
    def m2m_target_field_name(self) -> str: ...
    def m2m_reverse_target_field_name(self) -> str: ...

def create_many_to_many_intermediary_model(
    field: Type[Field[Any, Any]], klass: Type[Model]
) -> Type[Model]: ...
